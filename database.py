import sqlite3

def get_connection(db_name="usage_data.db"):
    conn = sqlite3.connect(db_name)
    return conn

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screen_time_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_name TEXT,
                start_time TEXT,
                end_time TEXT,
                duration REAL
            )
        ''')
        conn.commit()

def log_session(process_name, start_time, end_time, duration):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO screen_time_log (process_name, start_time, end_time, duration)
            VALUES (?, ?, ?, ?)
        ''', (process_name, start_time, end_time, duration))
        conn.commit()
