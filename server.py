import asyncio


class ServerProtocol(asyncio.Protocol):

    def __init__(self, clients):
        self.user = None
        self.clients = clients

    def connection_made(self, transport):
        ''' Подключение к серверу. '''
        self.clients += [transport]
        self.peername  = transport.get_extra_info('socket').getpeername()
        self.transport = transport

    def connection_lost(self, exc):
        ''' Отключение от сервера. '''
        if isinstance(exc, ConnectionResetError):
            self.clients.remove(self.transport)
        else:
            print(exc)
        message = '{} disconnected'.format(self.peername)
        for client in self.clients:
            self.transport.sendto(message.encode(), client)


    def data_received(self, data):
        ''' Обработка сообщений от клиента. '''
        if data:
            if not self.user:
                data_user = data.decode()
                if data_user.isalnum():
                    self.user = data_user
                    message = '{} connected to us.'.format(self.user)
                    for client in self.clients:
                        self.transport.sendto(message.encode(), client)
                else:
                    message = 'Your nickname must contain only letters and numbers, at least one character.'
                    self.transport.write(message.encode())
                    self.transport.close()
            else:
                message_user = data.decode()
                message = '{} send: {}'.format(self.user, message_user)
                for client in self.clients:
                    self.transport.sendto(message.encode(), client)
        else:
            message = 'Sorry! You sent nothing.'
            self.transport.write(message.encode())


def run_server():
    clients = []
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda:
        ServerProtocol(clients),
        '127.0.0.1', 8000
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()