import socket
import threading

sock = socket.create_connection(('127.0.0.1', 8000))

def read():
    global sock
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            print('Connection error')
            sock.close()
            break


def write():
    global sock
    while True:
        message = input()
        sock.send(message.encode())

read_thread = threading.Thread(target=read)
read_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
