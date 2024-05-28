# Importando bibliotecas necessárias
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.api import OLS
from sklearn.linear_model import LinearRegression
import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from faker import Faker
from datetime import datetime
import random

# Conexão com o banco de dados usando SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

# Query SQL para selecionar os dados relevantes das tabelas de estoque e vendas
query = """
    SELECT e.produto_id, e.quantidade AS quantidade_em_estoque,
           v.data_venda, v.quantidade AS quantidade_vendida
    FROM estoque AS e
    INNER JOIN vendas AS v ON e.produto_id = v.produto_id
"""

# Carregando dados do banco de dados
dados = pd.read_sql(query, engine)

# Engenharia de características
dados['data_venda'] = pd.to_datetime(dados['data_venda'])
dados['dia_da_semana'] = dados['data_venda'].dt.dayofweek
dados['mes'] = dados['data_venda'].dt.month
dados['ano'] = dados['data_venda'].dt.year

# Definindo características e alvo
X = dados[['dia_da_semana', 'mes', 'ano', 'quantidade_em_estoque']]
y = dados['quantidade_vendida']

# Dividindo em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Fazendo previsões
rf_y_pred = modelo_rf.predict(X_test)

# Avaliando o modelo
mae_rf = mean_absolute_error(y_test, rf_y_pred)
mse_rf = mean_squared_error(y_test, rf_y_pred)
r2_rf = r2_score(y_test, rf_y_pred)

print("Erro Médio Absoluto (Random Forest):", mae_rf)
print("Erro Médio Quadrático (Random Forest):", mse_rf)
print("R2 Score (Random Forest):", r2_rf)

# Otimização do Modelo com GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=modelo_rf, param_grid=param_grid, cv=5, scoring='r2', n_jobs=-1)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_

modelo_rf_otimizado = RandomForestRegressor(**best_params, random_state=42)
modelo_rf_otimizado.fit(X_train, y_train)

rf_y_pred_otimizado = modelo_rf_otimizado.predict(X_test)

mae_rf_otimizado = mean_absolute_error(y_test, rf_y_pred_otimizado)
mse_rf_otimizado = mean_squared_error(y_test, rf_y_pred_otimizado)
r2_rf_otimizado = r2_score(y_test, rf_y_pred_otimizado)

print("Melhores parâmetros encontrados:", best_params)
print("Erro Médio Absoluto (Random Forest Otimizado):", mae_rf_otimizado)
print("Erro Médio Quadrático (Random Forest Otimizado):", mse_rf_otimizado)
print("R2 Score (Random Forest Otimizado):", r2_rf_otimizado)

# Prevendo a demanda futura para um produto específico                 
produto_id_desejado = 9                                                           #                                      /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                      #/////////////////////////////////////////////          ALTERAR PRODUTO      /////////////////////////////////////////////////////////////
                                      #/////////////////////////////////////////////            DESEJADO           /////////////////////////////////////////////////////////////
                                      #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                                                      

# Consulta SQL para obter o nome do produto
consulta_nome_produto = f"SELECT nome FROM produtos WHERE produto_id = {produto_id_desejado}"

# Carregar o nome do produto
nome_produto = pd.read_sql_query(consulta_nome_produto, engine)['nome'].iloc[0]

# Obtendo a quantidade de estoque atual do produto desejado
quantidade_em_estoque_atual = dados.loc[dados['produto_id'] == produto_id_desejado, 'quantidade_em_estoque'].iloc[0]

# Criando um dataframe para representar o futuro (próximos 7 dias)
futuro = pd.DataFrame({
    'dia_da_semana': [i % 7 for i in range(1, 8)],  # Considerando os próximos 7 dias
    'mes': [6] * 7,
    'ano': [2024] * 7,
    'quantidade_em_estoque': quantidade_em_estoque_atual
})

# Realizando previsões para o futuro
demandas_futuras = modelo_rf_otimizado.predict(futuro[['dia_da_semana', 'mes', 'ano', 'quantidade_em_estoque']])

# Imprimindo previsões para cada dia
print(f"\nPrevisão de demanda futura para o produto '{nome_produto}' em junho de 2024:")
for dia, demanda in zip(futuro['dia_da_semana'], demandas_futuras):
    print(f"Dia da semana {dia}: {demanda:.2f} unidades")

# Calculando a média da demanda prevista
media_demanda_prevista = demandas_futuras.mean()
print(f"\nMédia da demanda prevista: {media_demanda_prevista:.2f} unidades por dia")

# Calculando o estoque sugerido para uma semana (supondo uma semana de estoque de segurança)
sugestao_estoque = media_demanda_prevista * 7
print(f"Estoque sugerido para uma semana: {sugestao_estoque:.2f} unidades")

# Crie gráficos para representar padrões e tendências

# Gráfico de dispersão
sns.scatterplot(x='dia_da_semana', y='quantidade_vendida', data=dados)
plt.title('Dispersão entre dia da semana e quantidade vendida')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade Vendida')
plt.show()

# Identificar padrões
tendencia = dados['dia_da_semana'].value_counts()
print("Tendência de vendas por dia da semana:")
print(tendencia)

# Regressão linear
modelo = OLS(y, X)
resultados = modelo.fit()
print("\nRegressão Linear com OLS:")
print(resultados.summary())

# Modelo de regressão linear
modelo_reg_linear = LinearRegression()
modelo_reg_linear.fit(X, y)
coeficientes = modelo_reg_linear.coef_
print("\nCoeficientes do modelo de regressão linear:")
print(coeficientes)

