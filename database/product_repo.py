from database.db import get_connection


def save_product(product_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO products(
            code,
            name,
            price,
            description
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            product_data["code"],
            product_data["name"],
            product_data["price"],
            product_data["description"]
        )
    )
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM products
        """
    )
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_code(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE code = ?
        """,
        (code,)
    )
    product = cursor.fetchone()
    conn.close()
    return product

def product_exists(code):
    product = get_product_by_code(code)
    return product is not None

def update_product(product_id, product_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET code = ?, name = ?, price = ?, description = ?
        WHERE id = ?
    """, (
        product_data["code"],
        product_data["name"],
        product_data["price"],
        product_data["description"],
        product_id
    ))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product