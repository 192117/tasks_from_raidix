from socket import *
from threading import Thread

host = '127.0.0.1'
port = 8000
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((host, port))

def read():
    try:
        while True:
            message = sock.recv(1024).decode()
            print('{}'.format(message))
    except:
        print('Connection error')
        sock.close()

def main():
    thread_read = Thread(target=read)
    thread_read.start()

    try:
        while True:
            message = input()
            sock.send(message.encode())
    except EOFError:
        pass
    finally:
        sock.close()


if __name__ == '__main__':
    main()