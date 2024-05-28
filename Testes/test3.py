import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pandas as pd
from sqlalchemy import create_engine, text
import random
from datetime import datetime
from faker import Faker

# Configuração da conexão com o banco de dados
engine = create_engine(
    'mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

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
