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