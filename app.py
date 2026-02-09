from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# ข้อมูลสินค้า
PRODUCTS = [
    {
        'id': 1,
        'name': 'แพลนเนอร์ (Planner)"',
        'price': 79,
        'category': 'หมวดบันทึกประจำวัน',
        'image': 'product1.png'
    },
    {
        'id': 2,
        'name': 'สมุดเช็คลิสต์ (Checklist Book)',
        'price': 49,
        'category': 'หมวดบันทึกประจำวัน',
        'description': 'สมุดสำหรับจดบันทึกสิ่งที่ต้องทำรายวัน รายสัปดาห์ หรือรายเดือน ช่วยให้ไม่ลืมงานสำคัญและจัดลำดับความสำคัญได้ดี',
        'image': 'product2.png'
    },
    {
        'id': 3,
        'name': 'สมุดติดตามนิสัย (Habit Tracker)',
        'price': 39,
        'category': 'หมวดบันทึกประจำวัน',
        'description': 'ใช้บันทึกกิจกรรมซ้ำๆ ที่อยากทำเป็นประจำ',
        'image': 'product3.png'
    },
    {
        'id': 4,
        'name': 'บันทึกความสุข (Gratitude Journal)',
        'price': 59,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดที่มี Template ให้เขียนขอบคุณเรื่องดีๆ 3 ข้อในแต่ละวัน',
        'image': 'product4.png'
    },
    {
        'id': 5,
        'name': 'สมุดระบายความคิด (Mind Dump Journal)',
        'price': 149,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดเส้นเปล่าสำหรับเขียนความรู้สึกทันทีหลังตื่นนอน เพื่อเคลียร์สมอง',
        'image': 'product5.png'
    },
    {
        'id': 6,
        'name': 'บันทึกบรรทัดเดียวต่อวัน (One Line A Day)',
        'price': 79,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดที่ให้เขียนสั้นๆ เพียงวันละ 1-3 ประโยค ต่อเนื่องกันหลายปี (3-5 ปี)',
        'image': 'product6.png'
    },
    {
        'id': 7,
        'name': 'บันทึกการประชุม (Meeting Notes)',
        'price': 79,
        'category': 'หมวดงานและการเรียน',
        'description': 'มีช่องสำหรับเขียนหัวข้อ, ผู้เข้าร่วม, มติที่ประชุม และ Action Plan',
        'image': 'product7.png'
    },
    {
        'id': 8,
        'name': 'สมุดจดสรุป (Cornell Notebook)',
        'price': 79,
        'category': 'หมวดงานและการเรียน',
        'description': 'สมุดที่แบ่งหน้ากระดาษเป็น 3 ส่วน (จดโน้ต, คีย์เวิร์ด, สรุป) ตามหลักการเรียนรู้',
        'image': 'product8.png'
    },
    {
        'id': 9,
        'name': 'สมุดตาราง (Grid/Square Notebook)',
        'price': 99,
        'category': 'หมวดงานและการเรียน',
        'description': 'เหมาะสำหรับสายคำนวณ วาดกราฟ หรือเขียนตัวอักษรภาษาจีน/ญี่ปุ่น',
        'image': 'product9.png'
    }
]

@app.route("/")
def home():
    category = request.args.get('category', 'ทั้งหมด')
    
    if category == 'ทั้งหมด':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
    
    categories = ['ทั้งหมด', 'หมวดบันทึกประจำวัน', 'หมวดพัฒนาความคิดและจิตใจ', 'หมวดงานและการเรียน']
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