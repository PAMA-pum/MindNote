from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

# สร้างไดเรกทอรีถ้ายังไม่มี
os.makedirs('static/images', exist_ok=True)

def add_shadow(img):
    """เพิ่ม shadow effect ให้กับรูปภาพ"""
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    
    # สร้าง shadow ที่ด้านล่าง
    for i in range(20, 0, -1):
        alpha = int(20 * (1 - i/20))
        shadow_draw.rectangle(
            [(20, img.size[1] - i), (img.size[0] - 20, img.size[1] - i + 2)],
            fill=(0, 0, 0, alpha)
        )
    
    img.paste(shadow, (0, 0), shadow)
    return img

# =========================
# 1. MacBook Pro
# =========================
def create_macbook():
    img = Image.new('RGB', (300, 300), color=(230, 230, 235))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background gradient
    for y in range(300):
        r = int(230 - (y/300) * 20)
        g = int(230 - (y/300) * 20)
        b = int(235 - (y/300) * 10)
        draw.line([(0, y), (300, y)], fill=(r, g, b))
    
    # MacBook body
    draw.rounded_rectangle(
        [(40, 80), (260, 190)],
        radius=15,
        fill=(210, 210, 215),
        outline=(150, 150, 155),
        width=3
    )
    
    # Screen
    draw.rounded_rectangle(
        [(55, 90), (245, 170)],
        radius=10,
        fill=(20, 20, 30),
        outline=(80, 80, 90),
        width=2
    )
    
    # Screen glow
    draw.rectangle(
        [(58, 93), (242, 167)],
        fill=(45, 45, 60)
    )
    
    # Notch
    draw.rounded_rectangle(
        [(125, 95), (175, 108)],
        radius=4,
        fill=(15, 15, 20),
        outline=(60, 60, 70)
    )
    
    # Camera
    draw.ellipse([(146, 99), (154, 107)], fill=(30, 30, 40))
    draw.ellipse([(148, 101), (152, 105)], fill=(50, 50, 60))
    
    # Keyboard area
    draw.rectangle([(50, 175), (250, 220)], fill=(200, 200, 205))
    
    # Keys
    for x in range(70, 240, 20):
        for y in range(185, 210, 15):
            draw.rectangle([(x, y), (x+12, y+8)], fill=(180, 180, 190), outline=(160, 160, 170))
    
    # Trackpad
    draw.rounded_rectangle([(100, 215), (200, 235)], radius=3, fill=(170, 170, 180))
    
    # Dock indicator
    draw.line([(80, 250), (220, 250)], fill=(200, 200, 210), width=2)
    
    return img

