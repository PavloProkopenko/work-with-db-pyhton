import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'phone_station',
    'user': 'postgres',
    'password': 'postgres'
}

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

def query_1():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT client_code, client_type, address, surname, name, middle_name
        FROM Clients
        WHERE client_type = 'фізична особа'
        ORDER BY surname
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]

def query_2():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            client_type,
            COUNT(*) as count
        FROM Clients
        GROUP BY client_type
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]

def query_3():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.conversation_code,
            c.conversation_date,
            c.phone_number,
            c.minutes,
            t.cost_per_minute,
            (c.minutes * t.cost_per_minute) as total_cost
        FROM Conversations c
        JOIN Tariffs t ON c.tariff_code = t.tariff_code
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]

def query_4(call_type):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            c.conversation_code,
            c.conversation_date,
            c.phone_number,
            c.minutes,
            t.call_type
        FROM Conversations c
        JOIN Tariffs t ON c.tariff_code = t.tariff_code
        WHERE t.call_type = %s
    """, (call_type,))
    return cur.fetchall(), [desc[0] for desc in cur.description]

def query_5():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            cl.client_code,
            cl.client_type,
            cl.surname,
            cl.name,
            COALESCE(SUM(c.minutes * t.cost_per_minute), 0) as total_cost
        FROM Clients cl
        LEFT JOIN Phones p ON cl.client_code = p.client_code
        LEFT JOIN Conversations c ON p.phone_number = c.phone_number
        LEFT JOIN Tariffs t ON c.tariff_code = t.tariff_code
        GROUP BY cl.client_code, cl.client_type, cl.surname, cl.name
        ORDER BY cl.client_code
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]

def query_6():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            cl.client_code,
            cl.surname,
            cl.name,
            t.call_type,
            COALESCE(SUM(c.minutes), 0) as total_minutes
        FROM Clients cl
        CROSS JOIN Tariffs t
        LEFT JOIN Phones p ON cl.client_code = p.client_code
        LEFT JOIN Conversations c ON p.phone_number = c.phone_number AND t.tariff_code = c.tariff_code
        GROUP BY cl.client_code, cl.surname, cl.name, t.call_type
        ORDER BY cl.client_code, t.call_type
    """)
    return cur.fetchall(), [desc[0] for desc in cur.description]
