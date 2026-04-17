"""
generar_qr_ludolab_poker.py
===========================
Versión TAMAÑO POKER (2.5" × 3.5" @ 600 DPI = 1500 × 2100 px) de la carta QR
con configuración LudoLab (sin corona, banda "LudoLab.cl").

Uso:
    cd qr/
    python3 generar_qr_ludolab_poker.py             # default ["01"]
    python3 generar_qr_ludolab_poker.py 80 11 ...   # genera esos IDs
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os, math, sys

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR  = BASE_DIR

QR_BASE_URL = "https://misteriosdechile.com?id="

# ── Dimensiones (tamaño poker a 600 DPI) ─────────────────────────────────────
# Escala ≈ 2x respecto a la versión BIG (745×1040)
S = 2
W, H = 1500, 2100      # 2.5" × 3.5" @ 600 DPI

# ── Paleta ───────────────────────────────────────────────────────────────────
BG        = (8,   10, 20)
DARK_SLOT = (14,  18, 36)
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

FONT_MULT = 1.40
f_eyebrow = lf(SANS,    int(round(16 * FONT_MULT * S)))   # 44
f_special = lf(SANS_BD, int(round(14 * S)))               # 28
f_main    = lf(SERIF_BD, int(round(44 * S)))              # 88
f_footer  = lf(SANS_BD, int(round(18 * FONT_MULT * S)))   # 50

# ── Helpers ──────────────────────────────────────────────────────────────────
def rr(draw, xy, r, fill=None, outline=None, w=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def cx_text(draw, text, font, y, color, width=W):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (bb[2]-bb[0]))//2, y), text, font=font, fill=color)

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx,cy-size),(cx+size,cy),(cx,cy+size),(cx-size,cy)], fill=color)

def star_points(cx, cy, r_out, r_in, n=8):
    pts = []
    for i in range(n*2):
        angle = math.pi/n*i - math.pi/2
        r = r_out if i%2==0 else r_in
        pts.append((cx + r*math.cos(angle), cy + r*math.sin(angle)))
    return pts

def corner_ornament(draw, cx, cy, dx, dy, arm=40*S):
    draw.line([(cx,cy),(cx+dx*arm,cy)],      fill=GOLD,    width=2*S)
    draw.line([(cx,cy),(cx,cy+dy*arm)],      fill=GOLD,    width=2*S)
    draw.line([(cx,cy),(cx+dx*(arm//2),cy)], fill=GOLD_HI, width=1*S)
    draw.line([(cx,cy),(cx,cy+dy*(arm//2))], fill=GOLD_HI, width=1*S)
    pts = star_points(cx, cy, 10*S, 4*S, n=8)
    draw.polygon(pts, fill=GOLD)
    diamond(draw, cx+dx*(arm+7*S), cy, 5*S, GOLD_DIM)
    diamond(draw, cx, cy+dy*(arm+7*S), 5*S, GOLD_DIM)

def side_diamonds(draw, spacing=52*S):
    for y in range(spacing//2, H, spacing):
        diamond(draw, 9*S,   y, 3*S, GOLD_DIM)
        diamond(draw, W-9*S, y, 3*S, GOLD_DIM)
    for x in range(spacing//2, W, spacing):
        diamond(draw, x, 9*S,   3*S, GOLD_DIM)
        diamond(draw, x, H-9*S, 3*S, GOLD_DIM)

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
    IL, IR = 22*S, W-22*S

    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    rr(draw, [0,0,W-1,H-1],         r=22*S, fill=BG)
    rr(draw, [4*S,4*S,W-5*S,H-5*S], r=18*S, fill=None, outline=GOLD,    w=3*S)
    rr(draw, [10*S,10*S,W-11*S,H-11*S], r=13*S, fill=None, outline=GOLD_DIM, w=1*S)
    rr(draw, [14*S,14*S,W-15*S,H-15*S], r=10*S, fill=None, outline=GOLD_DK,  w=1*S)

    side_diamonds(draw, spacing=52*S)

    for (cx,cy),(dx,dy) in [((IL,18*S),(1,1)),((IR,18*S),(-1,1)),
                             ((IL,H-18*S),(1,-1)),((IR,H-18*S),(-1,-1))]:
        corner_ornament(draw, cx, cy, dx, dy)

    # (SIN corona)

    EYE_Y = 60*S
    cx_text(draw, "MISTERIOS DE CHILE  ·  VOLUMEN I", f_eyebrow, EYE_Y, MIST)
    LINE_Y = 94*S
    draw.line([(IL+10*S, LINE_Y),(IR-10*S, LINE_Y)], fill=GOLD_DIM, width=1*S)

    # Banda "LudoLab.cl"
    EDI_TOP, EDI_BOT = LINE_Y+6*S, LINE_Y+30*S
    rr(draw, [IL, EDI_TOP, IR, EDI_BOT], r=3*S, fill=(28,20,6), outline=GOLD_DIM, w=1*S)
    cx_text(draw, "★  LudoLab.cl  ★", f_special, EDI_TOP+4*S, GOLD)

    # Slot del QR
    QZ_TOP = EDI_BOT + 6*S
    QZ_BOT = H - 240*S
    rr(draw, [IL, QZ_TOP, IR, QZ_BOT], r=10*S, fill=DARK_SLOT, outline=GOLD, w=2*S)
    rr(draw, [IL+5*S, QZ_TOP+5*S, IR-5*S, QZ_BOT-5*S], r=7*S, fill=None, outline=GOLD_DK, w=1*S)
    for (px,py) in [(IL,QZ_TOP),(IR,QZ_TOP),(IL,QZ_BOT),(IR,QZ_BOT)]:
        diamond(draw, px, py, 7*S, GOLD)

    qr_size = min(IR-IL, QZ_BOT-QZ_TOP) - 32*S
    qr_img  = make_qr(url, qr_size, DARK_SLOT, GOLD)
    qr_x = (W-qr_size)//2
    qr_y = QZ_TOP + (QZ_BOT-QZ_TOP-qr_size)//2
    img.paste(qr_img, (qr_x, qr_y))

    # Separador
    SEP_Y = QZ_BOT + 18*S
    draw.line([(IL+10*S, SEP_Y),(IR-10*S, SEP_Y)], fill=GOLD, width=1*S)
    pts = star_points(W//2, SEP_Y, 9*S, 4*S, n=8)
    draw.polygon(pts, fill=GOLD)
    diamond(draw, W//2-28*S, SEP_Y, 4*S, GOLD_DIM)
    diamond(draw, W//2+28*S, SEP_Y, 4*S, GOLD_DIM)

    # "ESCANEA PARA / EL RELATO"
    for i, line in enumerate(["ESCANEA PARA", "EL RELATO"]):
        bb = draw.textbbox((0,0), line, font=f_main)
        draw.text(((W-(bb[2]-bb[0]))//2, SEP_Y+18*S+i*52*S), line, font=f_main, fill=GOLD_HI)

    # Footer
    FT_LINE = H - 60*S
    draw.line([(IL+10*S, FT_LINE),(IR-10*S, FT_LINE)], fill=GOLD, width=1*S)
    diamond(draw, W//2, FT_LINE, 5*S, GOLD)

    FT_BOX_TOP = FT_LINE + 4*S
    rr(draw, [IL, FT_BOX_TOP, IR, H-6*S], r=5*S, fill=(18,14,4), outline=GOLD_DIM, w=1*S)
    footer = f"ANVERSO  ·  ID {num}  ·  1536 – 1910"
    bb = draw.textbbox((0,0), footer, font=f_footer)
    box_h = (H-6*S) - FT_BOX_TOP
    ty = FT_BOX_TOP + (box_h - (bb[3]-bb[1]))//2 - bb[1]
    draw.text(((W-(bb[2]-bb[0]))//2, ty), footer, font=f_footer, fill=CREAM)

    out = os.path.join(OUT_DIR, f"carta_qr_{num}_poker.png")
    img.save(out, "PNG", dpi=(600,600))
    print(f"  OK  {out}  ({W}×{H} @ 600 DPI)")

# ── IDs A GENERAR ─────────────────────────────────────────────────────────────
IDS = ["01"]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    if len(sys.argv) > 1:
        IDS = sys.argv[1:]
    print(f"Generando {len(IDS)} QR POKER (LudoLab)...\n")
    for num in IDS:
        generar_qr(num)
    print("\nListo.")
