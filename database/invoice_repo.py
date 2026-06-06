from database.db import get_connection


def save_invoice(invoice_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO invoices(

            invoice_number,
            invoice_date,

            customer_id,

            total_price,
            tax,
            final_price

        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            invoice_data["invoice_number"],
            invoice_data["invoice_date"],

            invoice_data["customer_id"],

            invoice_data["total_price"],
            invoice_data["tax"],
            invoice_data["final_price"]
        )
    )
    conn.commit()
    invoice_id = cursor.lastrowid
    conn.close()
    return invoice_id

def get_all_invoices():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM invoices
        """
    )
    invoices = cursor.fetchall()
    conn.close()
    return invoices

def get_invoice_by_number(invoice_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM invoices
        WHERE invoice_number = ?
        """,
        (invoice_number,)
    )
    invoice = cursor.fetchone()
    conn.close()
    return invoice

def invoice_exists(invoice_number):
    invoice = get_invoice_by_number(
        invoice_number
    )
    return invoice is not None

def save_invoice_item(
    invoice_id,
    item
):
    conn = get_connection()
    cursor = conn.cursor()
    total = item["qty"] * item["price"]
    cursor.execute(
        """
        INSERT INTO invoice_items(

            invoice_id,
            product_code,
            product_name,
            qty,
            price,
            total

        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            invoice_id,
            item["code"],
            item["name"],
            item["qty"],
            item["price"],
            total
        )
    )
    conn.commit()
    conn.close()
    
def get_invoice_items(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM invoice_items
        WHERE invoice_id = ?
        """,
        (invoice_id,)
    )
    items = cursor.fetchall()
    conn.close()
    return items

def get_invoice_by_id(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    invoice = cursor.fetchone()
    conn.close()
    return invoice

def is_invoice_number_exists(invoice_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM invoices WHERE invoice_number = ?", (invoice_number,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0