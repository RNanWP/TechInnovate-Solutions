import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.api import OLS
from sklearn.linear_model import LinearRegression
import random
from faker import Faker
from tkinter import ttk
import tkinter as tk

faker = Faker()
np.random.seed(42)
random.seed(42)

# Carregar os dados gerados
estoque = pd.read_csv('Techinnovate Solutions/Dados-csv/estoque.csv')
vendas = pd.read_csv('Techinnovate Solutions/Dados-csv/vendas.csv')
produtos = pd.read_csv('Techinnovate Solutions/Dados-csv/produtos.csv')

# Engenharia de características
vendas['data_venda'] = pd.to_datetime(vendas['data_venda'])
vendas['dia_da_semana'] = vendas['data_venda'].dt.dayofweek
vendas['mes'] = vendas['data_venda'].dt.month
vendas['ano'] = vendas['data_venda'].dt.year

dados = pd.merge(estoque, vendas, on='produto_id')

print(dados.columns)

X = dados[['dia_da_semana', 'mes', 'ano', 'quantidade_x']]
y = dados['quantidade_y']

X.columns = ['dia_da_semana', 'mes', 'ano', 'quantidade_estoque']
y.name = 'quantidade_vendida'

# Dividindo em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
modelo_rf.fit(X_train, y_train)

rf_y_pred = modelo_rf.predict(X_test)

mae_rf = mean_absolute_error(y_test, rf_y_pred)
mse_rf = mean_squared_error(y_test, rf_y_pred)
r2_rf = r2_score(y_test, rf_y_pred)

print("Erro Médio Absoluto (Random Forest):", mae_rf)
print("Erro Médio Quadrático (Random Forest):", mse_rf)
print("R2 Score (Random Forest):", r2_rf)

