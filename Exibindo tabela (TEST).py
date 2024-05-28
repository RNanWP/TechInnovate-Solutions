import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Configuração da conexão com o banco de dados
engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

def exibir_tabela(tabela):
    # Consulta SQL para selecionar todos os registros da tabela
    consulta = f"SELECT * FROM {tabela}"
    
    # Carregando dados da tabela
    dados = pd.read_sql(consulta, engine)
    
    # Criando uma nova janela para exibir os dados
    janela_tabela = tk.Toplevel(root)
    janela_tabela.title(f"Tabela {tabela.capitalize()}")
    
    # Estilo da fonte para a tabela
    estilo_fonte = ("Helvetica", 10)
    
    # Estilo para a tabela
    estilo_tabela = ttk.Style()
    estilo_tabela.configure("Treeview", font=estilo_fonte, rowheight=25)
    
    # Criando a tabela com rolagem
    frame = ttk.Frame(janela_tabela)
    frame.pack(expand=True, fill="both")
    
    tabela_treeview = ttk.Treeview(frame, columns=list(dados.columns), show="headings")
    tabela_treeview.pack(side="left", fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabela_treeview.yview)
    scrollbar.pack(side="right", fill="y")
    tabela_treeview.configure(yscrollcommand=scrollbar.set)
    
    # Adicionando os cabeçalhos das colunas
    for coluna in dados.columns:
        tabela_treeview.heading(coluna, text=coluna)
    
    # Adicionando as linhas com os dados
    for indice, linha in dados.iterrows():
        tabela_treeview.insert("", "end", values=list(linha))

def registrar_pedido(cliente_id, produtos):
    # produtos é uma lista de dicionários, cada dicionário contém produto_id, quantidade, preco_unitario
    data_pedido = datetime.now().date()
    valor_total = sum(item['quantidade'] * item['preco_unitario'] for item in produtos)
    
    # Inserir pedido na tabela pedidos
    with engine.connect() as connection:
        result = connection.execute(
            "INSERT INTO pedidos (cliente_id, data_pedido, valor_total) VALUES (%s, %s, %s)",
            (cliente_id, data_pedido, valor_total)
        )
        pedido_id = result.lastrowid
    
        # Inserir itens do pedido na tabela itens_pedido
        for item in produtos:
            connection.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)",
                (pedido_id, item['produto_id'], item['quantidade'], item['preco_unitario'])
            )
    return pedido_id

# Criando a janela principal
root = tk.Tk()
root.title("Exibição de Tabelas")
root.geometry("350x350")

# Estilo da fonte para os botões
estilo_fonte_btn = ("Helvetica", 12)

style_btn = ttk.Style()
style_btn.configure("TButton", font=estilo_fonte_btn, padding=7)

# Criando botões para exibir cada tabela
btn_clientes = ttk.Button(root, text="Clientes", command=lambda: exibir_tabela("clientes"))
btn_clientes.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_estoque = ttk.Button(root, text="Estoque", command=lambda: exibir_tabela("estoque"))
btn_estoque.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_fornecedores = ttk.Button(root, text="Fornecedores", command=lambda: exibir_tabela("fornecedores"))
btn_fornecedores.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_produtos = ttk.Button(root, text="Produtos", command=lambda: exibir_tabela("produtos"))
btn_produtos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_vendas = ttk.Button(root, text="Vendas", command=lambda: exibir_tabela("vendas"))
btn_vendas.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_pedidos = ttk.Button(root, text="Pedidos", command=lambda: exibir_tabela("pedidos"))
btn_pedidos.pack(pady=5, padx=10, ipadx=10, ipady=5)

btn_itens_pedido = ttk.Button(root, text="Itens Pedido", command=lambda: exibir_tabela("itens_pedido"))
btn_itens_pedido.pack(pady=5, padx=10, ipadx=10, ipady=5)

# Loop principal da aplicação
root.mainloop()
