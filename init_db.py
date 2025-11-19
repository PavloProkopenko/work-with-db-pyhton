import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'phone_station',
    'user': 'postgres',
    'password': 'postgres'
}

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            client_code SERIAL PRIMARY KEY,
            client_type VARCHAR(20) NOT NULL CHECK (client_type IN ('відомство', 'фізична особа')),
            address VARCHAR(255) NOT NULL,
            surname VARCHAR(100),
            name VARCHAR(100),
            middle_name VARCHAR(100),
            CONSTRAINT check_individual_fields CHECK (
                (client_type = 'фізична особа' AND surname IS NOT NULL AND name IS NOT NULL) OR
                (client_type = 'відомство')
            )
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Tariffs (
            tariff_code SERIAL PRIMARY KEY,
            call_type VARCHAR(20) NOT NULL CHECK (call_type IN ('внутрішній', 'міжміський', 'мобільний')),
            cost_per_minute DECIMAL(10, 2) NOT NULL CHECK (cost_per_minute >= 0) DEFAULT 0.00
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phones (
            phone_number VARCHAR(20) PRIMARY KEY,
            client_code INTEGER NOT NULL,
            CONSTRAINT fk_phone_client FOREIGN KEY (client_code) 
                REFERENCES Clients(client_code) 
                ON DELETE CASCADE 
                ON UPDATE CASCADE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Conversations (
            conversation_code SERIAL PRIMARY KEY,
            conversation_date DATE NOT NULL DEFAULT CURRENT_DATE,
            phone_number VARCHAR(20) NOT NULL,
            minutes INTEGER NOT NULL CHECK (minutes > 0),
            tariff_code INTEGER NOT NULL,
            CONSTRAINT fk_conversation_phone FOREIGN KEY (phone_number) 
                REFERENCES Phones(phone_number) 
                ON DELETE RESTRICT 
                ON UPDATE CASCADE,
            CONSTRAINT fk_conversation_tariff FOREIGN KEY (tariff_code) 
                REFERENCES Tariffs(tariff_code) 
                ON DELETE RESTRICT 
                ON UPDATE CASCADE
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()