# Comparando Random Forest com Random Forest Otimizado
if r2_rf > r2_rf_otimizado:
    print('Random Forest é melhor.')
else:
    print('Random Forest Otimizado é melhor.')

# Comparando Random Forest Otimizado com Regressão Linear
if r2_rf_otimizado > resultados.rsquared:
    print('Random Forest Otimizado é melhor que a Regressão Linear.')
else:
    print('Regressão Linear é melhor que o Random Forest Otimizado.')


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////          CRIAÇÃO DOS          /////////////////////////////////////////////////////////////
# /////////////////////////////////////////////            GRAFICOS           /////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Instância do Faker
fake = Faker()


def gerar_dados_aleatorios(num_pedidos, num_itens_por_pedido):
    # Carregar dados de clientes e produtos
    clientes = pd.read_sql("SELECT cliente_id FROM clientes", engine)
    produtos = pd.read_sql("SELECT produto_id FROM produtos", engine)

    if clientes.empty or produtos.empty:
        print("Certifique-se de que as tabelas clientes e produtos não estão vazias.")
        return

    pedidos_dados = []
    itens_pedido_dados = []

    for _ in range(num_pedidos):
        cliente_id = int(random.choice(clientes['cliente_id']))
        data_pedido = fake.date_between(start_date='-1y', end_date='today')
        valor_total = round(random.uniform(50, 500), 2)

        # Adicionar dados do pedido
        pedidos_dados.append((cliente_id, data_pedido, valor_total))

    # Inserir dados na tabela pedidos e obter os IDs gerados
    with engine.connect() as connection:
        result = connection.execute(
            text("INSERT INTO pedidos (cliente_id, data_pedido, valor_total) VALUES (:cliente_id, :data_pedido, :valor_total)"),
            [dict(cliente_id=pedido[0], data_pedido=pedido[1], valor_total=pedido[2]) for pedido in pedidos_dados]
        )
        connection.commit()

        # Obter os IDs dos pedidos inseridos
        pedido_ids = pd.read_sql("SELECT pedido_id FROM pedidos ORDER BY pedido_id DESC LIMIT %s" % num_pedidos, engine)['pedido_id']

        for pedido_id in pedido_ids:
            for _ in range(num_itens_por_pedido):
                produto_id = int(random.choice(produtos['produto_id']))
                quantidade = random.randint(1, 10)
                preco_unitario = round(random.uniform(10, 100), 2)

                # Adicionar item do pedido na lista
                itens_pedido_dados.append((pedido_id, produto_id, quantidade, preco_unitario))

        # Inserir itens na tabela itens_pedido
        connection.execute(
            text("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (:pedido_id, :produto_id, :quantidade, :preco_unitario)"),
            [dict(pedido_id=item[0], produto_id=item[1], quantidade=item[2], preco_unitario=item[3]) for item in itens_pedido_dados]
        )
        connection.commit()



def exibir_tabela(tabela):
    consulta = f"SELECT * FROM {tabela}"
    dados = pd.read_sql(consulta, engine)
    janela_tabela = tk.Toplevel(root)
    janela_tabela.title(f"Tabela {tabela.capitalize()}")

    estilo_fonte = ("Helvetica", 10)
    estilo_tabela = ttk.Style()
    estilo_tabela.configure("Treeview", font=estilo_fonte, rowheight=25)

    frame = ttk.Frame(janela_tabela)
    frame.pack(expand=True, fill="both")

    tabela_treeview = ttk.Treeview(
        frame, columns=list(dados.columns), show="headings")
    tabela_treeview.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical",
                              command=tabela_treeview.yview)
    scrollbar.pack(side="right", fill="y")
    tabela_treeview.configure(yscrollcommand=scrollbar.set)

    for coluna in dados.columns:
        tabela_treeview.heading(coluna, text=coluna)

    for indice, linha in dados.iterrows():
        tabela_treeview.insert("", "end", values=list(linha))


# Criando a janela principal
root = tk.Tk()
root.title("Exibição de Tabelas")
root.geometry("350x500")

estilo_fonte_btn = ("Helvetica", 12)
style_btn = ttk.Style()
style_btn.configure("TButton", font=estilo_fonte_btn, padding=7)

btn_clientes = ttk.Button(root, text="Clientes",
                          command=lambda: exibir_tabela("clientes"))
btn_clientes.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_estoque = ttk.Button(root, text="Estoque",
                         command=lambda: exibir_tabela("estoque"))
btn_estoque.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_fornecedores = ttk.Button(
    root, text="Fornecedores", command=lambda: exibir_tabela("fornecedores"))
btn_fornecedores.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_produtos = ttk.Button(root, text="Produtos",
                          command=lambda: exibir_tabela("produtos"))
btn_produtos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_vendas = ttk.Button(root, text="Vendas",
                        command=lambda: exibir_tabela("vendas"))
btn_vendas.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_pedidos = ttk.Button(root, text="Pedidos",
                         command=lambda: exibir_tabela("pedidos"))
btn_pedidos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_itens_pedido = ttk.Button(
    root, text="Itens Pedido", command=lambda: exibir_tabela("itens_pedido"))
btn_itens_pedido.pack(pady=5, padx=10, ipadx=10, ipady=5)

# Botão para gerar dados aleatórios
btn_gerar_dados = ttk.Button(
    root, text="Gerar Dados Aleatórios", command=lambda: gerar_dados_aleatorios(10, 5))
btn_gerar_dados.pack(pady=10, padx=10, ipadx=10, ipady=5)

# Loop principal da aplicação
root.mainloop()