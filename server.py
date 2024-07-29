import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Servidor en línea {host}:{port}")

clientes = []  # Almacenamos las conexiones de los clientes
userNames = []  # Almacenamos los usernames

def broadcast(message, _cliente):  # Enviar el mensaje a todos los clientes
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(message)  # Menos al que envió el mensaje

def handle_messages(cliente):
    while True:
        try:
            message = cliente.recv(1024)  # El peso máximo que leerá el mensaje 1024 bits
            broadcast(message, cliente)
        except:
            index = clientes.index(cliente)
            userName = userNames[index]
            broadcast(f"ChatgptTrucho: {userName} desconectado".encode('utf-8'), cliente)
            clientes.remove(cliente)
            userNames.remove(userName)
            cliente.close()
            break

def receive_connections():  # Con esta función el servidor podrá aceptar y manejar las conexiones
    while True:
        cliente, address = server.accept()  # Retorna objeto de la conexión del cliente y dirección IP y puerto
        
        cliente.send("@username".encode("utf-8"))
        userName = cliente.recv(1024).decode("utf-8")  # Cambié 2024 por 1024 para ser consistente con el tamaño de buffer

        clientes.append(cliente)
        userNames.append(userName)

        print(f"{userName} está conectado con esta dirección {str(address)}")
        message = f"chatgptTrucho: {userName} se ha unido al chat".encode("utf-8")
        broadcast(message, cliente)
        cliente.send("Conectado al servidor".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(cliente,))
        thread.start()

receive_connections()
