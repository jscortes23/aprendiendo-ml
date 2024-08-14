'''
    Script para determinar el numero de clusters
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

# Cargar datos
file_path = 'csv/entrega_ml.csv'
data = pd.read_csv(file_path)

# Convertir a alfanumerico
data['text'] = data.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Convertir el tecto en caractetirticas númericas usando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['text'])

# Definir el rango de cluster a evaluar
start, end = 2, 15 # Cambiar seguin necesidades

# Calcular el Silhoutte Score para diferentes números de clusters
silhoutte_scores = []
for k in range(start, end + 1):
    kmeans = KMeans(n_clusters=k, n_init=15, random_state=0).fit(X)
    score = silhouette_score(X, kmeans.labels_)
    silhoutte_scores.append(score)
    
# Graficar el Silhouette Score
plt.figure(figsize=(8, 5))
sns.lineplot(x=range(start, end + 1), y=silhoutte_scores, markers='o')
plt.title('Silhouette Score para encontrar el número óptimo de clusters')
plt.xlabel('Número de clustres')
plt.ylabel('Silhouette Score')
plt.show()
