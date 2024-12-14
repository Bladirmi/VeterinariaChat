# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector
from mysql.connector.errors import Error


def connectionBD():
    try:
        # connection = mysql.connector.connect(
        connection = mysql.connector.connect(
            host="sql300.infinityfree.com",
            user="if0_37830820",
            passwd="dkqbZNavwn",
            database="if0_37830820_sistemaveterinaria"
            # auth_plugin='mysql_native_password',
            # charset='utf8mb4',
            # collation='utf8mb4_unicode_ci'
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection
    except mysql.connector.Error as e:
        print(f"Error al conectar a la BD: {e}")
        return None
