"""
    Crear modelo PKL para entrenar
"""

import pandas as pd

# # Dataset de ejemplo con abreviaturas y sus normalizaciones
# data = {
#     'forma_incorrecta': ['carrera', 'carrera', 'calle', 'avenida', 'torre', 'apartamento','transversal','diagonal','aveni' ,'aveni'],
#     'forma_correcta': ['KR', 'KR', 'CL', 'AV', 'TO', 'AP','TV','DG','AV' ,'AV']
# }

# # Convertir el diccionario en un DataFrame
# df = pd.DataFrame(data)

# # Guardar el dataset para futuras referencias
# df.to_csv('dataset_abreviaturas.csv', index=False)


#################

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Cargar el dataset (Se le pasa las abreviaturas)
df = pd.read_csv('csv/dataset_abreviaturas.csv')

# División del dataset en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(df['forma_incorrecta'], df['forma_correcta'], test_size=0.2, random_state=42)

# Pipeline para vectorizar el texto y aplicar un modelo Random Forest
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Entrenamiento del modelo
pipeline.fit(X_train, y_train)

# Evaluación del modelo
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Precisión del modelo: {accuracy * 100:.2f}%')
print(classification_report(y_test, y_pred))

# Guardar el modelo entrenado en un archivo .pkl
with open('modelo_abreviaturas_rf.pkl', 'wb') as file:
    pickle.dump(pipeline, file)

