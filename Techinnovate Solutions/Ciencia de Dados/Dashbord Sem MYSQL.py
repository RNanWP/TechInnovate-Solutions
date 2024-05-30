import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from faker import Faker
import random

# Função para gerar dados aleatórios de pedidos e itens de pedido
def gerar_dados_aleatorios(num_pedidos, num_itens_por_pedido):
    # Aqui você pode implementar a geração de dados aleatórios se necessário
    pass

# Carregar os dados CSV
clientes = pd.read_csv('dados/clientes.csv')
produtos = pd.read_csv('dados/produtos.csv')
pedidos = pd.read_csv('dados/pedidos.csv')
itens_pedido = pd.read_csv('dados/itens_pedido.csv')

# Inicializar o Faker
fake = Faker()

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Dados de Vendas', style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Div(children=[
        html.Div(children=[
            html.H2(children='Dados dos Pedidos', style={'textAlign': 'center'}),
            dcc.Graph(
                id='grafico-pedidos',
                figure={
                    'data': [
                        go.Scatter(
                            x=pedidos['data_pedido'],
                            y=pedidos['valor_total'],
                            mode='markers',
                            marker=dict(color='blue'),
                            name='Valor Total'
                        )
                    ],
                    'layout': go.Layout(
                        title='Valor Total dos Pedidos ao Longo do Tempo',
                        xaxis={'title': 'Data do Pedido'},
                        yaxis={'title': 'Valor Total'},
                        plot_bgcolor='#f9f9f9',
                        paper_bgcolor='#f9f9f9'
                    )
                }
            )
        ], className='six columns'),

        html.Div(children=[
            html.H2(children='Dados dos Itens de Pedido', style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='dropdown-produto',
                options=[{'label': produto, 'value': produto} for produto in produtos['nome']],
                value=produtos['nome'].iloc[0],
                style={'width': '100%'}
            ),
            dcc.Graph(
                id='grafico-itens-pedido'
            )
        ], className='six columns')
    ], className='row')
])

# Callback para atualizar o gráfico de itens de pedido com base no produto selecionado
@app.callback(
    Output('grafico-itens-pedido', 'figure'),
    [Input('dropdown-produto', 'value')]
)
def atualizar_grafico_itens_pedido(produto_selecionado):
    # Filtrar itens de pedido para o produto selecionado
    produto_id = produtos.loc[produtos['nome'] == produto_selecionado, 'produto_id'].iloc[0]
    itens_filtrados = itens_pedido[itens_pedido['produto_id'] == produto_id]

    # Juntar com os pedidos para obter a data do pedido
    dados = pd.merge(itens_filtrados, pedidos, on='pedido_id')

    # Agrupar por data do pedido e somar a quantidade
    dados_agrupados = dados.groupby('data_pedido')['quantidade'].sum().reset_index()

    # Criar figura do gráfico
    figura = {
        'data': [
            go.Bar(
                x=dados_agrupados['data_pedido'],
                y=dados_agrupados['quantidade'],
                marker=dict(color='green'),
                name='Quantidade Vendida'
            )
        ],
        'layout': go.Layout(
            title=f'Quantidade do Produto "{produto_selecionado}" Vendida ao Longo do Tempo',
            xaxis={'title': 'Data do Pedido'},
            yaxis={'title': 'Quantidade Vendida'},
            plot_bgcolor='#f9f9f9',
            paper_bgcolor='#f9f9f9'
        )
    }

    return figura

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
