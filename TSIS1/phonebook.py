import psycopg2
import json
import csv
import sys
from connect import get_connection

def export_to_json(conn, filename="contacts.json"):
    """Экспорт всех контактов со всеми связями в JSON"""
    cur = conn.cursor()
    cur.execute("""
        SELECT c.first_name, c.last_name, c.email, c.birthday, g.name,
               array_agg(p.phone || ':' || p.type)
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """)
    rows = cur.fetchall()
    data = []
    for r in rows:
        data.append({
            "first_name": r[0], "last_name": r[1],
            "email": r[2], "birthday": str(r[3]),
            "group": r[4], "phones": r[5] if r[5] != [None] else []
        })
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Данные экспортированы в {filename}")

def import_from_json(conn, filename="contacts.json"):
    """Импорт из JSON с обработкой дубликатов"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Файл JSON не найден.")
        return

    cur = conn.cursor()
    for item in data:
        cur.execute("SELECT id FROM contacts WHERE first_name=%s AND last_name=%s", 
                    (item['first_name'], item['last_name']))
        exists = cur.fetchone()
        
        if exists:
            choice = input(f"Контакт {item['first_name']} {item['last_name']} уже есть. Перезаписать? (y/n): ")
            if choice.lower() != 'y': continue
            cur.execute("DELETE FROM contacts WHERE id=%s", (exists[0],))
        
        # Создание группы и вставка контакта
        cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (item['group'],))
        g_id = cur.fetchone()[0]
        
        cur.execute("INSERT INTO contacts (first_name, last_name, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id",
                    (item['first_name'], item['last_name'], item['email'], item['birthday'], g_id))
        c_id = cur.fetchone()[0]
        
        for p_info in item['phones']:
            p, t = p_info.split(':')
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)", (c_id, p, t))
    conn.commit()
    print("Импорт завершен.")

# --- КОНСОЛЬНЫЙ ИНТЕРФЕЙС ---

def paginated_view(conn):
    print("\n--- Выберите сортировку ---")
    print("1. По имени")
    print("2. По дате рождения")
    print("3. По дате добавления (Date)")
    sort_choice = input("Выбор: ")
    
    sort_map = {
        '1': 'first_name, last_name',
        '2': 'birthday',
        '3': 'created_at'
    }
    order_by = sort_map.get(sort_choice, 'first_name')

    page = 0
    limit = 5
    while True:
        cur = conn.cursor()
        # Cортировка в запросе пагинации
        query = f"""
            SELECT first_name, last_name, email, birthday 
            FROM contacts 
            ORDER BY {order_by} 
            LIMIT %s OFFSET %s
        """
        cur.execute(query, (limit, page * limit))
        rows = cur.fetchall()
        
        print(f"\n--- Страница {page+1} (Сортировка: {order_by}) ---")
        for r in rows: 
            print(f"{r[0]} {r[1]} | Email: {r[2]} | BD: {r[3]}")
        
        cmd = input("\n[n]next, [p]prev, [q]quit: ").lower()
        if cmd == 'n' and len(rows) == limit: page += 1
        elif cmd == 'p': page = max(0, page - 1)
        elif cmd == 'q': break

def advanced_search(conn):
    print("\n--- Расширенный поиск и фильтрация ---")
    print("1. Поиск по тексту (Email/Имя/Телефон)")
    print("2. Фильтр по группе")
    choice = input("Выберите вариант: ")
    
    cur = conn.cursor()
    if choice == '1':
        query = input("Введите запрос: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    elif choice == '2':
        group_name = input("Введите название группы: ")
        # Поиск контактов, принадлежащих конкретной группе
        cur.execute("""
            SELECT c.id, (c.first_name || ' ' || c.last_name), c.email, string_agg(p.phone, ', ')
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE g.name ILIKE %s
            GROUP BY c.id
        """, (group_name,))
    
    results = cur.fetchall()
    for r in results:
        print(f"ID: {r[0]} | Имя: {r[1]} | Email: {r[2]} | Телефоны: {r[3]}")

# --- ДЕМОНСТРАЦИЯ ВЫВОДА ---

def run_demo_output(conn):
    """Тесты вывода: имитация работы фильтров и сортировки для проверки визуальной части"""
    cur = conn.cursor()
    print("\n" + "="*50)
    print("ТЕСТЫ ВЫВОДА (DEMO MODE)")
    print("="*50)

    # 1. Тест сортировки по Имени
    print("\n[ТЕСТ 1] Сортировка по имени (First Name):")
    cur.execute("SELECT first_name, last_name, email FROM contacts ORDER BY first_name LIMIT 3")
    for r in cur.fetchall(): print(f"{r[0]} {r[1]} | {r[2]}")

    # 2. Тест сортировки по Дате рождения
    print("\n[ТЕСТ 2] Сортировка по дате рождения (Birthday):")
    cur.execute("SELECT first_name, birthday FROM contacts WHERE birthday IS NOT NULL ORDER BY birthday ASC LIMIT 3")
    for r in cur.fetchall(): print(f"{r[0]} | Дата: {r[1]}")

    # 3. Тест фильтрации по Группе
    print("\n[ТЕСТ 3] Фильтр по группе 'Work':")
    cur.execute("""
        SELECT c.first_name, g.name 
        FROM contacts c 
        JOIN groups g ON c.group_id = g.id 
        WHERE g.name ILIKE 'Work' LIMIT 3
    """)
    rows = cur.fetchall()
    if rows:
        for r in rows: print(f"{r[0]} | Группа: {r[1]}")
    else:
        print("ℹГруппа 'Work' пуста или не создана.")

    # 4. Тест поиска по Email (через хранимую функцию)
    print("\n[ТЕСТ 4] Поиск по части Email (например, 'gmail'):")
    cur.execute("SELECT * FROM search_contacts('gmail') LIMIT 3")
    for r in cur.fetchall():
        print(f"Найдено: {r[1]} | Email: {r[2]}")

    print("\n" + "="*50)
    print("ТЕСТЫ ВЫВОДА ЗАВЕРШЕНЫ")
    print("="*50)

# --- ГЛАВНОЕ МЕНЮ ---

def main_menu():
    conn = get_connection()
    if not conn: return
    
    while True:
        print("\n--- PhoneBook TSIS 1 ---")
        print("1. Просмотр + Сортировка")
        print("2. Поиск + Фильтр")
        print("3. Экспорт в JSON")
        print("4. Импорт из JSON")
        print("5. ЗАПУСТИТЬ ТЕСТЫ ВЫВОДА (Demo)")
        print("6. Выход")
        
        choice = input("Выберите действие: ")
        if choice == '1': paginated_view(conn)
        elif choice == '2': advanced_search(conn)
        elif choice == '3': export_to_json(conn)
        elif choice == '4': import_from_json(conn)
        elif choice == '5': run_demo_output(conn)
        elif choice == '6': break
    
    conn.close()

if __name__ == "__main__":
    main_menu()