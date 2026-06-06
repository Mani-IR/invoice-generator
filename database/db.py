import sqlite3
import os

DB_NAME = "invoice.db"
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
DB_PATH = os.path.join(
    BASE_DIR,
    DB_NAME
)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn
if __name__ == "__main__":
    conn = get_connection()
    print("Database Connected")
    conn.close()
    
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items(
    
        id INTEGER PRIMARY KEY AUTOINCREMENT,
    
        invoice_id INTEGER,
    
        product_code TEXT,
        product_name TEXT,
    
       qty INTEGER,
        price INTEGER,
    
        total INTEGER,
    
        FOREIGN KEY(invoice_id)
        REFERENCES invoices(id)
    )
    """)
    # ======================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
    
        id INTEGER PRIMARY KEY AUTOINCREMENT,
    
        code TEXT UNIQUE,
        name TEXT,
    
        price INTEGER,
    
        description TEXT
    )
    """)
    # ======================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        invoice_date TEXT,
        customer_id INTEGER,
        total_price INTEGER,
        tax INTEGER,
        final_price INTEGER,
        FOREIGN KEY(customer_id)
        REFERENCES customers(id)
    )
    """)
    
    # ======================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        invoice_date TEXT,
        customer_id INTEGER,
        total_price INTEGER,
        tax INTEGER,
        final_price INTEGER,
        FOREIGN KEY(customer_id)
        REFERENCES customers(id)
    )
    """)

    # ======================================
    # Customers

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        national_code TEXT,
        economic_code TEXT,
        postal_code TEXT,
        address TEXT
    )
    """)

    # ======================================
    # Products

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    """)

    # ======================================
    # Invoices

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        invoice_date TEXT,
        customer_id INTEGER,
        total_price INTEGER,
        tax INTEGER,
        final_price INTEGER,
        FOREIGN KEY(customer_id)
        REFERENCES customers(id)
    )
    """)

    # ======================================
    # Invoice Items
     
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        product_code TEXT,
        product_name TEXT,
        qty INTEGER,
        price INTEGER,
        total INTEGER,
        FOREIGN KEY(invoice_id)
        REFERENCES invoices(id)
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database Tables Created Successfully")

