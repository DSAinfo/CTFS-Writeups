import mariadb
from mariadb.constants import CLIENT
from hashlib import sha256
import os

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "meower",
    "password": "meowmeowmeow",
    "database": "catvault"
}

FLAG = os.environ.get("FLAG", "L3AK{real_flag_not_for_testing}")

conn: mariadb.Connection = None
cursor: mariadb.Cursor = None

initialized = False

def create_tables():
    connect()
    cursor.execute("CREATE OR REPLACE TABLE users ( id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(32) UNIQUE, password VARCHAR(64) );")
    cursor.execute("CREATE OR REPLACE TABLE vault ( id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, content TEXT );")

def create_admin():
    connect()
    cursor.execute("INSERT INTO users (name, password) VALUES ('admin', 'nologin');")
    conn.commit()
    cursor.execute(f"INSERT INTO vault (user_id, content) VALUES ({cursor.lastrowid}, '{FLAG}');")
    conn.commit()

def connect():
    global conn, cursor, initialized
    try:
        conn._check_closed()
        return
    except:
        pass
    conn = mariadb.connect(**config, client_flag=CLIENT.MULTI_STATEMENTS)
    cursor = conn.cursor()
    if not initialized:
        create_tables()
        create_admin()
        initialized = True

def create_user(username, password):
    connect()
    cursor.execute("INSERT INTO users (name, password) VALUES (?, ?);", (username, sha256(password).digest().hex()))
    conn.commit()
    return cursor.lastrowid

def login(username, password):
    connect()
    cursor.execute("SELECT id, name, password FROM users WHERE name = ? AND password = ?;", (username, sha256(password).digest().hex()))

def get_vault_entries(user_id):
    connect()
    cursor.execute(f"SELECT id, content FROM vault WHERE id = {user_id};")
    return [i for i in cursor]

def add_vault_entry(user_id, content):
    connect()
    cursor.execute(f"INSERT INTO vault (user_id, content) VALUES ({user_id}, ?);", (content,))
    conn.commit()
    return cursor.lastrowid
