import csv
from suppliers.connect import get_connection

def create_table():
    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        phone_number VARCHAR(20) UNIQUE NOT NULL
    )
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()

def upload_from_csv(file_path):
    sql = "INSERT INTO phonebook(first_name, phone_number) VALUES(%s, %s) ON CONFLICT (phone_number) DO NOTHING"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        cur.execute(sql, row)
            conn.commit()
        print("Успешно")
    except Exception as e:
        print(f"Ошибка: {e}")

def insert_contact(name, phone):
    insert_sql = "INSERT INTO phonebook(first_name, phone_number) VALUES(%s, %s) ON CONFLICT DO NOTHING"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (name, phone))

                if cur.rowcount > 0:
                    print(f"Контакт '{name}' успешно добавлен.")
                else:
                    print(f"Ошибка: Номер телефона '{phone}' уже существует в справочнике.")
                
            conn.commit()
    except Exception as e:
        print(f"Произошла системная ошибка: {e}")

def get_all_contacts(filter_type=None, extra_data=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if filter_type == '1':
                cur.execute("SELECT * FROM phonebook ORDER BY id")
            elif filter_type == '2':
                cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"{extra_data}%",))
            elif filter_type == '3':
                cur.execute("SELECT * FROM phonebook WHERE phone_number ILIKE %s ORDER BY id", (f"{extra_data}%",))
            else:
                cur.execute("SELECT * FROM phonebook ORDER BY id")
            return cur.fetchall()

def update_db_contact(target_id, name=None, phone=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if not name and not phone:
                return 0
            
            if name and phone:
                sql = "UPDATE phonebook SET first_name = %s, phone_number = %s WHERE id = %s"
                params = (name, phone, target_id)
            elif name:
                sql = "UPDATE phonebook SET first_name = %s WHERE id = %s"
                params = (name, target_id)
            else:
                sql = "UPDATE phonebook SET phone_number = %s WHERE id = %s"
                params = (phone, target_id)
            
            cur.execute(sql, params)
            updated_count = cur.rowcount
        conn.commit()
        return updated_count

def delete_db_contact(target):
    sql = "DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s"
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (target, target))
            deleted_rows = cur.rowcount
        conn.commit()
        return deleted_rows