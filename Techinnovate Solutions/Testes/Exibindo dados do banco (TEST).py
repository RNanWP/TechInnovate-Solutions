import pandas as pd
from sqlalchemy import create_engine

# Conexão com o banco de dados usando SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

# Consulta SQL para cada tabela
consulta_clientes = "SELECT * FROM clientes"
consulta_estoque = "SELECT * FROM estoque"
consulta_fornecedores = "SELECT * FROM fornecedores"
consulta_produtos = "SELECT * FROM produtos"
consulta_venda = "SELECT * FROM vendas"

# Carregando dados de cada tabela
clientes = pd.read_sql(consulta_clientes, engine)
estoque = pd.read_sql(consulta_estoque, engine)
fornecedores = pd.read_sql(consulta_fornecedores, engine)
produtos = pd.read_sql(consulta_produtos, engine)
venda = pd.read_sql(consulta_venda, engine)

# Fechando a conexão
engine.dispose()

# Exibindo os dados de cada tabela
print("Tabela Clientes:")
print(clientes)
print("\nTabela Estoque:")
print(estoque)
print("\nTabela Fornecedores:")
print(fornecedores)
print("\nTabela Produtos:")
print(produtos)
print("\nTabela Venda:")
print(venda)
