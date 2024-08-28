import pandas as pd
import re
from IPython.display import display

# Acceder a los diccionarios
transformaciones_frases_df = pd.read_csv('dic/transformaciones_frases.dic')
transformaciones_word_df = pd.read_csv('dic/transformaciones_word.dic')

# Eliminar valores nulos y convertir a cadenas para transformaciones de frases
transformaciones_frases_df = transformaciones_frases_df.dropna()
transformaciones_frases_df.columns = transformaciones_frases_df.columns.str.strip()
transformaciones_frases_df['frases'] = transformaciones_frases_df['frases'].astype(str)
transformaciones_frases_df['abreviatura'] = transformaciones_frases_df['abreviatura'].astype(str)

# Eliminar valores nulos y convertir a cadenas para transformaciones de palabras
transformaciones_word_df = transformaciones_word_df.dropna()
transformaciones_word_df.columns = transformaciones_word_df.columns.str.strip()
transformaciones_word_df['palabra'] = transformaciones_word_df['palabra'].astype(str)
transformaciones_word_df['abreviatura'] = transformaciones_word_df['abreviatura'].astype(str)

# Convertir los DataFrames a diccionarios
transformaciones_frases = dict(zip(transformaciones_frases_df['frases'], transformaciones_frases_df['abreviatura']))
transformaciones_word = dict(zip(transformaciones_word_df['palabra'], transformaciones_word_df['abreviatura']))

# Ordenar las transformaciones por longitud de mayor a menor
transformaciones_frases = dict(sorted(transformaciones_frases.items(), key=lambda item: len(item[0]), reverse=True))
transformaciones_word = dict(sorted(transformaciones_word.items(), key=lambda item: len(item[0]), reverse=True))

# Acceder al cluster
data = pd.read_csv('csv/cluster_01.csv')

def normalizar_direccion(direccion, transformaciones):
    direccion = direccion.upper()
    direccion = re.sub(r'[^A-Z0-9\s\-#]', '', direccion)
    
    #Aplicar transformaciones
    for frase, abreviatura in transformaciones.items():
        direccion = re.sub(r'\b' + re.escape(frase) + r'\b', abreviatura, direccion)
    
    direccion = re.sub(r'\s+', ' ', direccion).strip()
    
    return direccion

def reordenar_direccion(direccion):
    # Primer elemento de configuración. Secuencia a tener en cuenta para ordenar el complemento
    prioridad = {
        'TO': 1,
        'SO': 40,
        'AP': 80,  'LC': 81,  'HB': 82,
        'PQ': 120, 'DP': 121, 'PQSM': 122, 'SOPQ': 123, 'OF': 124, 'CA ': 125
        }
    
    # Buscar los elementos de prioridad con sus valores
    elementos = re.findall(r'\b(TO|AP|LC|HB|SO|PQ|DP|PQSM|SOPQ|OF|CA)\b\s*([A-Z0-9\-]*)', direccion)
    
    # Procesat cada elemento para eliminar guiones si los tiene
    elementos_procesados = [(elem[0], elem[1].replace('-', '_')) for elem in elementos]
    
    # Ordenar los elementos procesados según la prioridad
    elementos_ordenados = sorted(elementos_procesados, key=lambda x: prioridad.get(x[0], 8))
    
    # Eliminar los elementos originales de la dirección
    direccion_reordenada = re.sub(r'\b(TO|AP|LC|HB|SO|PQ|DP|PQSM|SOPQ|OF|CA)\b\s*[A-Z0-9\-]*', '', direccion).strip()
    direccion_reordenada = re.sub(r'\s+', ' ', direccion_reordenada)
    
    # Añade los elementos ordenados al final de la dirección
    for elem in elementos_ordenados:
        direccion_reordenada += f' {elem[0]} {elem[1]}'
        
    # Limpia los espacios adicionales
    direccion_reordenada = re.sub(r'\s+', ' ', direccion_reordenada).strip()
    
    return direccion_reordenada

# Aplicar transformaciones de frases primero y luego palabras
data['direccion_normalizada'] = data['DIRECCION_SNR'].apply(lambda x: normalizar_direccion(x, transformaciones_frases))
data['direccion_normalizada'] = data['direccion_normalizada'].apply(lambda x: normalizar_direccion(x, transformaciones_word))

# Aplicar reordenamiento de dirección
data['direccion_final'] = data['direccion_normalizada'].apply(reordenar_direccion)
