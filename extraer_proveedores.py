import psycopg2  # Importa el módulo psycopg2 para interactuar con PostgreSQL
import pandas as pd  # Importa pandas para la manipulación y análisis de datos
from unidecode import unidecode  # Importa unidecode para eliminar caracteres especiales

# Conexión a la base de datos
# Aquí se especifican los parámetros para conectarse a la base de datos PostgreSQL
conexion = psycopg2.connect(
    host="localhost",          # Dirección del servidor de la base de datos
    database="bd_python_excel",  # Nombre de la base de datos
    user="fernando_tm",        # Usuario de la base de datos
    password="nueva_12345"     # Contraseña del usuario
)

# Crear un cursor
# El cursor se usa para ejecutar comandos SQL en la base de datos
cursor = conexion.cursor()

# Ejecutar la consulta para obtener los primeros 20 registros
# Definimos la consulta SQL para seleccionar los campos id, contacto_comercial, email y telefono de la tabla proveedores
# Ordenamos por el campo id y limitamos la salida a los primeros 20 registros
query = """
SELECT id, proveedor, telefono, email
FROM proveedores
ORDER BY id
LIMIT 3;
"""
cursor.execute(query)  # Ejecuta la consulta SQL usando el cursor
result = cursor.fetchall()  # Recupera todos los resultados de la consulta ejecutada

# Convertir los resultados a un DataFrame de pandas
# Se convierte la lista de resultados en un DataFrame de pandas para facilitar su manipulación y exportación
df = pd.DataFrame(result, columns=['ID', 'saldo_pendiente', 'email', 'telefono'])

# Guardar el DataFrame en un archivo Excel
# Se guarda el DataFrame en un archivo Excel llamado proveedores_top_20.xlsx
# index=False significa que no se guardará el índice del DataFrame en el archivo Excel
df.to_excel('proveedores_extraidos_5.xlsx', index=False)

# Cerrar la conexión
# Se cierra el cursor y la conexión a la base de datos para liberar recursos
cursor.close()
conexion.close()
