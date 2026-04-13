from connect import get_connection

def create_table():
    """Creating table"""
    command = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) UNIQUE NOT NULL
    )
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()

create_table()

def call_upsert(name, phone):
    """Call the procedure upsert_contact"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s::VARCHAR, %s::VARCHAR)", (name, phone))
                conn.commit()
                print(f"Contact {name} processed successfully.")
    except Exception as e:
        print(f"Error in call_upsert: {e}")

def search_contacts(pattern):
    """Call the function get_contacts_by_pattern"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s::TEXT)", (pattern,))
                return cur.fetchall()
    except Exception as e:
        print(f"Error in search_contacts: {e}")
        return []

def bulk_insert(names, phones):
    """Mass inserting"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL bulk_insert_contacts(%s::VARCHAR[], %s::VARCHAR[], NULL)", (names, phones))
                errors = cur.fetchone()
                if errors and errors[0]:
                    print(f"Skipped due to invalid format: {errors[0]}")
                else:
                    print("All contacts inserted successfully.")
                conn.commit()
    except Exception as e:
        print(f"Error in bulk_insert: {e}")

def get_paginated(limit, offset):
    """Pagination"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s::INT, %s::INT)", (limit, offset))
                return cur.fetchall()
    except Exception as e:
        print(f"Error in get_paginated: {e}")
        return []

def delete_contact(target):
    """Deleting"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s::VARCHAR)", (target,))
                conn.commit()
                print(f"Delete operation for '{target}' completed.")
    except Exception as e:
        print(f"Error in delete_contact: {e}")

if __name__ == "__main__":
    #! TESTS:
    print("--- Testing Upsert ---")
    call_upsert("Alice", "87071112233")
    
    print("\n--- Testing Search ---")
    print(search_contacts("M"))
    
    print("\n--- Testing Bulk Insert ---")
    bulk_insert(["Bob", "Short", "Patrick", "John", "Marko", "Mavis"],
                ["87075556677", "87773223422", "87475670908",
                 "87054521124", "87871235692", "87279123415"])
    
    print("\n--- Testing Pagination ---")
    print(get_paginated(5, 0))
    
    print("\n--- Testing Deleting ---")
    print(delete_contact("Bob"))