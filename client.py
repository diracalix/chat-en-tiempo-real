import socket
import threading

username = input("Ingrese nombre de usuario: ")

host = '127.0.0.1'
port = 55555

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

def receive_message():
    while True:
        try:
            message = cliente.recv(1024).decode("utf-8")
            if message == "@username":
                cliente.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Ha ocurrido un error")
            cliente.close()
            break

def write_messages():
    while True:
        message = f"{username}: {input('')}"
        cliente.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_messages_thread = threading.Thread(target=write_messages)
write_messages_thread.start()



