import sqlite3
import time

'''# define connection
connection = sqlite3.connect('users.db')

# Create cursor 
cursor = connection.cursor()

create_db = ''CREATE TABLE IF NOT EXISTS
              users(chat_id INTERGER PRIMARY key, 
                    lat FLOAT, 
                    lon FLOAT, 
                    time INTERGER)'

cursor.execute(create_db)

# Add to users 
cursor.execute('INSERT INTO users VALUES (2654321, 41.28610, 1.98241, 1588747199)')
connection.commit()
# Get values
cursor.execute('SELECT chat_id FROM users')
res = cursor.fetchall()
print(res) '''

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.curs = self.conn.cursor()
        create_db = '''CREATE TABLE IF NOT EXISTS
                       users(chat_id INTERGER PRIMARY key, 
                             lat FLOAT, 
                             lon FLOAT, 
                             time INTERGER)'''

        self.curs.execute(create_db)

    def chk_user(self, chat_id):
        self.curs.execute('SELECT lat FROM users WHERE chat_id = {}'.format(chat_id))
        res = self.curs.fetchone()
        if res:
            return True

    def add_user(self, chat_id, lat, lon):
        if self.chk_user(chat_id):
            return True
        self.curs.execute('INSERT INTO users VALUES ({}, {}, {}, {})'.format(chat_id, lat, lon, int(time.time())))
        self.conn.commit()

    def del_user(self, chat_id):
        if not self.chk_user(chat_id):
            return True
        cmd = '''DELETE
                 FROM users
                 WHERE chat_id = {};'''.format(chat_id)
        self.curs.execute(cmd)
        self.conn.commit()

    def upd_user(self, chat_id, lat, lon):
        if not self.chk_user(chat_id):
            self.add_user(chat_id, lat, lon)
            return
        cmd = '''UPDATE users
                 SET lat = {},
                     lon = {},
                     time = {}
                 WHERE chat_id = {};'''.format(lat, lon, int(time.time()), chat_id)
        self.curs.execute(cmd)
        self.conn.commit()

    def get_user(self, chat_id):
        if not self.chk_user(chat_id):
            return True
        cmd = '''SELECT chat_id,
                        lat,
                        lon,
                        time 
                 FROM users
                 WHERE chat_id = {};'''.format(chat_id)
        self.curs.execute(cmd)
        res = self.curs.fetchall()
        lat, lon, time = res[0][1:]
        return lat, lon, time
