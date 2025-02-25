import psycopg2
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

# Configuración del correo electrónico
remitente = "trianafernando7@gmail.com"
destinatarios = ["fernandotrianam337@gmail.com", "jonfertri357@gmail.com"]  # Lista de destinatarios
asunto = "Archivo Excel - Proveedores"
cuerpo = "Adjunto encontrarás el archivo Excel con los registros de proveedores."

# Ruta del archivo Excel
archivo_adjunto = '/home/fernando/nuevas_pruebas/base_datos_python_excel/proveedores.xlsx'

# Crear la conexión a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="bd_python_excel",
    user="fernando_tm",
    password="nueva_12345"
)

# Crear un cursor
cursor = conexion.cursor()

# Ejecutar la consulta
query = """
SELECT id, contacto_comercial, email, telefono, saldo_pendiente, fecha_ultima_compra
FROM proveedores
ORDER BY id ASC
LIMIT 5;
"""
cursor.execute(query)
result = cursor.fetchall()

# Convertir los resultados a un DataFrame de pandas
df = pd.DataFrame(result, columns=['ID', 'Contacto_comercial', 'Email', 'Telefono', 'Saldo_pendiente', 'Fecha_ultima_compra'])

# Guardar el DataFrame en un archivo Excel
df.to_excel(archivo_adjunto, index=False)

# Cerrar la conexión
cursor.close()
conexion.close()

# Crear el mensaje de correo electrónico
mensaje = MIMEMultipart()
mensaje['From'] = remitente
mensaje['To'] = ", ".join(destinatarios)  # Convertir la lista de destinatarios en una cadena separada por comas
mensaje['Subject'] = asunto
mensaje.attach(MIMEText(cuerpo, 'plain'))

# Adjuntar el archivo
parte_adjunto = MIMEBase('application', 'octet-stream')
with open(archivo_adjunto, 'rb') as archivo:
    parte_adjunto.set_payload(archivo.read())
encoders.encode_base64(parte_adjunto)
parte_adjunto.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(archivo_adjunto)}')
mensaje.attach(parte_adjunto)

# Configuración del servidor SMTP
servidor_smtp = "smtp.gmail.com"
puerto_smtp = 587
usuario_smtp = "trianafernando7@gmail.com"
contraseña_smtp = "jrnh qoaw lgom zcvi"

# Enviar el correo
try:
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()
    servidor.login(usuario_smtp, contraseña_smtp)
    servidor.sendmail(remitente, destinatarios, mensaje.as_string())
    servidor.quit()
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
