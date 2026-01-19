from flask import Flask, render_template_string

app = Flask(__name__)

# ข้อมูลสินค้า (ตัวอย่าง)
products = [
    {"name": "เสื้อยืด", "price": 199, "image": "https://via.placeholder.com/150"},
    {"name": "กางเกงยีนส์", "price": 499, "image": "https://via.placeholder.com/150"},
    {"name": "รองเท้า", "price": 899, "image": "https://via.placeholder.com/150"},
]

html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ร้านค้าออนไลน์</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; }
        .container { width: 80%; margin: auto; }
        .product {
            background: white;
            padding: 15px;
            margin: 15px;
            display: inline-block;
            width: 200px;
            text-align: center;
            border-radius: 8px;
            box-shadow: 0 0 5px #ccc;
        }
        img { width: 150px; height: 150px; }
        button {
            background: green;
            color: white;
            border: none;
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 ร้านค้าออนไลน์</h1>
        {% for p in products %}
        <div class="product">
            <img src="{{ p.image }}">
            <h3>{{ p.name }}</h3>
            <p>ราคา {{ p.price }} บาท</p>
            <button>สั่งซื้อ</button>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html, products=products)

if __name__ == "__main__":
    app.run(debug=True)
