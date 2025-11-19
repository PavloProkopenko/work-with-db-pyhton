import psycopg2
from tabulate import tabulate
import queries

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'phone_station',
    'user': 'postgres',
    'password': 'postgres'
}

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_table_structure(table_name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT 
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]

def get_table_data(table_name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    return cur.fetchall(), [desc[0] for desc in cur.description]

def print_table_info(table_name):
    print(f"\n{'='*80}")
    print(f"ТАБЛИЦЯ: {table_name.upper()}")
    print(f"{'='*80}\n")
    
    structure, structure_headers = get_table_structure(table_name)
    print("СТРУКТУРА:")
    print(tabulate(structure, headers=structure_headers, tablefmt="grid"))
    print()
    
    data, data_headers = get_table_data(table_name)
    print("ДАНІ:")
    if data:
        print(tabulate(data, headers=data_headers, tablefmt="grid"))
    else:
        print("Таблиця порожня")
    print()

def print_query_result(title, data, headers):
    print(f"\n{'='*80}")
    print(f"ЗАПИТ: {title}")
    print(f"{'='*80}\n")
    if data:
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print("Результати відсутні")
    print()

def main():
    tables = ['Clients', 'Phones', 'Tariffs', 'Conversations']
    
    for table in tables:
        print_table_info(table)
    
    print_query_result(
        "1. Всі клієнти-фізичні особи, відсортовані по прізвищу",
        *queries.query_1()
    )
    
    print_query_result(
        "2. Кількість клієнтів по типах (підсумковий запит)",
        *queries.query_2()
    )
    
    print_query_result(
        "3. Вартість кожної розмови (запит з обчислювальним полем)",
        *queries.query_3()
    )
    
    print_query_result(
        "4. Список розмов з типом 'внутрішній' (запит з параметром)",
        *queries.query_4('внутрішній')
    )
    
    print_query_result(
        "5. Загальна вартість всіх розмов для кожного клієнта (підсумковий запит)",
        *queries.query_5()
    )
    
    print_query_result(
        "6. Кількість хвилин кожного типу дзвінків для кожного клієнта (перехресний запит)",
        *queries.query_6()
    )

if __name__ == "__main__":
    main()
