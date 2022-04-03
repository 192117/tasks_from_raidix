import sqlite3

def main():
    db = sqlite3.connect('chat.db')
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS chats (
        nickname TEXT UNIQUE,
        host TEXT,
        port INT
        status TEXT)
    ''')
    db.commit()
