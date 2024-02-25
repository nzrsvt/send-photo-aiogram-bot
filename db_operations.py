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
            instagram_nickname TEXT,
            is_admin BOOLEAN DEFAULT FALSE
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

def update_user_instagram(user_id, instagram_nickname):
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

def check_user_existence_by_username(username):
    conn, cur = connect_db()

    cur.execute('SELECT * FROM users WHERE username = ?', (username.lower(),))
    user_data = cur.fetchone()

    conn.close()

    return user_data is not None

def check_user_instagram_existence(user_id):
    conn, cur = connect_db()

    cur.execute('SELECT instagram_nickname FROM users WHERE user_id = ?', (user_id,))

    result = cur.fetchone()

    conn.close()

    return result is not None and result[0] != 'None' and result[0] is not None

def get_all_users():
    conn, cur = connect_db()

    cur.execute('SELECT * FROM users')
    all_users = cur.fetchall()

    conn.close()

    return all_users

def set_as_admin(username):
    conn, cur = connect_db()

    cur.execute('UPDATE users SET is_admin = ? WHERE username = ?', (True, username.lower()))

    conn.commit()
    conn.close()

def check_is_admin(user_id):
    conn, cur = connect_db()

    cur.execute('SELECT is_admin FROM users WHERE user_id = ?', (user_id,))
    result = cur.fetchone()

    conn.close()

    return result and result[0]

def check_is_admin_by_username(username):
    conn, cur = connect_db()

    cur.execute('SELECT is_admin FROM users WHERE username = ?', (username.lower(),))
    result = cur.fetchone()

    conn.close()

    return result and result[0]