# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 01:21:04 2024

@author: Usuario
"""

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def leer_y_limpieza_csv(file_path):
    """
    Lee un archivo CSV, limpia los datos y devuelve un DataFrame.
    """
    try:
        # Intentar leer el archivo CSV con diferentes codificaciones
        for encoding in ['utf-8', 'latin1', 'ISO-8859-1']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f'Archivo CSV leído exitosamente con codificación {encoding}')
                return df
            except (UnicodeDecodeError, pd.errors.ParserError) as e:
                print(f'Error con codificación {encoding}: {e}')
        raise ValueError('No se pudo leer el archivo CSV con las codificaciones intentadas.')
    except Exception as e:
        print(f'Error al leer y limpiar el archivo CSV: {e}')
        return None

def aplicar_clustering(df, n_clusters=3):
    """
    Aplica K-Means clustering al DataFrame.
    """
    try:
        # Seleccionar características para clustering
        X = df[['edad', 'ingreso', 'gasto']]
        
        # Aplicar K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
        df['cluster'] = kmeans.labels_

        print('Clustering realizado exitosamente.')
        return df
    except Exception as e:
        print(f'Error durante la aplicación del clustering: {e}')
        return None

def visualizar_clusters(df):
    """
    Visualiza los resultados del clustering.
    """
    try:
        # Visualizar los clusters con un gráfico de dispersión
        plt.figure(figsize=(10, 6))
        plt.scatter(df['edad'], df['ingreso'], c=df['cluster'], cmap='viridis', s=50, alpha=0.7)
        plt.xlabel('Edad')
        plt.ylabel('Ingreso')
        plt.title('Segmentación de Clientes - Gráfico de Dispersión')
        plt.colorbar(label='Cluster')
        plt.show()

        # Visualización adicional: Matriz de dispersión (pairplot)
        df_pairplot = df[['edad', 'ingreso', 'gasto', 'cluster']]
        sns.pairplot(df_pairplot, hue='cluster', palette='viridis', markers=["o", "s", "D"])
        plt.suptitle('Matriz de Dispersión con Clustering', y=1.02)
        plt.show()

        print('Visualización de clusters completada.')
    except Exception as e:
        print(f'Error durante la visualización de clusters: {e}')

def main(csv_file_path):
    """
    Función principal para leer datos, aplicar clustering y visualizar resultados.
    """
    # Leer y limpiar datos del archivo CSV
    df = leer_y_limpieza_csv(csv_file_path)
    if df is not None:
        # Aplicar clustering
        df_clustered = aplicar_clustering(df, n_clusters=3)
        if df_clustered is not None:
            # Visualizar los clusters
            visualizar_clusters(df_clustered)

# Ruta del archivo CSV
csv_file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\csv_xml_generado.CSV'

# Ejecutar el proceso principal
#main(csv_file_path)


