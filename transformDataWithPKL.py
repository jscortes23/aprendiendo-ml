# -*- coding: utf-8 -*-
"""
    Organizar con el modelo PKL
"""
import pandas as pd
import re
import pickle

# Función para normalizar las abreviaturas en la dirección
def normalizar_abreviaturas(direccion, modelo):
    df = pd.read_csv('csv/dataset_abreviaturas.csv')
    palabras = direccion.lower().split()
    palabras_normalizadas = []
    
    for palabra in palabras:
        # Intentar predecir si la palabra es una abreviatura que necesita normalización
        if any(re.findall(r'\b' + palabra + r'\b', ' '.join(df['forma_incorrecta']))):
            palabra_normalizada = modelo.predict([palabra])[0]
        else:
            palabra_normalizada = palabra
        
        palabras_normalizadas.append(palabra_normalizada.upper())
    
    return ' '.join(palabras_normalizadas)

# Cargar el modelo entrenado
with open('modelo_abreviaturas_rf.pkl', 'rb') as file:
    modelo = pickle.load(file)

# Ejemplo de dirección
direccion = "TRANSVERSAL 12 # 52 - 42 torre a Apartamento 201"
direccion_normalizada = normalizar_abreviaturas(direccion, modelo)
print(direccion_normalizada)