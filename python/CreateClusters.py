"""
    Clasificación de cluster
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Leer el archivo CVS de entrada
data_file = 'entrega_ml.csv'
df = pd.read_csv(data_file)

# Convertir los valores inf a NaN en el DataFrame
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Extraer la columna de direcciones
direcciones = df['direccion'].astype(str)

# Convertir direcciones a vectores TR-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(direcciones)

# Determinar el número óptimo de cluster usando el metodo del codo
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    sse.append(kmeans.inertia_)
    
# Convertir el rango de SEE a DataFrame para asegugar no tener valores
sse_df = pd.DataFrame({'clusters': range(1, 11), 'sse': sse})
sse_df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Graficar el método del codo
plt.figure(figsize=(8,5))
sns.lineplot(x='clusters', y='sse', data=sse_df, marker='o')
plt.title('Método del codo para encontrar el número óptimo de clusters')
plt.xlabel('Número de clustess')
plt.ylabel('SSE')
plt.show()

# Elegir el número óptimo de clusters (por ejemplo, 3)
n_clusters = 15
kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0).fit(X)
df['Patron'] = kmeans.labels_

# Guardar el resultado en un nuevo archivo CSV
output_file = 'clasificado_ml.csv'
df.to_csv(output_file, index=False)

output_file