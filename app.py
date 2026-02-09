from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from datetime import datetime
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# กำหนดโฟลเดอร์สำหรับอัพโหลดไฟล์
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ข้อมูลผู้ใช้ (ในแอปจริง ควรใช้ฐานข้อมูล)
USERS = {
    'sdpatthama2212@gmail.com': {
        'password': 'pum123456',
        'name': 'ปัทมา แพงไธสง',
        'email': 'sdpatthama2212@gmail.com',
        'is_admin': True
    },
    'demo@mindnote.com': {
        'password': '123456',
        'name': 'Demo User',
        'email': 'demo@mindnote.com',
        'is_admin': False
    }
}

# ข้อมูลสินค้า
PRODUCTS = [
    {
        'id': 1,
        'name': 'แพลนเนอร์ (Planner)"',
        'price': 79,
        'category': 'หมวดบันทึกประจำวัน',
        'description': 'สมุดสำหรับจดบันทึกสิ่งที่ต้องทำรายวัน รายสัปดาห์ หรือรายเดือน ช่วยให้ไม่ลืมงานสำคัญและจัดลำดับความสำคัญได้ดี',
        'image': 'แพลนเนอร์ (Planner).png'
    },
    {
        'id': 2,
        'name': 'สมุดเช็คลิสต์ (Checklist Book)',
        'price': 49,
        'category': 'หมวดบันทึกประจำวัน',
        'description': 'สมุดสำหรับจดบันทึกสิ่งที่ต้องทำรายวัน รายสัปดาห์ หรือรายเดือน ช่วยให้ไม่ลืมงานสำคัญและจัดลำดับความสำคัญได้ดี',
        'image': 'สมุดเช็คลิสต์ (Checklist Book).png'
    },
    {
        'id': 3,
        'name': 'สมุดติดตามนิสัย (Habit Tracker)',
        'price': 39,
        'category': 'หมวดบันทึกประจำวัน',
        'description': 'ใช้บันทึกกิจกรรมซ้ำๆ ที่อยากทำเป็นประจำ',
        'image': 'สมุดติดตามนิสัย (Habit Tracker).png'
    },
    {
        'id': 4,
        'name': 'บันทึกความสุข (Gratitude Journal)',
        'price': 59,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดที่มี Template ให้เขียนขอบคุณเรื่องดีๆ 3 ข้อในแต่ละวัน',
        'image': 'บันทึกความสุข (Gratitude Journal).png'
    },
    {
        'id': 5,
        'name': 'สมุดระบายความคิด (Mind Dump Journal)',
        'price': 149,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดเส้นเปล่าสำหรับเขียนความรู้สึกทันทีหลังตื่นนอน เพื่อเคลียร์สมอง',
        'image': 'สมุดระบายความคิด (Mind Dump Journal).png'
    },
    {
        'id': 6,
        'name': 'บันทึกบรรทัดเดียวต่อวัน (One Line A Day)',
        'price': 79,
        'category': 'หมวดพัฒนาความคิดและจิตใจ',
        'description': 'สมุดที่ให้เขียนสั้นๆ เพียงวันละ 1-3 ประโยค ต่อเนื่องกันหลายปี (3-5 ปี)',
        'image': 'บันทึกบรรทัดเดียวต่อวัน (One Line A Day).png'
    },
    {
        'id': 7,
        'name': 'บันทึกการประชุม (Meeting Notes)',
        'price': 79,
        'category': 'หมวดงานและการเรียน',
        'description': 'มีช่องสำหรับเขียนหัวข้อ, ผู้เข้าร่วม, มติที่ประชุม และ Action Plan',
        'image': 'บันทึกการประชุม (Meeting Notes).png'
    },
    {
        'id': 8,
        'name': 'สมุดจดสรุป (Cornell Notebook)',
        'price': 79,
        'category': 'หมวดงานและการเรียน',
        'description': 'สมุดที่แบ่งหน้ากระดาษเป็น 3 ส่วน (จดโน้ต, คีย์เวิร์ด, สรุป) ตามหลักการเรียนรู้',
        'image': 'สมุดจดสรุป (Cornell Notebook).png'
    },
    {
        'id': 9,
        'name': 'สมุดตาราง (Grid/Square Notebook)',
        'price': 99,
        'category': 'หมวดงานและการเรียน',
        'description': 'เหมาะสำหรับสายคำนวณ วาดกราฟ หรือเขียนตัวอักษรภาษาจีน/ญี่ปุ่น',
        'image': 'สมุดตาราง (GridSquare Notebook).png'
    }
]

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        confirm_password = data.get('confirm_password', '')
        
        # ตรวจสอบความถูกต้อง
        if not email or not password or not name or not confirm_password:
            return jsonify({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'รหัสผ่านไม่ตรงกัน'})
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'})
        
        # ตรวจสอบรูปแบบอีเมล
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'message': 'รูปแบบอีเมลไม่ถูกต้อง'})
        
        if email in USERS:
            return jsonify({'success': False, 'message': 'อีเมลนี้ลงทะเบียนแล้ว'})
        
        # สร้างบัญชีใหม่
        USERS[email] = {
            'password': password,
            'name': name,
            'email': email
        }
        
        return jsonify({'success': True, 'message': 'ลงทะเบียนสำเร็จแล้ว กรุณาเข้าสู่ระบบ'})
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'กรุณากรอกอีเมลและรหัสผ่าน'})
        
        if email not in USERS:
            return jsonify({'success': False, 'message': 'ไม่พบผู้ใช้นี้'})
        
        user = USERS[email]
        if user['password'] != password:
            return jsonify({'success': False, 'message': 'รหัสผ่านไม่ถูกต้อง'})
        
        # บันทึกลงใน session
        session['user_email'] = email
        session['user_name'] = user['name']
        session['is_admin'] = user.get('is_admin', False)
        session.modified = True
        
        return jsonify({'success': True, 'message': 'เข้าสู่ระบบสำเร็จแล้ว'})
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/admin")
def admin():
    # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
    if not session.get('is_admin'):
        return redirect(url_for('home'))
    
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    cart_count = len(session.get('cart', []))
    
    return render_template('admin.html', 
                         products=PRODUCTS,
                         user_email=user_email,
                         user_name=user_name,
                         cart_count=cart_count)

