from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# ข้อมูลสินค้า
PRODUCTS = [
    {
        'id': 1,
        'name': 'MacBook Pro 14"',
        'price': 79999,
        'category': 'คอมพิวเตอร์',
        'description': 'MacBook Pro พร้อม M3 Pro',
        'image': 'product1.png'
    },
    {
        'id': 2,
        'name': 'iPhone 15 Pro',
        'price': 44999,
        'category': 'อิเล็กทรอนิกส์',
        'description': 'iPhone 15 Pro 256GB',
        'image': 'product2.png'
    },
    {
        'id': 3,
        'name': 'Canon EOS R5',
        'price': 149999,
        'category': 'กล้อง',
        'description': 'กล้อง DSLR มืออาชีพ',
        'image': 'product3.png'
    },
    {
        'id': 4,
        'name': 'iPad Air',
        'price': 29999,
        'category': 'คอมพิวเตอร์',
        'description': 'iPad Air 11 นิ้ว',
        'image': 'product4.png'
    },
    {
        'id': 5,
        'name': 'Sony WH-1000XM5',
        'price': 14999,
        'category': 'อิเล็กทรอนิกส์',
        'description': 'หูฟังบลูทูธระดับพรีเมียม',
        'image': 'product5.png'
    },
    {
        'id': 6,
        'name': 'DJI Air 3S',
        'price': 34999,
        'category': 'กล้อง',
        'description': 'โดรนถ่ายภาพ 4K',
        'image': 'product6.png'
    }
]

@app.route("/")
def home():
    category = request.args.get('category', 'ทั้งหมด')
    
    if category == 'ทั้งหมด':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
    
    categories = ['ทั้งหมด', 'อิเล็กทรอนิกส์', 'คอมพิวเตอร์', 'กล้อง']
    cart_count = len(session.get('cart', []))
    
    return render_template("home.html", 
                         products=filtered_products, 
                         categories=categories, 
                         current_category=category,
                         cart_count=cart_count)

@app.route("/cart")
def cart():
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            product_copy = product.copy()
            product_copy['quantity'] = item['quantity']
            product_copy['subtotal'] = product['price'] * item['quantity']
            cart_products.append(product_copy)
            total += product_copy['subtotal']
    
    return render_template("cart.html", 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items))

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        data = request.get_json()
        # บันทึกข้อมูลการสั่งซื้อ (ในแอปจริง ควรบันทึกลงฐานข้อมูล)
        session['cart'] = []
        return jsonify({'success': True, 'message': 'สั่งซื้อสำเร็จ'})
    
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            product_copy = product.copy()
            product_copy['quantity'] = item['quantity']
            product_copy['subtotal'] = product['price'] * item['quantity']
            cart_products.append(product_copy)
            total += product_copy['subtotal']
    
    return render_template("checkout.html", 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items))

@app.route("/api/cart/add", methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    
    # ตรวจสอบสินค้าที่มีอยู่แล้ว
    existing_item = next((item for item in cart if item['id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({'id': product_id, 'quantity': quantity})
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(cart), 'message': 'เพิ่มสินค้าเรียบร้อยแล้ว'})

@app.route("/api/cart/remove", methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('id')
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(cart)})

@app.route("/api/cart/update", methods=['POST'])
def update_cart():
    data = request.get_json()
    product_id = data.get('id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    item = next((item for item in cart if item['id'] == product_id), None)
    
    if item:
        if quantity > 0:
            item['quantity'] = quantity
        else:
            cart = [i for i in cart if i['id'] != product_id]
    
    session['cart'] = cart
    session.modified = True
    
    # คำนวณราคารวม
    total = 0
    for item in cart:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            total += product['price'] * item['quantity']
    
    return jsonify({'success': True, 'cart_count': len(cart), 'total': total})

@app.route("/api/cart/get", methods=['GET'])
def get_cart():
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            product_copy = product.copy()
            product_copy['quantity'] = item['quantity']
            product_copy['subtotal'] = product['price'] * item['quantity']
            cart_products.append(product_copy)
            total += product_copy['subtotal']
    
    return jsonify({'items': cart_products, 'total': total, 'count': len(cart_items)})

if __name__ == "__main__":
    app.run(debug=True)