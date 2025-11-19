import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'phone_station',
    'user': 'postgres',
    'password': 'postgres'
}

fake = Faker('uk_UA')

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

def populate_tariffs():
    conn = create_connection()
    cur = conn.cursor()
    
    tariffs = [
        ('внутрішній', 0.50),
        ('міжміський', 2.00),
        ('мобільний', 1.50)
    ]
    
    cur.execute("DELETE FROM Tariffs")
    for call_type, cost in tariffs:
        cur.execute(
            "INSERT INTO Tariffs (call_type, cost_per_minute) VALUES (%s, %s)",
            (call_type, cost)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Tariffs populated")

def populate_clients():
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM Clients")
    
    individual_clients = 3
    office_clients = 2
    
    for _ in range(individual_clients):
        cur.execute(
            "INSERT INTO Clients (client_type, address, surname, name, middle_name) VALUES (%s, %s, %s, %s, %s)",
            ('фізична особа', fake.address(), fake.last_name(), fake.first_name(), fake.middle_name())
        )
    
    for _ in range(office_clients):
        cur.execute(
            "INSERT INTO Clients (client_type, address, surname, name, middle_name) VALUES (%s, %s, %s, %s, %s)",
            ('відомство', fake.address(), None, None, None)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Clients populated")

def populate_phones():
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT client_code FROM Clients")
    client_codes = [row[0] for row in cur.fetchall()]
    
    cur.execute("DELETE FROM Phones")
    
    phone_numbers = []
    for i in range(7):
        phone = fake.phone_number().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(phone) > 20:
            phone = phone[:20]
        if phone not in phone_numbers:
            phone_numbers.append(phone)
            client_code = random.choice(client_codes)
            cur.execute(
                "INSERT INTO Phones (phone_number, client_code) VALUES (%s, %s)",
                (phone, client_code)
            )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Phones populated")

def populate_conversations():
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT phone_number FROM Phones")
    phone_numbers = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT tariff_code, call_type FROM Tariffs")
    tariffs = cur.fetchall()
    
    cur.execute("DELETE FROM Conversations")
    
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(20):
        phone_number = random.choice(phone_numbers)
        tariff_code, call_type = random.choice(tariffs)
        minutes = random.randint(1, 120)
        conversation_date = start_date + timedelta(days=random.randint(0, 29))
        
        cur.execute(
            "INSERT INTO Conversations (conversation_date, phone_number, minutes, tariff_code) VALUES (%s, %s, %s, %s)",
            (conversation_date.date(), phone_number, minutes, tariff_code)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("Conversations populated")

if __name__ == "__main__":
    populate_tariffs()
    populate_clients()
    populate_phones()
    populate_conversations()
    print("Database populated successfully")