# =========================
# 2. iPhone 15 Pro
# =========================
def create_iphone():
    img = Image.new('RGB', (300, 300), color=(240, 240, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    for y in range(300):
        r = int(240 - (y/300) * 15)
        g = int(240 - (y/300) * 15)
        b = int(245 - (y/300) * 20)
        draw.line([(0, y), (300, y)], fill=(r, g, b))
    
    # iPhone body - black
    draw.rounded_rectangle(
        [(70, 40), (230, 260)],
        radius=30,
        fill=(25, 25, 30),
        outline=(0, 0, 0),
        width=2
    )
    
    # Screen bezel
    draw.rounded_rectangle(
        [(75, 55), (225, 250)],
        radius=25,
        fill=(20, 20, 25),
        outline=(40, 40, 50)
    )
    
    # Screen display
    draw.rounded_rectangle(
        [(80, 60), (220, 245)],
        radius=22,
        fill=(30, 30, 40)
    )
    
    # Notch Dynamic Island
    draw.rounded_rectangle(
        [(110, 62), (190, 80)],
        radius=12,
        fill=(10, 10, 15),
        outline=(50, 50, 60)
    )
    
    # Status bar icons
    draw.text((95, 68), "5G 100%", fill=(100, 100, 100), font=None)
    
    # App icons
    colors = [(100, 150, 255), (255, 100, 150), (100, 255, 150), (255, 200, 100)]
    x_pos = [95, 140, 185]
    y_pos = [100, 140]
    
    for i, y in enumerate(y_pos):
        for j, x in enumerate(x_pos):
            draw.rounded_rectangle(
                [(x, y), (x+25, y+25)],
                radius=6,
                fill=colors[(i*3 + j) % len(colors)]
            )
    
    # Home indicator
    draw.rounded_rectangle(
        [(120, 240), (180, 244)],
        radius=2,
        fill=(150, 150, 160)
    )
    
    # Camera
    draw.ellipse([(85, 65), (92, 72)], fill=(40, 40, 50))
    draw.ellipse([(88, 68), (90, 70)], fill=(60, 60, 70))
    
    return img

# =========================
# 3. Canon EOS R5
# =========================
def create_camera():
    img = Image.new('RGB', (300, 300), color=(240, 240, 240))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    for y in range(300):
        shade = int(240 - (y/300) * 30)
        draw.line([(0, y), (300, y)], fill=(shade, shade, shade-10))
    
    # Camera body
    draw.rounded_rectangle(
        [(60, 80), (240, 200)],
        radius=12,
        fill=(50, 50, 55),
        outline=(20, 20, 25),
        width=2
    )
    
    # Top plate
    draw.rectangle([(65, 82), (235, 100)], fill=(60, 60, 65))
    
    # Main lens barrel - metallic
    for r in range(50, 20, -2):
        alpha = int(255 * (1 - (50-r)/30))
        draw.ellipse(
            [(150-r, 140-r), (150+r, 140+r)],
            fill=(80, 80, 85, alpha),
            outline=(70, 70, 75, alpha)
        )
    
    # Lens glass - reflective
    draw.ellipse([(115, 105), (185, 175)], fill=(40, 40, 45), outline=(100, 100, 110), width=2)
    draw.ellipse([(125, 115), (175, 165)], fill=(60, 60, 70))
    
    # Secondary lens
    draw.ellipse([(85, 140), (110, 165)], fill=(45, 45, 50), outline=(80, 80, 85), width=2)
    draw.ellipse([(90, 145), (105, 160)], fill=(65, 65, 75))
    
    # Flash
    draw.ellipse([(200, 140), (220, 160)], fill=(70, 70, 75), outline=(50, 50, 55), width=2)
    draw.rectangle([(205, 145), (215, 155)], fill=(90, 90, 100))
    
    # Shutter button
    draw.ellipse([(135, 105), (165, 135)], fill=(80, 80, 90), outline=(60, 60, 70), width=2)
    draw.ellipse([(140, 110), (160, 130)], fill=(100, 100, 110))
    
    return img

# =========================
# 4. iPad Air
# =========================
def create_ipad():
    img = Image.new('RGB', (300, 300), color=(245, 245, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    for y in range(300):
        shade = int(245 - (y/300) * 15)
        draw.line([(0, y), (300, y)], fill=(shade, shade, shade))
    
    # iPad body
    draw.rounded_rectangle(
        [(50, 30), (250, 270)],
        radius=18,
        fill=(225, 225, 230),
        outline=(180, 180, 190),
        width=3
    )
    
    # Screen
    draw.rounded_rectangle(
        [(62, 45), (238, 255)],
        radius=14,
        fill=(250, 250, 250),
        outline=(200, 200, 210),
        width=2
    )
    
    # App grid
    colors = [(100, 150, 255), (255, 100, 150), (100, 255, 150), 
              (255, 200, 100), (255, 150, 200), (150, 200, 255)]
    
    positions = [
        (75, 60), (130, 60), (185, 60),
        (75, 115), (130, 115), (185, 115)
    ]
    
    for pos, color in zip(positions, colors):
        draw.rounded_rectangle(
            [pos, (pos[0]+35, pos[1]+35)],
            radius=8,
            fill=color
        )
    
    # Status area
    draw.rectangle([(65, 50), (235, 58)], fill=(230, 230, 235))
    
    # Home indicator
    draw.rounded_rectangle(
        [(120, 250), (180, 253)],
        radius=2,
        fill=(200, 200, 210)
    )
    
    # Camera
    draw.ellipse([(145, 52), (155, 62)], fill=(80, 80, 90))
    draw.ellipse([(148, 55), (152, 59)], fill=(100, 100, 110))
    
    return img

# =========================
# 5. Sony Headphones
# =========================
def create_headphones():
    img = Image.new('RGB', (300, 300), color=(240, 240, 245))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    for y in range(300):
        shade = int(240 - (y/300) * 20)
        draw.line([(0, y), (300, y)], fill=(shade, shade, shade-5))
    
    # Left ear cup
    draw.ellipse([(60, 80), (120, 140)], fill=(60, 60, 65), outline=(30, 30, 35), width=2)
    draw.ellipse([(70, 90), (110, 130)], fill=(40, 40, 45))
    
    # Left speaker grill
    for i in range(4):
        draw.line([(75, 95+i*8), (105, 95+i*8)], fill=(80, 80, 90), width=1)
    
    # Right ear cup
    draw.ellipse([(180, 80), (240, 140)], fill=(60, 60, 65), outline=(30, 30, 35), width=2)
    draw.ellipse([(190, 90), (230, 130)], fill=(40, 40, 45))
    
    # Right speaker grill
    for i in range(4):
        draw.line([(195, 95+i*8), (225, 95+i*8)], fill=(80, 80, 90), width=1)
    
    # Headband - arc
    draw.arc(
        [(80, 30), (220, 120)],
        0, 180,
        fill=(50, 50, 60),
        width=14
    )
    draw.arc(
        [(82, 35), (218, 115)],
        0, 180,
        fill=(70, 70, 80),
        width=10
    )
    
    # Left arm
    draw.line([(80, 115), (70, 180)], fill=(50, 50, 60), width=10)
    draw.line([(80, 115), (70, 180)], fill=(65, 65, 75), width=6)
    
    # Right arm
    draw.line([(220, 115), (230, 180)], fill=(50, 50, 60), width=10)
    draw.line([(220, 115), (230, 180)], fill=(65, 65, 75), width=6)
    
    # Control button
    draw.ellipse([(235, 65), (250, 80)], fill=(80, 80, 90), outline=(50, 50, 60), width=1)
    draw.ellipse([(240, 70), (245, 75)], fill=(100, 100, 110))
    
    return img

# =========================
# 6. DJI Drone
# =========================
def create_drone():
    img = Image.new('RGB', (300, 300), color=(240, 245, 250))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background gradient (sky-like)
    for y in range(300):
        b = int(250 - (y/300) * 20)
        g = int(245 - (y/300) * 10)
        r = int(240 - (y/300) * 5)
        draw.line([(0, y), (300, y)], fill=(r, g, b))
    
    # Central body
    draw.ellipse([(120, 110), (180, 170)], fill=(45, 45, 50), outline=(20, 20, 25), width=2)
    
    # Camera gimbal
    draw.ellipse([(135, 155), (165, 180)], fill=(30, 30, 35), outline=(50, 50, 60), width=1)
    draw.ellipse([(140, 160), (160, 175)], fill=(60, 60, 70))
    
    # Camera lens
    draw.ellipse([(145, 164), (155, 174)], fill=(20, 20, 25))
    
    # Arms and motors
    motor_colors = [(200, 30, 50), (30, 100, 200), (200, 30, 50), (30, 100, 200)]
    arm_coords = [
        ((150, 130), (80, 70)),   # Front left (red)
        ((150, 130), (220, 70)),  # Front right (blue)
        ((150, 160), (80, 200)),  # Back left (red)
        ((150, 160), (220, 200))  # Back right (blue)
    ]
    
    for (start, end), color in zip(arm_coords, motor_colors):
        draw.line([start, end], fill=(50, 50, 55), width=8)
        draw.line([start, end], fill=(65, 65, 75), width=5)
        
        # Motor/propeller
        draw.ellipse(
            [(end[0]-10, end[1]-10), (end[0]+10, end[1]+10)],
            fill=(30, 30, 35),
            outline=(20, 20, 25),
            width=1
        )
        draw.ellipse(
            [(end[0]-7, end[1]-7), (end[0]+7, end[1]+7)],
            fill=color
        )
        
        # Propeller blades indication
        draw.line([(end[0]-5, end[1]), (end[0]+5, end[1])], fill=(100, 100, 110), width=1)
        draw.line([(end[0], end[1]-5), (end[0], end[1]+5)], fill=(100, 100, 110), width=1)
    
    # Vision system sensors
    draw.rectangle([(130, 145), (135, 150)], fill=(30, 150, 200))
    draw.rectangle([(165, 145), (170, 150)], fill=(30, 150, 200))
    
    # Status LED (green)
    draw.ellipse([(145, 105), (155, 115)], fill=(50, 200, 50))
    
    return img

# Create all images
print("🖼️  สร้างรูปภาพสินค้า...")

products = [
    ("product1.png", create_macbook, "MacBook Pro"),
    ("product2.png", create_iphone, "iPhone 15 Pro"),
    ("product3.png", create_camera, "Canon EOS R5"),
    ("product4.png", create_ipad, "iPad Air"),
    ("product5.png", create_headphones, "Sony WH-1000XM5"),
    ("product6.png", create_drone, "DJI Air 3S")
]

for filename, create_func, name in products:
    print(f"  ✓ สร้าง {name}...", end="")
    img = create_func()
    img = img.convert('RGB')
    img.save(f'static/images/{filename}', 'PNG', quality=95)
    print(" เสร็จสิ้น!")

print("\n✅ สร้างรูปภาพทั้งหมดเรียบร้อยแล้ว!")
print("📁 บันทึกไว้ใน: static/images/")
