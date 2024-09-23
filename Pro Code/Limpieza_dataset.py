# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 22:12:48 2024

@author: Usuario
"""
import pandas as pd
import numpy as np
import chardet
import lxml

def detectar_errores_e_inconsistencias(df):
    """
    Detecta errores e inconsistencias en un DataFrame y genera un informe estadístico.
    """
    errores = {}
    
    # Valores faltantes
    valores_faltantes = df.isnull().sum()
    if valores_faltantes.sum() > 0:
        errores['Valores Faltantes'] = valores_faltantes[valores_faltantes > 0].to_dict()

    # Valores duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        errores['Valores Duplicados'] = duplicados

    # Errores de formato
    errores['Errores de Formato'] = {}
    for columna in df.columns:
        if pd.api.types.is_numeric_dtype(df[columna]):
            if df[columna].dtype != np.float64:
                errores['Errores de Formato'][columna] = 'Formato incorrecto'
        elif pd.api.types.is_datetime64_any_dtype(df[columna]):
            try:
                df[columna] = pd.to_datetime(df[columna], errors='coerce')
                if df[columna].isnull().sum() > 0:
                    errores['Errores de Formato'][columna] = 'Fechas incorrectas'
            except:
                errores['Errores de Formato'][columna] = 'Formato incorrecto'

    return errores

def corregir_errores(df, errores):
    """
    Corrige errores e inconsistencias en un DataFrame.
    """
    # Corregir valores faltantes
    for columna, valor in errores.get('Valores Faltantes', {}).items():
        df[columna].fillna(df[columna].mean(), inplace=True) if pd.api.types.is_numeric_dtype(df[columna]) else df[columna].fillna(df[columna].mode()[0], inplace=True)
    
    # Eliminar duplicados
    if 'Valores Duplicados' in errores:
        df.drop_duplicates(inplace=True)
    
    # Corregir formatos
    for columna, error in errores.get('Errores de Formato', {}).items():
        if error == 'Formato incorrecto':
            if pd.api.types.is_numeric_dtype(df[columna]):
                df[columna] = pd.to_numeric(df[columna], errors='coerce')
            elif pd.api.types.is_datetime64_any_dtype(df[columna]):
                df[columna] = pd.to_datetime(df[columna], errors='coerce')

    return df

def generar_informe_estadistico(df):
    """
    Genera un informe estadístico sobre un DataFrame.
    """
    informe = []
    informe.append("Informe Estadístico del Dataset")
    informe.append("="*40)
    informe.append(f"Cantidad de Filas: {df.shape[0]}")
    informe.append(f"Cantidad de Columnas: {df.shape[1]}")
    informe.append("\nResumen Estadístico:")
    informe.append(df.describe(include='all').to_string())
    informe.append("\nEncabezados:")
    informe.append(str(df.columns.tolist()))
    
    return "\n".join(informe)

def generar_informe_correcciones(df_original, df_corregido):
    """
    Genera un informe de las correcciones realizadas en un DataFrame.
    """
    informe = []
    informe.append("Informe de Correcciones Realizadas")
    informe.append("="*40)

    # Comparar antes y después
    diferencia = df_original.compare(df_corregido)
    if diferencia.empty:
        informe.append("No se realizaron correcciones.")
    else:
        informe.append("Correcciones realizadas:")
        informe.append(diferencia.to_string())
    
    return "\n".join(informe)

def leer_csv_con_codificacion(file_path):
    """
    Lee un archivo CSV detectando automáticamente la codificación y prueba diferentes codificaciones si es necesario.
    """
    encodings = ['utf-8', 'latin1', 'ISO-8859-1']
    for encoding in encodings:
        try:
            print(f"Intentando con codificación: {encoding}")
            df = pd.read_csv(file_path, encoding=encoding)
            return df
        except UnicodeDecodeError as e:
            print(f"Error con codificación {encoding}: {e}")
    
    raise ValueError("No se pudo leer el archivo con ninguna de las codificaciones probadas.")

def leer_xml_a_dataframe(xml_file_path, csv_file_path):
    """
    Lee un archivo XML y lo convierte en un DataFrame con la estructura del archivo CSV.
    """
    # Leer el archivo XML
    df_xml = pd.read_xml(xml_file_path)

    # Leer encabezados del archivo CSV para definir estructura
    df_csv = leer_csv_con_codificacion(csv_file_path)
    encabezados_csv = df_csv.columns.tolist()
    
    # Reorganizar columnas del XML para que coincidan con el CSV
    df_xml_reorganizado = df_xml[encabezados_csv]
    
    return df_xml_reorganizado

def main(csv_file_path, xml_file_path, output_csv_path):
    """
    Función principal para procesar y limpiar los datos de archivos CSV y XML.
    """
    print("Leyendo y limpiando datos del archivo CSV...")
    df_csv = leer_csv_con_codificacion(csv_file_path)
    
    print("Leyendo y limpiando datos del archivo XML...")
    try:
        df_xml = leer_xml_a_dataframe(xml_file_path, csv_file_path)
    except ImportError as e:
        print(f"Error al leer XML: {e}")
        return
    
    # Detectar errores en ambos DataFrames
    print("Detectando errores en el archivo CSV...")
    errores_csv = detectar_errores_e_inconsistencias(df_csv)
    print("Detectando errores en el archivo XML...")
    errores_xml = detectar_errores_e_inconsistencias(df_xml)
    
    # Corregir errores en ambos DataFrames
    print("Corrigiendo errores en el archivo CSV...")
    df_csv_corregido = corregir_errores(df_csv, errores_csv)
    print("Corrigiendo errores en el archivo XML...")
    df_xml_corregido = corregir_errores(df_xml, errores_xml)
    
    # Generar informes
    informe_csv = generar_informe_estadistico(df_csv_corregido)
    informe_xml = generar_informe_estadistico(df_xml_corregido)
    informe_correcciones_csv = generar_informe_correcciones(df_csv, df_csv_corregido)
    informe_correcciones_xml = generar_informe_correcciones(df_xml, df_xml_corregido)
    
    print(informe_csv)
    print(informe_xml)
    print(informe_correcciones_csv)
    print(informe_correcciones_xml)
    
    # Unir los DataFrames y guardar el resultado
    df_combinado = pd.concat([df_csv_corregido, df_xml_corregido], ignore_index=True)
    df_combinado.to_csv(output_csv_path, index=False)
    print(f"DataFrame combinado guardado en: {output_csv_path}")

# Usar la función principal con las rutas de archivo correspondientes
csv_file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\SISBEN_base_modificado.CSV'
xml_file_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\registraduria_modificado.xml'
output_csv_path = r'E:\Google Drive 2\SENA 2024\Evidencias Agosto 2024\IA Bootcamp & Hackathon\csv_xml_generado.csv'

main(csv_file_path, xml_file_path, output_csv_path)
