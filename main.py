import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados de treinamento
train_data = pd.read_csv('treino.csv')

# Carregar dados de teste
test_data = pd.read_csv('teste.csv')

# Separar features e target no conjunto de treinamento
X_train = train_data.drop(columns=['id', 'target'])
y_train = train_data['target']

# Separar features no conjunto de teste
X_test = test_data.drop(columns=['id'])

# Criar e treinar o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fazer predições no conjunto de treinamento (para análise)
train_predictions = model.predict(X_train)

# Fazer predições no conjunto de teste
test_predictions = model.predict(X_test)

# Calcular a Medida-F (F1-Score) no conjunto de treinamento
f1_train = f1_score(y_train, train_predictions, average='weighted')
print(f"Medida-F (F1-Score) no conjunto de treinamento: {f1_train:.4f}")

# Calcular a Medida-F (F1-Score) usando validação cruzada no conjunto de treinamento
f1_cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
print(f"Medida-F (F1-Score) em validação cruzada: {f1_cv_scores.mean():.4f}")

# Criar DataFrame para as predições no conjunto de treinamento
train_results = train_data[['id', 'target']].copy()
train_results['resultado_previsto'] = train_predictions

# Criar DataFrame para as predições no conjunto de teste
test_results = test_data[['id']].copy()
test_results['resultado_previsto'] = test_predictions

# Exibir as primeiras 10 linhas do DataFrame de treinamento
print("\nPredições no conjunto de treinamento (10 primeiras linhas):")
print(train_results.head(10))

# Exibir as primeiras 10 linhas do DataFrame de teste
print("\nPredições no conjunto de teste (10 primeiras linhas):")
print(test_results.head(10))

# Criar um DataFrame com a contagem de cada classe
class_counts = test_results['resultado_previsto'].value_counts().sort_index()
class_labels = ['Deserto', 'Vulcânico', 'Oceânico', 'Florestal', 'Gelado']

# Criar o gráfico de barras com Seaborn
plt.figure(figsize=(8, 5))
sns.barplot(x=class_labels, y=class_counts.values, color='royalblue')

# Adicionar rótulos e título
plt.title('Distribuição das Classes Previstas no Conjunto de Teste', fontsize=14, fontweight='bold')
plt.xlabel('Classe do Planeta', fontsize=12)
plt.ylabel('Número de Planetas', fontsize=12)

# Adicionar os valores acima das barras
for i, count in enumerate(class_counts):
    plt.text(i, count + 10, str(count), ha='center', fontsize=10)

# Ajustar o layout
plt.tight_layout()
plt.show()

# Salvar as predições no arquivo CSV
output = pd.DataFrame({'id': test_data['id'], 'target': test_predictions})
output.to_csv('predicoes.csv', index=False)
