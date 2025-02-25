import psycopg2  # Importa el módulo psycopg2 para interactuar con PostgreSQL

# Configuración de la conexión
# Aquí se especifican los parámetros para conectarse a la base de datos PostgreSQL
conexion = psycopg2.connect(
    host="localhost",         # Dirección del servidor de la base de datos
    database="bd_python_excel",  # Nombre de la base de datos
    user="fernando_tm",       # Usuario de la base de datos
    password="nueva_12345"    # Contraseña del usuario
)

# Crear un cursor
# El cursor se usa para ejecutar comandos SQL en la base de datos
cursor = conexion.cursor()

# Ejecutar una consulta
# La consulta SQL se ejecuta usando el cursor
cursor.execute("SELECT * FROM proveedores")

# Obtener los resultados
# Se recuperan todos los resultados de la consulta ejecutada
resultados = cursor.fetchall()

# Imprimir los resultados
# Se recorren los resultados y se imprimen en formato legible
for fila in resultados:
    print(f"ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")

# Cerrar la conexión
# Se cierra el cursor y la conexión a la base de datos
cursor.close()
conexion.close()
