from app.db import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Connection is successfull:", tables)
    conn.close()
except Exception as e:
    print("HATA:", e)