# Aprendiendo Machine Learning
Aprender sobre Machine Learning y Inteligencia Artificial 

## Herramientas
* Anaconda
* Spyder

>[!NOTE]
>En el entorno de Syper asegurarse que este apuntando a la carpeta donde estan todos los archivos
>![image](https://github.com/user-attachments/assets/f0773ecd-17fe-4703-8fef-4afcf001ed5c)


## Funcionamiento de los archivos Python
### countClusters.py
Este se encarga de mostrar un grafico del numero de clusters para determinar la coherencia y consistencia de su contendido de cada uno de ellos 

### CreateClusters.py
Este se encarga de crear un archivo CSV con la infomración agrupada por cluster (se puede determinar el numero de cluster a usar, se recomienda un numero maximo de 15)

### normalizacion.py
Este se encarga de organizar la data según patron de comportamiento encontrado en el cluster, pero este se puede mejorar por medio de archivos `.dic` que lee el archivo para mejorar la respuesta

### CargaMasiva.py
Este se encarga de crear una base de datos en MySQL y dentro crea una tabla para cargar todos los datos.

### CreateModelPKL.py
Este se encarga de crear una archivo PKL. Este es un modelo que se usara en el archvo `transformDataWithPKL.py`.

### transformDataWithPKL.py
Este se encarga de organizar la data en base a un modelo que se creo (PKL).
