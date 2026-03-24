import sqlite3
import os

def init_database():
    """Initialize the database with users table"""
    cwd = os.getcwd()
    db_dir = os.path.join(cwd, 'database')
    
    # Create database directory if it doesn't exist
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    database_path = os.path.join(db_dir, 'db.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            mobile INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    print('Database initialized successfully!')

if __name__ == '__main__':
    init_database()
