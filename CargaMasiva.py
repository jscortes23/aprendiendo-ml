import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Nombre de la base de datos
database_name = 'data_lake'

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': database_name
}

# https://thedataschools.com/python/mysql-create-database/
# Función para crear la base de datos si no existe
def create_database(cursor, database_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")

# https://thedataschools.com/python/mysql-create-table/
# Función para crear una tabla si no existe
def create_table_if_not_exists(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        direccion TEXT,
        patron VARCHAR(20)
    )
    """
    try:
        cursor.execute(create_table_query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(f"La tabla {table_name} ya existe.")
        else:
            print(err.msg)
            
# https://thedataschools.com/python/mysql-insert-into/
# Función para insertar registros en la tabla correspondiente
def insert_into_table(cursor, table_name, data):
    insert_query = f"INSERT INTO {table_name} (direccion, patron) VALUES (%s, %s)"
    try:
        cursor.execute(insert_query, data)
    except mysql.connector.Error as err:
        print(err.msg)


##########  LLAMADO DE LAS FUNCIONES    ############

# Ruta del archivo CSV ya aplicado el proceso de clusters
csv_file_path = 'csv/clasificado_ml.csv'

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
# Lectura del archivo CSV
df = pd.read_csv(csv_file_path, header=None, names=['direccion', 'Patron'])

# https://thedataschools.com/python/mysql/
# Conexión a la base de datos
conn = mysql.connector.connect(
    user=config['user'], 
    password=config['password'], 
    host=config['host']
    )

cursor = conn.cursor()

# Creación de la base de datos si no existe y selección de la base de datos
create_database(cursor, database_name)

# Procesamiento de cada registro del CSV
# https://www.w3schools.com/python/pandas/ref_df_iterrows.asp
# Derechos reservados de CHAT-GPT

table_name = "comuna_17"
create_table_if_not_exists(cursor, table_name)

for _, row in df.iterrows():
    # Asegurarse de que data es una tupla con un único elemento, SIN LA COMA DA ERROR
    data = (row['direccion'], row['Patron'],)
    insert_into_table(cursor, table_name, data)

# Derechos reservados de CHAT-GPT
# Confirmar cambios y cerrar conexión
conn.commit()
cursor.close()
conn.close()

print("Carga de datos completada.")
