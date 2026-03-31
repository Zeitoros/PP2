from suppliers.database import *

def show_contacts(rows):
    print("\nID | Имя | Телефон")
    print("-" * 30)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]}")

def main():
    create_table()
    while True:
        print("\nPhoneBook Меню")
        print("1. Загрузить из CSV\n2. Добавить контакт\n3. Обновить контакт\n4. Список контактов\n5. Удалить контакт\n0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            path = input("Введите путь к файлу: ")
            upload_from_csv(path)

        elif choice == '2':
            name = input("Имя: ")
            phone = input("Телефон: ")
            insert_contact(name, phone)
            
        elif choice == '3':
            show_contacts(get_all_contacts('1'))
            tid = input("Введите ID для правки: ")
            print("1 - Имя | 2 - Телефон | 3 - Всё")
            sub_ch = input("> ")
            if sub_ch == '1':
                update_db_contact(tid, name=input("Новое имя: "))
            elif sub_ch == '2':
                update_db_contact(tid, phone=input("Новый телефон: "))
            elif sub_ch == '3':
                update_db_contact(tid, input("Имя: "), input("Тел: "))

        elif choice == '4':
            print("1 - Все | 2 - По первой букве | 3 - По префиксу номера")
            f_type = input("Фильтр: ")
            search = None
            if f_type == '2':
                search = input("Введите начало имени: ")
            elif f_type == '3':
                search = input("Введите начало номера телефона: ")
            contacts = get_all_contacts(filter_type=f_type, extra_data=search)
            if not contacts:
                print("\nКонтактов не найдено.")
            else:
                print(f"\nНайдено: {len(contacts)}")
                print(f"{'#':<3} | {'Имя':<15} | {'Телефон':<15}")
                print("-" * 40)
                for idx, row in enumerate(contacts, 1):
                    print(f"{idx:<3} | {row[1]:<15} | {row[2]:<15}")
            

        elif choice == '5':
            target = input("Введите имя или номер телефона для удаления: ")
            rows_deleted = delete_db_contact(target)
            
            if rows_deleted > 0:
                print(f"Успешно удалено контактов: {rows_deleted}")
            else:
                print("Контакт не найден. Проверьте правильность ввода.")
                
        elif choice == '0':
            break

if __name__ == "__main__":
    main()