# Otimização do Modelo com RandomizedSearchCV
param_dist = {
    'n_estimators': [50, 100, 200],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

random_search = RandomizedSearchCV(estimator=modelo_rf, param_distributions=param_dist, n_iter=20, cv=5, scoring='r2', n_jobs=-1, random_state=42)
random_search.fit(X_train, y_train)

best_params = random_search.best_params_

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

produto_id_desejado = 2  # Alterar conforme necessário               ///////////////////////////////////////////////////////////////////////////////////////
                                                                    #///////////////////////////////    ALTERAR PRODUTO     ////////////////////////////////
                                                                    #///////////////////////////////        DESEJADO        ////////////////////////////////
                                                                    #///////////////////////////////////////////////////////////////////////////////////////

nome_produto_desejado = produtos.loc[produtos['produto_id'] == produto_id_desejado, 'nome'].iloc[0]

quantidade_em_estoque_atual = dados.loc[dados['produto_id'] == produto_id_desejado, 'quantidade_x'].iloc[0]

# Criando um dataframe para representar o futuro (próximos 7 dias)
futuro = pd.DataFrame({
    'dia_da_semana': [i % 7 for i in range(1, 8)],
    'mes': [6] * 7,
    'ano': [2024] * 7,
    'quantidade_estoque': quantidade_em_estoque_atual
})

# Realizando previsões para o futuro
demandas_futuras = modelo_rf_otimizado.predict(futuro[['dia_da_semana', 'mes', 'ano', 'quantidade_estoque']])

# Imprimindo previsões para cada dia
print(f"\nPrevisão de demanda futura para o produto '{nome_produto_desejado}' em junho de 2024:")
for dia, demanda in zip(futuro['dia_da_semana'], demandas_futuras):
    print(f"Dia da semana {dia}: {demanda:.2f} unidades")

media_demanda_prevista = demandas_futuras.mean()
print(f"\nMédia da demanda prevista: {media_demanda_prevista:.2f} unidades por dia")

sugestao_estoque = media_demanda_prevista * 7
print(f"Estoque sugerido para uma semana: {sugestao_estoque:.2f} unidades")

# Gráfico de dispersão
sns.scatterplot(x='dia_da_semana', y=y_test, data=X_test)
plt.title('Dispersão entre dia da semana e quantidade vendida')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade Vendida')
plt.show()

tendencia = dados['dia_da_semana'].value_counts().sort_index()
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
intercepto = modelo_reg_linear.intercept_

print("\nCoeficientes da regressão linear:", coeficientes)
print("Intercepto da regressão linear:", intercepto)

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


fake = Faker()

def gerar_dados_aleatorios(num_pedidos, num_itens_por_pedido):
    clientes = pd.read_csv('Techinnovate Solutions/Dados-csv/clientes.csv')
    produtos = pd.read_csv('Techinnovate Solutions/Dados-csv/produtos.csv')

    if clientes.empty or produtos.empty:
        print("Certifique-se de que os arquivos clientes.csv e produtos.csv não estão vazios.")
        return

    pedidos_dados = []
    itens_pedido_dados = []

    for _ in range(num_pedidos):
        cliente_id = int(random.choice(clientes['cliente_id']))
        data_pedido = fake.date_between(start_date='-1y', end_date='today')
        valor_total = round(random.uniform(50, 500), 2)

        # Adicionar dados do pedido
        pedidos_dados.append((cliente_id, data_pedido, valor_total))

    pedidos_df = pd.DataFrame(pedidos_dados, columns=['cliente_id', 'data_pedido', 'valor_total'])
    pedidos_df['pedido_id'] = range(len(pedidos_dados))
    pedidos_df.to_csv('pedidos.csv', mode='a', header=False, index=False)

    pedidos_inseridos = pd.read_csv('Techinnovate Solutions/Dados-csv/pedidos.csv')
    pedido_ids = pedidos_inseridos['pedido_id'].tail(num_pedidos).tolist()

    for pedido_id in pedido_ids:
        for _ in range(num_itens_por_pedido):
            produto_id = int(random.choice(produtos['produto_id']))
            quantidade = random.randint(1, 10)
            preco_unitario = round(random.uniform(10, 100), 2)

            itens_pedido_dados.append((pedido_id, produto_id, quantidade, preco_unitario))

    itens_pedido_df = pd.DataFrame(itens_pedido_dados, columns=['pedido_id', 'produto_id', 'quantidade', 'preco_unitario'])
    itens_pedido_df['item_id'] = range(len(itens_pedido_dados))
    itens_pedido_df.to_csv('Techinnovate Solutions/Dados-csv/itens_pedido.csv', mode='a', header=False, index=False)

    print("Dados aleatórios gerados e salvos nos arquivos CSV!")

# Função para exibir dados de uma tabela CSV
def exibir_tabela(tabela):
    dados = pd.read_csv(f'{tabela}.csv')
    janela_tabela = tk.Toplevel(root)
    janela_tabela.title(f"Tabela {tabela.capitalize()}")

    estilo_fonte = ("Helvetica", 10)
    estilo_tabela = ttk.Style()
    estilo_tabela.configure("Treeview", font=estilo_fonte, rowheight=25)

    frame = ttk.Frame(janela_tabela)
    frame.pack(expand=True, fill="both")

    tabela_treeview = ttk.Treeview(frame, columns=list(dados.columns), show="headings")
    tabela_treeview.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabela_treeview.yview)
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

btn_clientes = ttk.Button(root, text="Clientes", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/clientes"))
btn_clientes.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_estoque = ttk.Button(root, text="Estoque", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/estoque"))
btn_estoque.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_fornecedores = ttk.Button(root, text="Fornecedores", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/fornecedores"))
btn_fornecedores.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_produtos = ttk.Button(root, text="Produtos", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/produtos"))
btn_produtos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_vendas = ttk.Button(root, text="Vendas", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/vendas"))
btn_vendas.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_pedidos = ttk.Button(root, text="Pedidos", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/pedidos"))
btn_pedidos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_itens_pedido = ttk.Button(root, text="Itens Pedido", command=lambda: exibir_tabela("Techinnovate Solutions/Dados-csv/itens_pedido"))
btn_itens_pedido.pack(pady=5, padx=10, ipadx=10, ipady=5)

# Botão para gerar dados aleatórios
btn_gerar_dados = ttk.Button(root, text="Gerar Dados Aleatórios", command=lambda: gerar_dados_aleatorios(10, 5))
btn_gerar_dados.pack(pady=10, padx=10, ipadx=10, ipady=5)


# Loop principal da aplicação
root.mainloop()
