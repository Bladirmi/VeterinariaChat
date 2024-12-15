# Importando Libreria mysql.connector para conectar Python con MySQL
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector.errors import Error

load_dotenv()

# Cargar variables del archivo .env

def connectionBD():
    try:
        # Obtén las credenciales desde las variables de entorno
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection
    except mysql.connector.Error as e:
        print(f"Error al conectar a la BD: {e}")
        return None
    finally:
        # Asegúrate de cerrar la conexión si es exitosa
        if connection and connection.is_connected():
            connection.close()
