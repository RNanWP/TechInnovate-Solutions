import pandas as pd
import numpy as np
from faker import Faker
import random

faker = Faker()
np.random.seed(42)
random.seed(42)

produtos_tecnologia = [
    ('iPhone Pro', 'Celular'),
    ('Notebook Dell', 'Notebook'),
    ('Samsung Galaxy S23', 'Celular'),
    ('Samsung Tab S6', 'Tablet'),
    ('Computador Gamer', 'Computador'),
    ('Apple Watch', 'Smartwatch'),
    ('Amazon Echo', 'Assistente Virtual'),
    ('Kindle Paperwhite', 'Leitor de eBooks'),
    ('Monitor LG 4K', 'Monitor'),
    ('Teclado Mecânico', 'Acessório')
]

clientes = pd.DataFrame({
    'cliente_id': range(1, 501),
    'nome': [faker.name() for _ in range(500)],
    'email': [faker.email() for _ in range(500)]
})

estoque = pd.DataFrame({
    'estoque_id': range(1, 501),
    'produto_id': np.random.randint(1, 21, 500),
    'quantidade': np.random.randint(1, 100, 500)
})

fornecedores = pd.DataFrame({
    'fornecedor_id': range(1, 501),
    'nome': [faker.company() for _ in range(500)],
    'contato': [faker.phone_number() for _ in range(500)]
})

itens_pedido = pd.DataFrame({
    'item_id': range(1, 501),
    'pedido_id': np.random.randint(1, 201, 500),
    'produto_id': np.random.randint(1, 21, 500),
    'quantidade': np.random.randint(1, 30, 500),
    'preco_unitario': np.round(np.random.uniform(100, 2000, 500), 2)  # Preço ajustado para produtos de tecnologia
})

pedidos = pd.DataFrame({
    'pedido_id': range(1, 501),
    'cliente_id': np.random.randint(1, 201, 500),
    'data_pedido': [faker.date_between(start_date='-1y', end_date='today') for _ in range(500)],
    'valor_total': np.round(np.random.uniform(500, 5000, 500), 2)  # Valor ajustado para pedidos de tecnologia
})

produtos = pd.DataFrame({
    'produto_id': range(1, 11),
    'nome': [item[0] for item in produtos_tecnologia],
    'categoria': [item[1] for item in produtos_tecnologia]
})

vendas = pd.DataFrame({
    'venda_id': range(1, 501),
    'produto_id': np.random.randint(1, 11, 500),
    'data_venda': [faker.date_between(start_date='-1y', end_date='today') for _ in range(500)],
    'quantidade': np.random.randint(1, 20, 500)
})

# Salvar dados em arquivos CSV
clientes.to_csv('Techinnovate-Solutions/Dados/clientes.csv', index=False)
estoque.to_csv('Techinnovate-Solutions/Dados/estoque.csv', index=False)
fornecedores.to_csv('Techinnovate-Solutions/Dados/fornecedores.csv', index=False)
itens_pedido.to_csv('Techinnovate-Solutions/Dados/itens_pedido.csv', index=False)
pedidos.to_csv('Techinnovate-Solutions/Dados/pedidos.csv', index=False)
produtos.to_csv('Techinnovate-Solutions/Dados/produtos.csv', index=False)
vendas.to_csv('Techinnovate-Solutions/Dados/vendas.csv', index=False)

print("Arquivos CSV criados com sucesso!")
