import asyncio
import sqlite3

db = []

class ServerProtocol(asyncio.Protocol):

    def process_data(self, data):
        """ Обработка сообщений от клиента."""
        try:
            if data == 'connect':
                pass
            elif data == 'disconnect':
                pass
            else:
                command, address, message = data.split('-')[0], data.split('-')[1], data.split('-')[2:]
                pass


    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        ''' Обработка входящих сообщений от клиента и отправка ответа от сервера.'''
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())
