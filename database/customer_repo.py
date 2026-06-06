from database.db import get_connection

def save_customer(customer_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO customers(name, phone, national_code, economic_code, postal_code, address)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_data["name"],
        customer_data["phone"],
        customer_data["national_code"],
        customer_data["economic_code"],
        customer_data["postal_code"],
        customer_data["address"]
    ))
    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()
    return customer_id

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM customers
        """
    )
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_customer_by_phone(phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE phone = ?
        """,
        (phone,)
    )
    customer = cursor.fetchone()
    conn.close()
    return customer
def customer_exists(phone):
    customer = get_customer_by_phone(phone)
    return customer is not None

def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer
# database/customer_repo.py (اضافه کردن توابع زیر)

def get_customer_by_id(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def update_customer(customer_id, customer_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE customers
        SET name = ?, phone = ?, national_code = ?, economic_code = ?, postal_code = ?, address = ?
        WHERE id = ?
    """, (
        customer_data["name"],
        customer_data["phone"],
        customer_data["national_code"],
        customer_data["economic_code"],
        customer_data["postal_code"],
        customer_data["address"],
        customer_id
    ))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

def get_customer_invoices(customer_id):
    """بازگرداندن لیست فاکتورهای یک مشتری"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, invoice_number, invoice_date, total_price, tax, final_price
        FROM invoices WHERE customer_id = ?
        ORDER BY invoice_date DESC
    """, (customer_id,))
    invoices = cursor.fetchall()
    conn.close()
    return invoices