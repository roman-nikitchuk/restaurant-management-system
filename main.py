from database.connection import get_connection

try:
    conn = get_connection()
    print("Підключення успішне!")
    conn.close()
except Exception as e:
    print(f"Помилка: {e}")