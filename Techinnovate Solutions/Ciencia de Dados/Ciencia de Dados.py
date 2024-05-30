from faker import Faker
import numpy as np
import pandas as pd
import random
from sklearn.model_selection import train_test_split

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
