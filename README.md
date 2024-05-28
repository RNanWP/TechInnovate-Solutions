<h1 align="center"> TechInnovate Solutions - Previsão de Demanda e Gerenciamento de Dados </h1>
Tecnologia da Informação

<h2>Visão Geral do Projeto</h2>

Este projeto tem como objetivo fornecer uma solução para previsão de demanda de produtos e gerenciamento de dados de uma empresa. Utilizamos técnicas de aprendizado de máquina, especificamente o algoritmo Random Forest, para prever a demanda futura de produtos com base em dados históricos de vendas. Além disso, oferecemos uma interface gráfica para visualização e gerenciamento de tabelas do banco de dados.


<h2>Escopo do Projeto</h2>

O projeto abrange as seguintes funcionalidades:

Previsão de Demanda: Utiliza dados históricos de vendas para prever a demanda futura de produtos específicos.
Gerenciamento de Dados: Gera dados aleatórios para pedidos e itens de pedido e exibe dados de várias tabelas do banco de dados através de uma interface gráfica.


<h2>Plano de Negócios</h2>

O plano de negócios para este projeto envolve a criação de um sistema que permite:

Previsão precisa da demanda de produtos para otimização do estoque.
Integração com um banco de dados para gerenciar informações de clientes, produtos, vendas, pedidos e itens de pedido.
Interface amigável para visualização e gerenciamento de dados.

<h2>Descrição das Disciplinas Envolvidas</h2>

Aprendizado de Máquina (Algoritmos de ML): Implementação de um modelo de Random Forest para previsão de demanda.
Ciência de Dados (Python e Estatística)
Modelagem de Dados
Engenharia de Dados: Extração, transformação e carregamento (ETL) de dados para análise e previsão.
Redes de Computadores
Desenvolvimento de Software: Criação de scripts Python para previsão de demanda e geração de dados aleatórios.
Desenvolvimento de Interface Gráfica: Uso da biblioteca Tkinter para criar uma interface gráfica para visualização e gerenciamento de dados.
Segurança da Informação

<h2>Tecnologias Utilizadas</h2>
Linguagem de Programação: Python
Bibliotecas de Machine Learning: Scikit-learn, Pandas, Numpy
Bibliotecas para Manipulação de Dados: Pandas, SQLAlchemy
Banco de Dados: MySQL
Interface Gráfica: Tkinter
Gerador de Dados Falsos: Faker

<h2>Configuração do Ambiente de Desenvolvimento</h2>
Instalação de Dependências:

Python 3.x
Bibliotecas Python (instaláveis via pip):
pip install pandas numpy scikit-learn sqlalchemy mysql-connector-python faker tk

<h3>Configuração do Banco de Dados:</h3>
Certifique-se de ter um servidor MySQL em execução.
Crie um banco de dados chamado techinnovate-solutions e configure as tabelas conforme necessário.

<h3>Configuração do Arquivo de Conexão:</h3>
Configure a string de conexão do SQLAlchemy para o seu banco de dados MySQL:
engine = create_engine('mysql+mysqlconnector://<root>:<root>@<localhost>/<techinnovate-solutionsnome>')

<h2>Execução do Projeto</h2>

<h3>Previsão de Demanda:</h3>
Execute o script para treinar o modelo de previsão e obter previsões futuras:
python previsao_demanda.py

<h3>Geração de Dados Aleatórios e Interface Gráfica:</h3>
Execute o script para gerar dados aleatórios e abrir a interface gráfica:
python geracao_dados_interface.py

<h2>Instruções de Uso</h2>

<h3>Previsão de Demanda:</h3>
Execute o script previsao_demanda.py para treinar o modelo e realizar previsões de demanda.
O script exibirá as previsões de demanda futura para o produto desejado e sugerirá o estoque necessário para uma semana.

<h3>Geração de Dados Aleatórios e Interface Gráfica:</h3>
Execute o script geracao_dados_interface.py para gerar dados aleatórios de pedidos e itens de pedido.
A interface gráfica permitirá visualizar as tabelas clientes, estoque, fornecedores, produtos, vendas, pedidos e itens_pedido.

<h1>Contato</h1>
Para mais informações, entre em contato:

Email: suporte@techinnovate.com
Email: renan92011@hotmail.com
Telefone: +55 11 968180410
Obrigado por utilizar a solução TechInnovate!

# Autores

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/111291880?s=400&u=f42178536c3b43cac91e3fb58665566bd58115b7&v=4" width=115><br><sub>Renan Oliveira</sub>](https://github.com/RNanWP) |
| :---: | :---: | :---: |