"""
generar_qr_premium.py
=====================
Genera las cartas QR PREMIUM (fondo negro/dorado) para Misterios de Chile.
Usa el mismo diseño exacto de las cartas QR 76-80.

DEPENDENCIAS:
    pip install pillow qrcode

USO:
    python generar_qr_premium.py

    Para agregar una carta nueva, agrega su ID al array IDS al final.
    El QR apuntará automáticamente a: https://misteriosdechile.com?id=XX

SALIDA:
    qr/carta_qr_XX.png   (745x1040 px, 150 dpi)
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os, math

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
OUT_DIR  = os.path.join(ROOT_DIR, "qr")

QR_BASE_URL = "https://misteriosdechile.com?id="

# ── Dimensiones ──────────────────────────────────────────────────────────────
W, H = 745, 1040

# ── Paleta premium ───────────────────────────────────────────────────────────
BG        = (8,  10, 20)
DARK_SLOT = (14, 18, 36)
GOLD_HI   = (255, 215, 80)
GOLD      = (210, 168, 52)
GOLD_DIM  = (160, 128, 38)
GOLD_DK   = (100,  78, 22)
CREAM     = (240, 220, 165)
MIST      = (160, 145, 110)

# ── Fuentes ──────────────────────────────────────────────────────────────────
def lf(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

SANS_BD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BD = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
if not os.path.exists(SERIF_BD):
    for p in ["/System/Library/Fonts/Times New Roman Bold.ttf",
              "/Library/Fonts/Times New Roman Bold.ttf", SANS_BD]:
        if os.path.exists(p): SERIF_BD = p; break

f_eyebrow = lf(SANS,    16)
f_special = lf(SANS_BD, 14)
f_main    = lf(SERIF_BD, 44)
f_footer  = lf(SANS_BD, 18)

# ── Helpers ──────────────────────────────────────────────────────────────────
def rr(draw, xy, r, fill=None, outline=None, w=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def cx_text(draw, text, font, y, color, width=W):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((width-(bb[2]-bb[0]))//2, y), text, font=font, fill=color)

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx,cy-size),(cx+size,cy),(cx,cy+size),(cx-size,cy)], fill=color)

def star_points(cx, cy, r_out, r_in, n=8):
    pts = []
    for i in range(n*2):
        angle = math.pi/n*i - math.pi/2
        r = r_out if i%2==0 else r_in
        pts.append((cx + r*math.cos(angle), cy + r*math.sin(angle)))
    return pts

def corner_ornament(draw, cx, cy, dx, dy, arm=40):
    draw.line([(cx,cy),(cx+dx*arm,cy)],      fill=GOLD, width=2)
    draw.line([(cx,cy),(cx,cy+dy*arm)],      fill=GOLD, width=2)
    draw.line([(cx,cy),(cx+dx*(arm//2),cy)], fill=GOLD_HI, width=1)
    draw.line([(cx,cy),(cx,cy+dy*(arm//2))], fill=GOLD_HI, width=1)
    pts = star_points(cx, cy, 10, 4, n=8)
    draw.polygon(pts, fill=GOLD)
    diamond(draw, cx+dx*(arm+7), cy, 5, GOLD_DIM)
    diamond(draw, cx, cy+dy*(arm+7), 5, GOLD_DIM)

def side_diamonds(draw, spacing=52):
    for y in range(spacing//2, H, spacing):
        diamond(draw, 9,   y, 3, GOLD_DIM)
        diamond(draw, W-9, y, 3, GOLD_DIM)
    for x in range(spacing//2, W, spacing):
        diamond(draw, x, 9,   3, GOLD_DIM)
        diamond(draw, x, H-9, 3, GOLD_DIM)

def draw_crown(draw, cx, top_y):
    bw, bh = 68, 20
    bx, by = cx-bw//2, top_y+26
    draw.rectangle([bx, by, bx+bw, by+bh], fill=GOLD)
    for px, ph in [(bx+4,16),(cx,24),(bx+bw-4,16)]:
        draw.polygon([(px-9,by),(px,by-ph),(px+9,by)], fill=GOLD)
    for px in [bx+12, cx, bx+bw-12]:
        draw.ellipse([(px-4,by+3),(px+4,by+11)], fill=BG, outline=GOLD_DIM, width=1)

def make_qr(url, size, bg, fg):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=fg, back_color=bg).convert("RGB").resize((size,size), Image.NEAREST)

# ── Función principal ─────────────────────────────────────────────────────────
def generar_qr(num):
    url = f"{QR_BASE_URL}{num}"
    IL, IR = 22, W-22

    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    rr(draw, [0,0,W-1,H-1], r=22, fill=BG)
    rr(draw, [4,4,W-5,H-5],     r=18, fill=None, outline=GOLD,    w=3)
    rr(draw, [10,10,W-11,H-11], r=13, fill=None, outline=GOLD_DIM,w=1)
    rr(draw, [14,14,W-15,H-15], r=10, fill=None, outline=GOLD_DK, w=1)

    side_diamonds(draw, spacing=52)

    for (cx,cy),(dx,dy) in [((IL,18),(1,1)),((IR,18),(-1,1)),
                             ((IL,H-18),(1,-1)),((IR,H-18),(-1,-1))]:
        corner_ornament(draw, cx, cy, dx, dy)

    draw_crown(draw, W//2, 6)

    cx_text(draw, "MISTERIOS DE CHILE  ·  VOLUMEN I", f_eyebrow, 58, MIST)
    draw.line([(IL+10, 80),(IR-10, 80)], fill=GOLD_DIM, width=1)

    rr(draw, [IL, 86, IR, 110], r=3, fill=(28,20,6), outline=GOLD_DIM, w=1)
    cx_text(draw, "★  EDICIÓN ESPECIAL  ★", f_special, 90, GOLD)

    QZ_TOP, QZ_BOT = 116, H-226
    rr(draw, [IL, QZ_TOP, IR, QZ_BOT], r=10, fill=DARK_SLOT, outline=GOLD, w=2)
    rr(draw, [IL+5, QZ_TOP+5, IR-5, QZ_BOT-5], r=7, fill=None, outline=GOLD_DK, w=1)
    for (px,py) in [(IL,QZ_TOP),(IR,QZ_TOP),(IL,QZ_BOT),(IR,QZ_BOT)]:
        diamond(draw, px, py, 7, GOLD)

    qr_size = min(IR-IL, QZ_BOT-QZ_TOP) - 32
    qr_img  = make_qr(url, qr_size, DARK_SLOT, GOLD)
    qr_x = (W-qr_size)//2
    qr_y = QZ_TOP + (QZ_BOT-QZ_TOP-qr_size)//2
    img.paste(qr_img, (qr_x, qr_y))

    SEP_Y = QZ_BOT + 18
    draw.line([(IL+10, SEP_Y),(IR-10, SEP_Y)], fill=GOLD, width=1)
    pts = star_points(W//2, SEP_Y, 9, 4, n=8)
    draw.polygon(pts, fill=GOLD)
    diamond(draw, W//2-28, SEP_Y, 4, GOLD_DIM)
    diamond(draw, W//2+28, SEP_Y, 4, GOLD_DIM)

    for i, line in enumerate(["ESCANEA PARA", "EL RELATO"]):
        bb = draw.textbbox((0,0), line, font=f_main)
        draw.text(((W-(bb[2]-bb[0]))//2, SEP_Y+24+i*56), line, font=f_main, fill=GOLD_HI)

    FT_LINE = H-52
    draw.line([(IL+10, FT_LINE),(IR-10, FT_LINE)], fill=GOLD, width=1)
    diamond(draw, W//2, FT_LINE, 5, GOLD)

    rr(draw, [IL, FT_LINE+4, IR, H-6], r=5, fill=(18,14,4), outline=GOLD_DIM, w=1)
    footer = f"ANVERSO  ·  ID {num}  ·  1536 – 1910"
    bb = draw.textbbox((0,0), footer, font=f_footer)
    draw.text(((W-(bb[2]-bb[0]))//2, FT_LINE+10), footer, font=f_footer, fill=CREAM)

    out = os.path.join(OUT_DIR, f"carta_qr_{num}.png")
    img.save(out, "PNG", dpi=(150,150))
    print(f"  ✅  {out}")

# ── IDs A GENERAR ─────────────────────────────────────────────────────────────
# Agrega aquí el ID de cada carta premium que quieras generar.
# El número debe coincidir con el ID en Firestore.

IDS = ["76", "77", "78", "79", "80"]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Generando {len(IDS)} QR premium...\n")
    for num in IDS:
        generar_qr(num)
    print(f"\n🏁 Listo.")
