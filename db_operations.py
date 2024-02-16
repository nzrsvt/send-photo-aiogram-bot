import sqlite3

def connect_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    return conn, cur

def create_users_table():
    conn, cur = connect_db()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            photo_path TEXT,
            instagram_nickname TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id, username, full_name):
    conn, cur = connect_db()

    cur.execute('''
        INSERT INTO users (user_id, username, full_name)
        VALUES (?, ?, ?)
    ''', (user_id, username, full_name))

    conn.commit()
    conn.close()

def update_user_photo_path(user_id, photo_path):
    conn, cur = connect_db()

    cur.execute('''
        UPDATE users
        SET photo_path = ?
        WHERE user_id = ?
    ''', (photo_path, user_id))

    conn.commit()
    conn.close()

def update_user_nickname(user_id, instagram_nickname):
    conn, cur = connect_db()

    cur.execute('''
        UPDATE users
        SET instagram_nickname = ?
        WHERE user_id = ?
    ''', (instagram_nickname, user_id))

    conn.commit()
    conn.close()

def check_user_existence(user_id):
    conn, cur = connect_db()

    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cur.fetchone()

    conn.close()

    return user_data is not None