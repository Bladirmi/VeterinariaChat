import os
from dotenv import load_dotenv
from flask import Flask, render_template
# Importando las clases SocketIO y emit del módulo flask_socketio
from flask_socketio import SocketIO, emit
from .confiBD.conexionBD import connectionBD
from funciones import *  # Importando mis Funciones

load_dotenv()

app = Flask(__name__)

# para crear una instancia de Socket.IO en una aplicación Flask
socketio = SocketIO(app)


# Escuchando si el servidor esta conectado del lado del servidor
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


# Escuchando si el cliente se desconecta del lado del servidor
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')


# Definiendo mi ruta de Inicio
@app.route('/')
def index():
    """ **CAMBIO REALIZADO AQUÍ**
    Ahora usamos `connectionBD` para conectarnos a la base de datos
    y obtener los mensajes almacenados.
    """
    conexion = connectionBD()
    if not conexion:
        return "Error al conectar a la base de datos", 500

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mensajes")  # **Consulta para obtener mensajes**
        lista_mensajes = cursor.fetchall()
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        lista_mensajes = []
    finally:
        conexion.close()  # **Cerramos la conexión después de usarla**

    return render_template('public/inicio.html', lista_mensajes=lista_mensajes)


''' 
La función recibirMsj se encarga de escuchar el evento "message"
en el lado del servidor y mostrar el mensaje recibido en la consola del servidor.
'''


@socketio.on('mensaje_chat')
def recibir_mensaje(mensaje_chat):
    """ **CAMBIO REALIZADO AQUÍ**
    Ahora guardamos los mensajes recibidos en la base de datos.
    """
    conexion = connectionBD()
    if not conexion:
        emit('error', {'message': 'Error al conectar a la base de datos'}, broadcast=True)
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO mensajes (mensaje) VALUES (%s)", (mensaje_chat,))  # **Insertamos mensaje**
        conexion.commit()
    except Exception as e:
        print(f"Error al insertar mensaje: {e}")
    finally:
        conexion.close()  # **Cerramos la conexión después de usarla**

    # **Emitimos el mensaje al cliente después de guardarlo**
    emit('mensaje_chat', mensaje_chat, broadcast=True)


# Arrancando aplicacion Flask
if __name__ == '__main__':
    """ 
    se llama a la función socketio.run() para iniciar el servidor de Flask-SocketIO.
    Esto significa que cuando ejecutes este archivo específico, el servidor Flask-SocketIO 
    se iniciará y estará listo para recibir conexiones y manejar eventos de socket
    """
    port = int(os.environ.get('PORT', 5100))
    socketio.run(app, debug=True, port=port)
