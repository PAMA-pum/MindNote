import db
from products_initial import PRODUCTS


def migrate():
    db.init_db()
    existing = db.get_all_products()
    if existing:
        print('Products table already contains data; skipping migration.')
        return

    for p in PRODUCTS:
        prod = {
            'name': p['name'],
            'price': p['price'],
            'category': p.get('category', ''),
            'description': p.get('description', ''),
            'image': p.get('image', 'default.png')
        }
        db.add_product(prod)

    print('Migration completed.')


if __name__ == '__main__':
    migrate()
