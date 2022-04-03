import socket


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, message_send):
        with socket.create_connection((self.host, self.port)) as sock:
            try:
                sock.sendall(message_send.encode("utf-8"))
                answer = sock.recv(1024).decode("utf-8")
            except socket.error:
                raise ClientError
            return answer

    def con(self, nickname):
        data = "connect-{}".format(nickname)
        answer = self.connect(data)
        print('answer ', answer)

    def dis(self, nickname):
        data = "disconnect-{}".format(nickname)
        answer = self.connect(data)
        print('answer ', answer)

    def send(self, recipient, message):
        data = "send-{}-{}".format(recipient, message)
        answer = self.connect(data)
        print('answer ', answer)