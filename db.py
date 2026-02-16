import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT,
        description TEXT,
        image TEXT
    )
    ''')
    conn.commit()
    conn.close()


def add_product(product):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO products (name, price, category, description, image)
                 VALUES (?, ?, ?, ?, ?)''',
              (product['name'], product['price'], product.get('category', ''), product.get('description', ''), product.get('image', 'default.png')))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return get_product(new_id)


def delete_product(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()


def update_product(product_id, fields):
    # fields is a dict of columns to update
    keys = []
    values = []
    for k, v in fields.items():
        keys.append(f"{k} = ?")
        values.append(v)
    if not keys:
        return get_product(product_id)
    values.append(product_id)
    conn = get_conn()
    c = conn.cursor()
    query = f"UPDATE products SET {', '.join(keys)} WHERE id = ?"
    c.execute(query, values)
    conn.commit()
    conn.close()
    return get_product(product_id)


def get_product(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def get_all_products():
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM products ORDER BY id')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_products_by_category(category):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE category = ? ORDER BY id', (category,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
