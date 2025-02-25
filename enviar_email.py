import smtplib  # Importa el módulo smtplib para enviar correos electrónicos
from email.mime.multipart import MIMEMultipart  # Importa MIMEMultipart para crear el contenedor del correo
from email.mime.base import MIMEBase  # Importa MIMEBase para el archivo adjunto
from email.mime.text import MIMEText  # Importa MIMEText para el cuerpo del correo
from email import encoders  # Importa encoders para codificar el archivo adjunto
import os  # Importa os para interactuar con el sistema operativo

# Configuración del correo electrónico
remitente = "trianafernando7@gmail.com"  # Tu dirección de correo
destinatario = "fernandotrianam337@gmail.com", "jonfertri357@gmail.com"  # Dirección de correo del destinatario
#destinatario = "belenchamucero@gmail.com"  # Dirección de correo del destinatario
asunto = "Archivo Excel - proveedores_extraidos_5.xlsx"
cuerpo = "Adjunto encontrarás el archivo Excel con los 5 primeros registros de proveedores."

# Ruta del archivo Excel
archivo_adjunto = '/home/fernando/nuevas_pruebas/base_datos_python_excel/proveedores_extraidos_5.xlsx'

# Verificar si el archivo existe
if not os.path.exists(archivo_adjunto):
    print(f"El archivo no se encuentra en la ruta especificada: {archivo_adjunto}")
    exit(1)

# Crear el objeto del mensaje
mensaje = MIMEMultipart()
mensaje['From'] = remitente
mensaje['To'] = destinatario
mensaje['Subject'] = asunto

# Adjuntar el cuerpo del mensaje
mensaje.attach(MIMEText(cuerpo, 'plain'))

# Adjuntar el archivo
parte_adjunto = MIMEBase('application', 'octet-stream')
with open(archivo_adjunto, 'rb') as archivo:
    parte_adjunto.set_payload(archivo.read())
encoders.encode_base64(parte_adjunto)
parte_adjunto.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(archivo_adjunto)}')
mensaje.attach(parte_adjunto)

# Configuración del servidor SMTP
servidor_smtp = "smtp.gmail.com"  # Dirección del servidor SMTP
puerto_smtp = 587  # Puerto del servidor SMTP
usuario_smtp = "trianafernando7@gmail.com"  # Usuario del servidor SMTP (normalmente es tu dirección de correo)
contraseña_smtp = "jrnh qoaw lgom zcvi"  # Contraseña del servidor SMTP

# Enviar el correo
try:
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()  # Inicia la conexión TLS (si es necesario)
    servidor.login(usuario_smtp, contraseña_smtp)  # Inicia sesión en el servidor SMTP
    servidor.sendmail(remitente, destinatario, mensaje.as_string())  # Envía el correo
    servidor.quit()  # Cierra la conexión con el servidor SMTP
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
