X = dados[['dia_da_semana', 'mes', 'ano', 'quantidade_x']]
y = dados['quantidade_y']

X.columns = ['dia_da_semana', 'mes', 'ano', 'quantidade_estoque']
y.name = 'quantidade_vendida'

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
