import sqlite3
import os

def get_db_path():
    """Get cross-platform database path"""
    cwd = os.getcwd()
    return os.path.join(cwd, 'database', 'db.db')

def createDabase():
    global conn, cursor
    database_path = get_db_path()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    print('Database Created')

def InsertData(name,email,password,mobile):
    database_path = get_db_path()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `users` ("
                   "username,email,password,mobile) "
                   "VALUES(?, ?, ?, ?)",
                   (name,email,password,mobile))

    conn.commit()
    print('Inserted Data')

def read_cred(email,password):
    database_path = get_db_path()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT username,email,password,mobile FROM users WHERE email = ? and password = ?", (email, password))
    fetch = cursor.fetchone()
    print(fetch)
    return fetch

createDabase()
