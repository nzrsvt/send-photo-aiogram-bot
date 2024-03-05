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

    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
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

def get_all_admins():
    conn, cur = connect_db()

    cur.execute('SELECT * FROM users WHERE is_admin = True')
    all_admins = cur.fetchall()

    conn.close()

    return all_admins

def set_as_admin(username):
    conn, cur = connect_db()

    cur.execute('UPDATE users SET is_admin = ? WHERE username = ?', (True, username))

    conn.commit()
    conn.close()

def set_as_not_admin(username):
    conn, cur = connect_db()

    cur.execute('UPDATE users SET is_admin = ? WHERE username = ?', (False, username))

    conn.commit()
    conn.close()

def set_as_admin_by_user_id(user_id):
    conn, cur = connect_db()

    cur.execute('UPDATE users SET is_admin = ? WHERE user_id = ?', (True, user_id))

    conn.commit()
    conn.close()

def set_as_not_admin_by_user_id(user_id):
    conn, cur = connect_db()

    cur.execute('UPDATE users SET is_admin = ? WHERE user_id = ?', (False, user_id))

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

    cur.execute('SELECT is_admin FROM users WHERE username = ?', (username,))
    result = cur.fetchone()

    conn.close()

    return result and result[0]

def get_user_id_by_username(username):
    conn, cur = connect_db()

    cur.execute('SELECT user_id FROM users WHERE username = ?', (username,))
    result = cur.fetchone()

    conn.close()

    return result[0] if result else None

def get_instagram_nickname_by_username(username):
    conn, cur = connect_db()

    cur.execute('SELECT instagram_nickname FROM users WHERE username = ?', (username,))
    result = cur.fetchone()

    conn.close()

    return result[0] if result and result[0] != 'None' and result[0] is not None else None

def create_photos_table():
    conn, cur = connect_db()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            user_id INTEGER NOT NULL,
            file_id TEXT NOT NULL,
            PRIMARY KEY (user_id, file_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_photo(user_id, file_id):
    conn, cur = connect_db()

    cur.execute('INSERT INTO photos (user_id, file_id) VALUES (?, ?)', (user_id, file_id))

    conn.commit()
    conn.close()

def delete_photo_by_file_id(file_id):
    conn, cur = connect_db()

    cur.execute('DELETE FROM photos WHERE file_id = ?', (file_id,))

    conn.commit()
    conn.close()

def get_file_ids_by_user_id(user_id):
    conn, cur = connect_db()

    cur.execute('SELECT file_id FROM photos WHERE user_id = ?', (user_id,))
    file_ids = [row[0] for row in cur.fetchall()]

    conn.close()

    return file_ids

def delete_all_photos():
    conn, cur = connect_db()

    cur.execute('DELETE FROM photos')

    conn.commit()
    conn.close()

def is_photos_table_empty():
    conn, cur = connect_db()

    cur.execute('SELECT COUNT(*) FROM photos')
    count = cur.fetchone()[0]

    conn.close()

    return count == 0