import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Carregando o conjunto de dados
df = pd.read_csv('seu_arquivo.csv')

X = df.drop('target', axis=1)
y = df['target']

# Dividindo o conjunto de dados em treinamento e teste
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

# Treinando o modelo otimizado
modelo_rf_otimizado = RandomForestRegressor(**best_params, random_state=42)
modelo_rf_otimizado.fit(X_train, y_train)

# Fazendo previsões com o modelo otimizado
rf_y_pred_otimizado = modelo_rf_otimizado.predict(X_test)

# Avaliando o modelo otimizado
print("Erro Médio Absoluto (Random Forest Otimizado):", mean_absolute_error(y_test, rf_y_pred_otimizado))
print("Erro Médio Quadrático (Random Forest Otimizado):", mean_squared_error(y_test, rf_y_pred_otimizado))
print("R2 Score (Random Forest Otimizado):", r2_score(y_test, rf_y_pred_otimizado))
