import asyncio
import database
import sqlite3



class ServerProtocol(asyncio.Protocol):

    def process_data(self, data, peername):
        print(data)
        """ Обработка сообщений от клиента."""
        try:
            if 'connect' in data:
                return self.connect_user(peername, data.split('-')[1])
            elif 'disconnect' in data:
                return self.disconnect_user(peername, data.split('-')[1])
            else:
                command, nickname, message = data.split('-')[0], data.split('-')[1], data.split('-')[2:]
                if command == 'send':
                    return self.send_message(nickname, message, peername)
                else:
                    return 'Unknown command\n'
        except Exception:
            return "error wrong command\n"


    def connect_user(self, peername, nickname):
        db = None
        row = (nickname, peername[0], peername[1], 'online')
        print(row)
        try:
            db = sqlite3.connect('chat.db')
            cur = db.cursor()
            cur.execute('INSERT INTO chats(nickname, host, port, status) VALUES(?, ?, ?);', row)
            db.commit()
        except sqlite3.IntegrityError:
            return 'Change nickname\n'
        except sqlite3.Error:
            if db: db.rollback()
            return 'Request error\n'
        finally:
            if db: db.close()
            return 'ok\n'


    def disconnect_user(self, peername, nickname):
        db = None
        try:
            db = sqlite3.connect('chat.db')
            cur = db.cursor()
            query = ('UPDATE chats SET status = ? where nickname = ? and host = ? and port = ?')
            row = ('offline', nickname, peername[0], peername[1])
            cur.execute(query, row)
            db.commit()
        except sqlite3.Error:
            if db: db.rollback()
            return 'Request error'
        finally:
            if db: db.close()
            return 'ok\n'


    def send_message(self, nickname, message, peername):
        db = None
        try:
            db = sqlite3.connect('chat.db')
            cur = db.cursor()
            query_sender = ('SELECT nickname FROM chats WHERE host = ? and port = ?')
            sender = cur.execute(query_sender, (peername[0], peername[1])).fetchone()
            print(sender)
            query_recipient = ('SELECT * FROM chats WHERE nickname = ?')
            recipient = cur.execute(query_recipient, (nickname)).fetchone()
            self.transport.sendto('message: {} from: {}'.format(message, sender).encode(), (recipient[1], recipient[2]))
        except sqlite3.Error:
            if db: db.rollback()
            return 'Request error'
        finally:
            if db: db.close()
            return 'ok\n'


    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport
    

    def data_received(self, data):
        resp = self.process_data(data.decode(), self.peername)
        self.transport.write(resp.encode())


def run_server():
    database.main()
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ServerProtocol,
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