# import pandas as pd
# from sqlalchemy import create_engine

# # Conexão com o banco de dados usando SQLAlchemy
# engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

# # Query SQL para selecionar todas as vendas
# query = "SELECT * FROM Vendas"

# # Carregando dados do banco de dados
# dados = pd.read_sql(query, engine)

# # Fechando a conexão
# engine.dispose()

# # Engenharia de características
# dados['data_venda'] = pd.to_datetime(dados['data_venda'])
# dados['dia_da_semana'] = dados['data_venda'].dt.dayofweek
# dados['mes'] = dados['data_venda'].dt.month
# dados['ano'] = dados['data_venda'].dt.year

# # Definindo características e alvo
# X = dados[['dia_da_semana', 'mes', 'ano', 'produto_id']]
# y = dados['quantidade']
