import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Conexão com o banco de dados usando SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost/techinnovate-solutions')

# Query SQL para selecionar todas as vendas
query = "SELECT * FROM Vendas"

# Carregando dados do banco de dados
dados = pd.read_sql(query, engine)

# Fechando a conexão
engine.dispose()

# Engenharia de características
dados['data_venda'] = pd.to_datetime(dados['data_venda'])
dados['dia_da_semana'] = dados['data_venda'].dt.dayofweek
dados['mes'] = dados['data_venda'].dt.month
dados['ano'] = dados['data_venda'].dt.year

# Definindo características e alvo
X = dados[['dia_da_semana', 'mes', 'ano', 'produto_id']]
y = dados['quantidade']

# Dividindo em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Fazendo previsões
rf_y_pred = modelo_rf.predict(X_test)

# Avaliando o modelo
print("Erro Médio Absoluto (Random Forest):", mean_absolute_error(y_test, rf_y_pred))
print("Erro Médio Quadrático (Random Forest):", mean_squared_error(y_test, rf_y_pred))
print("R2 Score (Random Forest):", r2_score(y_test, rf_y_pred))

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
print("Melhores parâmetros encontrados:", best_params)

modelo_rf_otimizado = RandomForestRegressor(**best_params, random_state=42)
modelo_rf_otimizado.fit(X_train, y_train)

rf_y_pred_otimizado = modelo_rf_otimizado.predict(X_test)

print("Erro Médio Absoluto (Random Forest Otimizado):", mean_absolute_error(y_test, rf_y_pred_otimizado))
print("Erro Médio Quadrático (Random Forest Otimizado):", mean_squared_error(y_test, rf_y_pred_otimizado))
print("R2 Score (Random Forest Otimizado):", r2_score(y_test, rf_y_pred_otimizado))

# Prevendo a demanda futura para um produto diferente 
produto_id_desejado = 2                                                        #***------___________ ( TROCANDO ITEM/PRODUTO ) ___________------***

futuro = pd.DataFrame({
    'dia_da_semana': [1, 2, 3, 4, 5, 6, 7],
    'mes': [6]*7,
    'ano': [2024]*7,
    'produto_id': [produto_id_desejado]*7
})

demanda_futura = modelo_rf_otimizado.predict(futuro)
print(f"\nPrevisão de demanda futura para o produto {produto_id_desejado} em junho de 2024:")
for dia, demanda in zip(futuro['dia_da_semana'], demanda_futura):
    print(f"Dia da semana {dia}: {demanda:.2f} unidades")

# Sugestões para gerenciamento de inventário
media_demanda = demanda_futura.mean()
print(f"\nMédia da demanda prevista: {media_demanda:.2f} unidades por dia")
sugestao_estoque = media_demanda * 7  # Supondo uma semana de estoque de segurança
print(f"Estoque sugerido para uma semana: {sugestao_estoque:.2f} unidades")