@app.route("/api/upload", methods=['POST'])
def upload_file():
    # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิในการอัพโหลดไฟล์'})
    
    # ตรวจสอบว่าหมวดหมู่ไฟล์มีอยู่หรือไม่
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'ไม่พบไฟล์'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'ไม่ได้เลือกไฟล์'})
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'ประเภทไฟล์ไม่ถูกต้อง (รองรับ: png, jpg, jpeg, gif, webp)'})
    
    try:
        # สร้างชื่อไฟล์ที่ปลอดภัย
        filename = secure_filename(file.filename)
        # เพิ่มวันที่และเวลาเพื่อหลีกเลี่ยงการซ้ำกันของชื่อไฟล์
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S_')
        filename = timestamp + filename
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'message': 'อัพโหลดไฟล์สำเร็จ',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'})

@app.route("/api/product/add", methods=['POST'])
def add_product():
    # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิในการเพิ่มสินค้า'})
    
    data = request.get_json()
    
    # ตรวจสอบข้อมูล
    name = data.get('name', '').strip()
    price = data.get('price', 0)
    category = data.get('category', '').strip()
    description = data.get('description', '').strip()
    image = data.get('image', '').strip()
    
    if not name or price <= 0 or not category or not description:
        return jsonify({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วนและถูกต้อง'})
    
    try:
        price = float(price)
    except:
        return jsonify({'success': False, 'message': 'ราคาต้องเป็นตัวเลข'})
    
    # หาไอดีใหม่
    new_id = max([p['id'] for p in PRODUCTS]) + 1 if PRODUCTS else 1
    
    # เพิ่มสินค้าใหม่
    new_product = {
        'id': new_id,
        'name': name,
        'price': price,
        'category': category,
        'description': description,
        'image': image if image else 'default.png'
    }
    
    PRODUCTS.append(new_product)
    
    return jsonify({'success': True, 'message': 'เพิ่มสินค้าสำเร็จแล้ว', 'product': new_product})

@app.route("/api/product/delete", methods=['POST'])
def delete_product():
    # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิในการลบสินค้า'})
    
    data = request.get_json()
    product_id = data.get('id')
    
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p['id'] != product_id]
    
    return jsonify({'success': True, 'message': 'ลบสินค้าสำเร็จแล้ว'})

@app.route("/api/product/update", methods=['POST'])
def update_product():
    # ตรวจสอบว่าผู้ใช้เป็นแอดมินหรือไม่
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'ไม่มีสิทธิในการแก้ไขสินค้า'})
    
    data = request.get_json()
    product_id = data.get('id')
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'ไม่พบสินค้า'})
    
    # อัปเดตข้อมูล
    product['name'] = data.get('name', product['name']).strip()
    product['price'] = float(data.get('price', product['price']))
    product['category'] = data.get('category', product['category']).strip()
    product['description'] = data.get('description', product['description']).strip()
    product['image'] = data.get('image', product['image']).strip()
    
    return jsonify({'success': True, 'message': 'แก้ไขสินค้าสำเร็จแล้ว', 'product': product})

@app.route("/")
def home():
    category = request.args.get('category', 'ทั้งหมด')
    
    if category == 'ทั้งหมด':
        filtered_products = PRODUCTS
    else:
        filtered_products = [p for p in PRODUCTS if p['category'] == category]
    
    categories = ['ทั้งหมด', 'หมวดบันทึกประจำวัน', 'หมวดพัฒนาความคิดและจิตใจ', 'หมวดงานและการเรียน']
    cart_count = len(session.get('cart', []))
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    is_admin = session.get('is_admin', False)
    
    return render_template("home.html", 
                         products=filtered_products, 
                         categories=categories, 
                         current_category=category,
                         cart_count=cart_count,
                         user_email=user_email,
                         user_name=user_name,
                         is_admin=is_admin)

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
    
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    is_admin = session.get('is_admin', False)
    
    return render_template("cart.html", 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items),
                         user_email=user_email,
                         user_name=user_name,
                         is_admin=is_admin)

@app.route("/about")
def about():
    cart_count = len(session.get('cart', []))
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    is_admin = session.get('is_admin', False)
    return render_template("about.html", cart_count=cart_count, user_email=user_email, user_name=user_name, is_admin=is_admin)

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
    
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    is_admin = session.get('is_admin', False)
    
    return render_template("checkout.html", 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items),
                         user_email=user_email,
                         user_name=user_name,
                         is_admin=is_admin)

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