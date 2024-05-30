import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from statsmodels.regression.linear_model import OLS
from sklearn.linear_model import LinearRegression
import random
from faker import Faker

# Carregar os dados gerados
estoque = pd.read_csv('dados/estoque.csv')
vendas = pd.read_csv('dados/vendas.csv')
produtos = pd.read_csv('dados/produtos.csv')

# Engenharia de características
vendas['data_venda'] = pd.to_datetime(vendas['data_venda'])
vendas['dia_da_semana'] = vendas['data_venda'].dt.dayofweek
vendas['mes'] = vendas['data_venda'].dt.month
vendas['ano'] = vendas['data_venda'].dt.year

# Mesclar os dados de estoque e vendas
dados = pd.merge(estoque, vendas, on='produto_id')

# Ajuste das colunas de características e alvo
X = dados[['dia_da_semana', 'mes', 'ano', 'quantidade_x']]
y = dados['quantidade_y']

# Treinando o modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
modelo_rf.fit(X, y)

# Prevendo a demanda futura para um produto específico
produto_id_desejado = 2  # Alterar conforme necessário

# Obtendo o nome do produto desejado
nome_produto_desejado = produtos.loc[produtos['produto_id'] == produto_id_desejado, 'nome'].iloc[0]

# Obtendo a quantidade de estoque atual do produto desejado
quantidade_em_estoque_atual = dados.loc[dados['produto_id'] == produto_id_desejado, 'quantidade_x'].iloc[0]

# Criando um dataframe para representar o futuro (próximos 7 dias)
futuro = pd.DataFrame({
    'dia_da_semana': [i % 7 for i in range(1, 8)],
    'mes': [6] * 7,
    'ano': [2024] * 7,
    'quantidade_x': quantidade_em_estoque_atual  # Use 'quantidade_x' em vez de 'quantidade_estoque'
})

# Realizando previsões para o futuro
demandas_futuras = modelo_rf_otimizado.predict(futuro[['dia_da_semana', 'mes', 'ano', 'quantidade_x']])  # Use 'quantidade_x' em vez de 'quantidade_estoque'


# Calculando a média da demanda prevista
media_demanda_prevista = demandas_futuras.mean()

# Calculando o estoque sugerido para uma semana (supondo uma semana de estoque de segurança)
sugestao_estoque = media_demanda_prevista * 7

# Comparando Random Forest com Regressão Linear
modelo_reg_linear = LinearRegression()
modelo_reg_linear.fit(X, y)

# Criando o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Ciência de Dados'),

    html.Div(children=[
        html.H2(children=f"Previsão de demanda futura para o produto '{nome_produto_desejado}' em junho de 2024:"),
        html.Ul([html.Li(f"Dia da semana {i+1}: {demanda:.2f} unidades") for i, demanda in enumerate(demandas_futuras)]),
        html.Div(f"Média da demanda prevista: {media_demanda_prevista:.2f} unidades por dia"),
        html.Div(f"Estoque sugerido para uma semana: {sugestao_estoque:.2f} unidades"),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='scatter-plot',
            figure={
                'data': [
                    go.Scatter(
                        x=X_test['dia_da_semana'],
                        y=y_test,
                        mode='markers',
                        marker=dict(color='blue'),
                        name='Real'
                    ),
                    go.Scatter(
                        x=X_test['dia_da_semana'],
                        y=rf_y_pred,
                        mode='lines',
                        marker=dict(color='red'),
                        name='Previsão Random Forest'
                    ),
                    go.Scatter(
                        x=X_test['dia_da_semana'],
                        y=modelo_reg_linear.predict(X_test),
                        mode='lines',
                        marker=dict(color='green'),
                        name='Previsão Regressão Linear'
                    ),
                ],
                'layout': go.Layout(
                    title='Dispersão entre dia da semana e quantidade vendida',
                    xaxis={'title': 'Dia da Semana'},
                    yaxis={'title': 'Quantidade Vendida'},
                )
            }
        )
    ]),
])

# Executando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
