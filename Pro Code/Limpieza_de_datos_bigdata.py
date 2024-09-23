# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:52:13 2024

@author: Usuario
"""

import pandas as pd

def generar_informe_columnas(csv_file_path):
    """
    Lee un archivo CSV y genera un informe con información detallada sobre las columnas del archivo.
    
    Args:
        csv_file_path (str): La ruta del archivo CSV.
    
    Returns:
        str: Informe con información sobre las columnas.
    """
    try:
        # Intentar leer el archivo CSV con diferentes codificaciones
        for encoding in ['utf-8', 'latin1', 'ISO-8859-1']:
            try:
                df = pd.read_csv(csv_file_path, encoding=encoding)
                print(f'Archivo CSV leído exitosamente con codificación {encoding}')
                break
            except (UnicodeDecodeError, pd.errors.ParserError) as e:
                print(f'Error con codificación {encoding}: {e}')
        else:
            raise ValueError('No se pudo leer el archivo CSV con las codificaciones intentadas.')
        
        # Generar informe
        informe = []
        informe.append("Informe de Columnas del Archivo CSV")
        informe.append("=" * 50)
        informe.append(f"Ruta del archivo: {csv_file_path}")
        informe.append(f"Número de columnas: {len(df.columns)}")
        informe.append(f"Encabezados de las columnas: {list(df.columns)}")
        informe.append("=" * 50)
        
        # Agregar detalles de cada columna
        for col in df.columns:
            informe.append(f"Columna: {col}")
            informe.append(f" - Tipo de datos: {df[col].dtype}")
            informe.append(f" - Valores nulos: {df[col].isnull().sum()}")
            informe.append(f" - Valores únicos: {df[col].nunique()}")
            informe.append(f" - Primeros 5 valores: {df[col].head().tolist()}")
            informe.append("-" * 50)
        
        # Unir el informe en una cadena de texto
        informe_str = "\n".join(informe)
        return informe_str
    
    except Exception as e:
        return f'Error al generar el informe de columnas: {e}'

# Ruta del archivo CSV
csv_file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\SISBEN_base_modificado.csv'

# Generar y mostrar el informe
#informe = generar_informe_columnas(csv_file_path)
#print(informe)


import pandas as pd
import sqlite3
import os

def leer_corregir_y_guardar_csv(file_path, corrected_csv_path, db_path):
    """
    Lee un archivo CSV utilizando diferentes codificaciones, verifica errores comunes,
    guarda el archivo corregido en un nuevo CSV y lo guarda en una base de datos SQLite.
    """
    # Intentar leer el dataset con diferentes codificaciones
    codificaciones = ['utf-8', 'latin1', 'ISO-8859-1']
    df = None
    for codificacion in codificaciones:
        try:
            df = pd.read_csv(file_path, encoding=codificacion)
            print(f"Archivo leído correctamente con codificación: {codificacion}")
            break
        except Exception as e:
            print(f"Error al leer el archivo con codificación {codificacion}: {e}")
    
    if df is None:
        print("Error al leer el archivo CSV con las codificaciones comunes.")
        return

    # Corrección de inconsistencias de codificación de texto
    try:
        df = df.apply(lambda x: x.astype(str).str.encode('utf-8', 'ignore').str.decode('utf-8') if x.dtype == 'object' else x)
        print("Codificación de texto corregida.")
    except Exception as e:
        print(f"Error al corregir la codificación de texto: {e}")

    # Verificación y corrección de datos faltantes y duplicados
    df.fillna('N/A', inplace=True)  # Ejemplo de imputación para valores nulos
    df.drop_duplicates(inplace=True)

    # Guardar DataFrame corregido en un archivo CSV
    try:
        df.to_csv(corrected_csv_path, index=False, encoding='utf-8')
        print(f"Archivo corregido guardado en: {corrected_csv_path}")
    except Exception as e:
        print(f"Error al guardar el archivo CSV corregido: {e}")
    
    # Guardar DataFrame corregido en una base de datos SQLite
    try:
        # Conectar a la base de datos SQLite (se creará si no existe)
        conn = sqlite3.connect(db_path)
        table_name = "datos_corregidos"
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Datos guardados en la base de datos SQLite en la tabla: {table_name}")
        conn.close()
    except Exception as e:
        print(f"Error al guardar los datos en la base de datos: {e}")

# Rutas de los archivos
file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\SISBEN_base.CSV'
corrected_csv_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\SISBEN_base_corregido.CSV'
db_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\SISBEN_base.db'

# Llamar a la función
#leer_corregir_y_guardar_csv(file_path, corrected_csv_path, db_path)

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def realizar_clustering(file_path):
    # Leer el archivo CSV
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"Archivo leído correctamente desde {file_path}")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
        print(f"Archivo leído con codificación latin1 desde {file_path}")

    # Seleccionar características para clustering
    # Asegúrate de que los nombres de las columnas coincidan con los de tu archivo CSV
    columnas_para_clustering = ['edad', 'ingreso', 'gasto']
    if not all(column in df.columns for column in columnas_para_clustering):
        print("Error: No se encontraron todas las columnas necesarias para el clustering en el archivo CSV.")
        return

    # Seleccionar las columnas relevantes
    X = df[columnas_para_clustering]

    # Escalado de datos (opcional pero recomendado para clustering)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Aplicar K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(X_scaled)
    df['cluster'] = kmeans.labels_

    # Visualizar los clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(df['edad'], df['ingreso'], c=df['cluster'], cmap='viridis')
    plt.xlabel('Edad')
    plt.ylabel('Ingreso')
    plt.title('Clustering de Clientes basado en Edad e Ingreso')
    plt.colorbar(label='Cluster')
    plt.show()

    # Visualización alternativa: Edad vs Gasto
    plt.figure(figsize=(8, 6))
    plt.scatter(df['edad'], df['gasto'], c=df['cluster'], cmap='viridis')
    plt.xlabel('Edad')
    plt.ylabel('Gasto')
    plt.title('Clustering de Clientes basado en Edad y Gasto')
    plt.colorbar(label='Cluster')
    plt.show()

# Ruta del archivo CSV
file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\csv_xml_generado.csv'

# Llamar a la función para realizar el clustering y generar gráficos
#realizar_clustering(file_path)

import sqlite3

def generar_informe_columnas(db_path):
    # Conectar a la base de datos SQLite
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"Conectado a la base de datos {db_path}")
        
        # Obtener el nombre de todas las tablas en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("No se encontraron tablas en la base de datos.")
            return
        
        # Iterar sobre cada tabla para obtener los nombres de las columnas
        for table_name in tables:
            table_name = table_name[0]
            print(f"\nTabla: {table_name}")
            
            # Obtener nombres de las columnas para la tabla actual
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            if not columns:
                print(f"No se encontraron columnas en la tabla {table_name}.")
                continue
            
            print("Columnas:")
            for column in columns:
                column_name = column[1]  # El nombre de la columna está en la segunda posición
                print(f"- {column_name}")
    
    except sqlite3.Error as e:
        print(f"Error al conectar o leer la base de datos: {e}")
    
    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            conn.close()
            print("Conexión a la base de datos cerrada.")

# Ruta del archivo de base de datos
db_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\dataset\SISBEN_base.db'

# Llamar a la función para generar el informe
generar_informe_columnas(db_path)

