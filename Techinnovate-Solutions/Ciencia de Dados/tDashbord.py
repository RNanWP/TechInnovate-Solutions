import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Carregar dados do banco de dados
engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')
query = """
    SELECT e.produto_id, e.quantidade AS quantidade_em_estoque,
           v.data_venda, v.quantidade AS quantidade_vendida
    FROM estoque AS e
    INNER JOIN vendas AS v ON e.produto_id = v.produto_id
"""
dados = pd.read_sql(query, engine)

# Engenharia de características
dados['data_venda'] = pd.to_datetime(dados['data_venda'])
dados['dia_da_semana'] = dados['data_venda'].dt.dayofweek
dados['mes'] = dados['data_venda'].dt.month
dados['ano'] = dados['data_venda'].dt.year

# Adicionar 'data_venda' às características
X = dados[['dia_da_semana', 'mes', 'ano', 'quantidade_em_estoque', 'data_venda']]
y = dados['quantidade_vendida']

# Dividindo em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train.drop(columns=['data_venda']), y_train)

# Fazendo previsões
rf_y_pred = modelo_rf.predict(X_test.drop(columns=['data_venda']))

# Avaliando o modelo
mae_rf = mean_absolute_error(y_test, rf_y_pred)
mse_rf = mean_squared_error(y_test, rf_y_pred)
r2_rf = r2_score(y_test, rf_y_pred)

# Dados para visualização
resultados = {
    'Erro Médio Absoluto': mae_rf,
    'Erro Médio Quadrático': mse_rf,
    'R2 Score': r2_rf
}

# Visualizando previsões e valores reais
previsoes = pd.DataFrame({
    'data_venda': X_test['data_venda'],
    'quantidade_vendida_real': y_test,
    'quantidade_vendida_prevista': rf_y_pred
}).sort_values('data_venda')

# Criação do dashboard
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Dashboard de Previsão de Demanda e Gerenciamento de Dados"),

    # Gráfico de resultados de avaliação
    dcc.Graph(
        id='resultado-avaliacao',
        figure=go.Figure(
            data=[go.Bar(
                x=list(resultados.keys()),
                y=list(resultados.values())
            )],
            layout=go.Layout(
                title="Resultados de Avaliação do Modelo"
            )
        )
    ),

    # Gráfico de tendências de vendas e previsões
    dcc.Graph(
        id='tendencias-previsoes',
        figure=make_subplots(rows=2, cols=1, shared_xaxes=True,
                             subplot_titles=("Vendas Reais ao Longo do Tempo", "Previsões vs Vendas Reais"),
                             vertical_spacing=0.2)
            .add_trace(go.Scatter(x=dados['data_venda'], y=dados['quantidade_vendida'],
                                  mode='lines', name='Vendas Reais'), row=1, col=1)
            .add_trace(go.Scatter(x=previsoes['data_venda'], y=previsoes['quantidade_vendida_real'],
                                  mode='lines', name='Vendas Reais'), row=2, col=1)
            .add_trace(go.Scatter(x=previsoes['data_venda'], y=previsoes['quantidade_vendida_prevista'],
                                  mode='lines', name='Vendas Previstas'), row=2, col=1)
            .update_layout(title="Tendências de Vendas e Previsões",
                           height=800)
    ),

    # Tabela de dados de vendas
    dash_table.DataTable(
        id='tabela-vendas',
        columns=[{"name": i, "id": i} for i in dados.columns],
        data=dados.to_dict('records'),
        page_size=10,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
