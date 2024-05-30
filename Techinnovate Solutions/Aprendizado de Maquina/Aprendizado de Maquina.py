from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.api import OLS
from sklearn.linear_model import LinearRegression

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

produto_id_desejado = 2  # Alterar conforme necessário

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

# Calculando a média da demanda prevista
media_demanda_prevista = demandas_futuras.mean()
print(f"\nMédia da demanda prevista: {media_demanda_prevista:.2f} unidades por dia")

# Calculando o estoque sugerido para uma semana (supondo uma semana de estoque de segurança)
sugestao_estoque = media_demanda_prevista * 7
print(f"Estoque sugerido para uma semana: {sugestao_estoque:.2f} unidades")

# Gráfico de dispersão
sns.scatterplot(x='dia_da_semana', y=y_test, data=X_test)
plt.title('Dispersão entre dia da semana e quantidade vendida')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade Vendida')
plt.show()

# Identificar padrões
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
