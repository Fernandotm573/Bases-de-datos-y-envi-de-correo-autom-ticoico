import psycopg2  # Importa el módulo psycopg2 para interactuar con PostgreSQL
import pandas as pd  # Importa pandas para la manipulación y análisis de datos
import os  # Importa el módulo os para interactuar con el sistema operativo
import re  # Importa el módulo re para trabajar con expresiones regulares
from unidecode import unidecode  # Importa unidecode para eliminar caracteres especiales

# Ruta del archivo CSV
ruta_csv = '/home/fernando/nuevas_pruebas/base_datos_python_excel/Listado_proveedores.csv'

# Verificar si el archivo existe
if not os.path.exists(ruta_csv):
    print(f"El archivo no se encuentra en la ruta especificada: {ruta_csv}")
    exit(1)

# Leer datos desde el archivo CSV con codificación adecuada
df = pd.read_csv(ruta_csv, encoding='latin1')  # Lee el archivo CSV utilizando la codificación 'latin1'

# Imprime las columnas del DataFrame antes de renombrar
print("Columnas antes de renombrar:", df.columns)

# Función para limpiar los nombres de las columnas
def limpiar_nombre_columna(col):
    col = unidecode(col)  # Elimina caracteres especiales
    col = re.sub(r'[^A-Za-z0-9\s]', '', col)  # Elimina caracteres no alfanuméricos excepto espacios
    col = col.strip()  # Elimina espacios adicionales al inicio y al final
    col = col.replace(' ', '_')  # Reemplaza espacios por guiones bajos
    col = col.lower()  # Convierte todo el nombre de la columna a minúsculas
    return col

# Renombrar columnas utilizando la función de limpieza
df.columns = [limpiar_nombre_columna(col) for col in df.columns]

# Imprime las columnas del DataFrame después de renombrar
print("Columnas después de renombrar:", df.columns)

# Corregir manualmente los nombres de las columnas
nombres_correctos = {
    'teli_12fono': 'telefono',
    '_saldo_pendiente_': 'saldo_pendiente',
    'fecha_de_i_12ltima_compra': 'fecha_de_ultima_compra'
}

# Aplica la corrección manual
df.rename(columns=nombres_correctos, inplace=True)

# Imprime las columnas del DataFrame después de la corrección manual
print("Columnas después de la corrección manual:", df.columns)

# Limpiar los datos en la columna 'saldo_pendiente'
def limpiar_valor(x):
    try:
        return float(str(x).replace('�', '').strip())
    except ValueError:
        return 0  # Valor predeterminado en caso de error de conversión

# Verificar si la columna 'saldo_pendiente' existe en el DataFrame
if 'saldo_pendiente' in df.columns:
    df['saldo_pendiente'] = df['saldo_pendiente'].apply(limpiar_valor)
else:
    print("Error: La columna 'saldo_pendiente' no se encontró en el DataFrame después del renombrado.")
    exit(1)

# Configuración de la conexión
conexion = psycopg2.connect(
    host="localhost",          # Dirección del servidor de la base de datos
    database="bd_python_excel",  # Nombre de la base de datos
    user="fernando_tm",        # Usuario de la base de datos
    password="nueva_12345"     # Contraseña del usuario
)

# Crear un cursor
cursor = conexion.cursor()  # Crea un cursor para ejecutar comandos SQL en la base de datos

# Verificar si todas las columnas necesarias están presentes
columnas_necesarias = ['id', 'contacto_comercial', 'email', 'telefono', 'saldo_pendiente', 'fecha_de_ultima_compra']
for columna in columnas_necesarias:
    if columna not in df.columns:
        print(f"Error: La columna '{columna}' no está presente en el DataFrame.")
        exit(1)

# Iterar sobre las filas del DataFrame e insertar los datos en la tabla
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO proveedores (id, contacto_comercial, email, telefono, saldo_pendiente, fecha_ultima_compra)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            contacto_comercial = EXCLUDED.contacto_comercial,
            email = EXCLUDED.email,
            telefono = EXCLUDED.telefono,
            saldo_pendiente = EXCLUDED.saldo_pendiente,
            fecha_ultima_compra = EXCLUDED.fecha_ultima_compra
    """, (
        row['id'], 
        row['contacto_comercial'], 
        row['email'], 
        row['telefono'],  
        row['saldo_pendiente'],  
        row['fecha_de_ultima_compra']  
    ))

# Confirmar los cambios
conexion.commit()  # Confirma los cambios en la base de datos

# Cerrar la conexión
cursor.close()  # Cierra el cursor
conexion.close()  # Cierra la conexión a la base de datos
