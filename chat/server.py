import asyncio
from datetime import datetime
from chat.chat_logger import create_logger


class ServerProtocol(asyncio.Protocol):

    def __init__(self, clients, logger):
        self.clients = clients
        self.logger = logger
        self.user = None


    def connection_made(self, transport):
        ''' Подключение пользователя. '''
        self.transport = transport
        self.transport.write('Wellcome! Please enter your nickname'.encode())


    def connection_lost(self, exc):
        ''' Отключение пользователя. '''
        if isinstance(exc, ConnectionResetError):
            self.clients.pop(self.user)
        else:
            pass
        message = self.make_message(message=self.user, event='disconnect')
        for client in self.clients:
            if client != self.user:
                self.clients[client].write(message)


    def data_received(self, data):
        ''' Обработка сообщений клиента. '''
        if data:
            if not self.user:
                user_nickname = data.decode()
                if user_nickname.isalnum():
                    if user_nickname not in self.clients:
                        self.user = user_nickname
                        self.clients.update({self.user: self.transport})
                        message = self.make_message(message=self.user, event='connect')
                        for client in self.clients:
                            if client != self.user:
                                self.clients[client].write(message)
                            else:
                                message = self.make_message(event='server')
                                self.clients[client].write(message)
                    else:
                        message = self.make_message(message=user_nickname, event='change nickname')
                        self.transport.write(message)
                else:
                    message = self.make_message(message=user_nickname, event='incorrect nickname')
                    self.transport.write(message)
                    self.transport.close()
            else:
                user_message = data.decode()
                if len(self.clients) > 1:
                    message = self.make_message(message=user_message, author=self.user, event='message')
                    self.logger.info(message.decode())
                    for client in self.clients:
                        if client != self.user:
                            self.clients[client].write(message)
                        else:
                            msg = self.make_message(event='server')
                            self.clients[client].write(msg)
                            your_message = self.make_message(message=user_message, event='me')
                            self.clients[client].write(your_message)
                else:
                    message = self.make_message(event='no users')
                    self.transport.write(message)
        else:
            message = self.make_message(event='')
            self.transport.write(message)


    def make_message(self, message=None, author=None, event=None):
        ''' Форматирование сообщений клиента и сервера для отправки клиентам.'''
        if event == 'connect':
            msg = '{}: {} connected!'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), message)
            return msg.encode()
        elif event == 'disconnect':
            msg = '{}: {} disconnected!'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), message)
            return msg.encode()
        elif event == 'incorrect nickname':
            msg = '{}: Your nickname must contain only letters and numbers, at least one character. ' \
                  '"{}" is an incorrect nickname.'.format(message, datetime.now().strftime('%Y-%m-%d %H:%M'))
            return msg.encode()
        elif event == 'message':
            msg = '{}: {} sent {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), author, message)
            return msg.encode()
        elif event == 'me':
            msg = '{}: YOU SEND USERS {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), message)
            return msg.encode()
        elif event == 'server':
            msg = '{}: Server: ok!.'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))
            return msg.encode()
        elif event == 'no users':
            msg = '{}: Server: there are no other users!'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))
            return msg.encode()
        elif event == 'change nickname':
            msg = '{}: "{}" is already busy.'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), message)
            return msg.encode()
        elif event == '':
            msg = '{}: Sorry! You send nothing.'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))
            return msg.encode()


def run_server():
    ''' Запуск сервера. '''
    clients = dict()
    logger = create_logger()
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ServerProtocol(clients, logger), '127.0.0.1', 8000)
    print('Server is ready for work!')

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server()