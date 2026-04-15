"""
generar_carta_premium.py
========================
Genera cartas físicas PREMIUM (fondo negro/dorado) para Misterios de Chile.
Usa el mismo diseño exacto de las cartas 76-80.

DEPENDENCIAS:
    pip install pillow

USO:
    python generar_carta_premium.py

    Para agregar una carta nueva, agrega una entrada al array CARTAS al final
    del archivo y vuelve a ejecutar. Solo genera las cartas listadas.

SALIDA:
    cartas/id_XX_carta_v2.png   (750x1050 px, 150 dpi)
"""

from PIL import Image, ImageDraw, ImageFont
import os, math

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))   # misterios-seed/
ROOT_DIR  = os.path.dirname(BASE_DIR)                    # Juego Chile/
IMG_DIR   = os.path.join(ROOT_DIR, "imagenes")
OUT_DIR   = os.path.join(ROOT_DIR, "cartas")

# ── Dimensiones ──────────────────────────────────────────────────────────────
W, H = 750, 1050

# ── Paleta premium ───────────────────────────────────────────────────────────
BG         = (8,  10, 20)
DARK_SLATE = (14, 18, 36)
GOLD_HI    = (255, 215, 80)
GOLD       = (210, 168, 52)
GOLD_DIM   = (160, 128, 38)
GOLD_DK    = (100,  78, 22)
COPPER     = (185, 120, 45)
COPPER_DK  = (130,  80, 25)
CREAM      = (240, 220, 165)
CREAM_DIM  = (190, 168, 115)

# ── Zonas verticales ─────────────────────────────────────────────────────────
Y_CROWN   = 5
Y_YEAR    = 60
Y_SPEC    = 172
Y_TITLE   = 195
Y_TBOT    = 250
Y_IBOT    = 695
Y_TEXT    = 703
Y_FLINE   = H - 58
Y_FOOT    = H - 50
IL, IR    = 24, W - 24

# ── Fuentes ──────────────────────────────────────────────────────────────────
def lf(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

SANS_BD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BD = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
# macOS fallback
if not os.path.exists(SERIF_BD):
    for p in ["/System/Library/Fonts/Times New Roman Bold.ttf",
              "/Library/Fonts/Times New Roman Bold.ttf",
              SANS_BD]:
        if os.path.exists(p): SERIF_BD = p; break

f_year    = lf(SERIF_BD, 104)
f_special = lf(SANS_BD,  15)
f_title   = lf(SANS_BD,  26)
f_label   = lf(SANS_BD,  19)
f_body    = lf(SANS,     18)
f_footer  = lf(SANS_BD,  17)

# ── Helpers ──────────────────────────────────────────────────────────────────
def rr(draw, xy, r, fill=None, outline=None, w=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def cx_text(draw, text, font, y, color, width=W):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (bb[2]-bb[0])) // 2, y), text, font=font, fill=color)

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx,cy-size),(cx+size,cy),(cx,cy+size),(cx-size,cy)], fill=color)

def star_points(cx, cy, r_out, r_in, n=8):
    pts = []
    for i in range(n * 2):
        angle = math.pi / n * i - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts

def corner_ornament(draw, cx, cy, dx, dy, arm=44):
    draw.line([(cx, cy),(cx+dx*arm, cy)],     fill=GOLD, width=2)
    draw.line([(cx, cy),(cx, cy+dy*arm)],     fill=GOLD, width=2)
    draw.line([(cx, cy),(cx+dx*(arm//2), cy)],fill=GOLD_HI, width=1)
    draw.line([(cx, cy),(cx, cy+dy*(arm//2))],fill=GOLD_HI, width=1)
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

def wrap_draw(draw, text, font, x, y, max_w, lh, color):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0,0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    for i, line in enumerate(lines):
        draw.text((x, y + i*lh), line, font=font, fill=color)
    return y + len(lines) * lh

# ── Función principal ─────────────────────────────────────────────────────────
def generar_carta(card):
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    rr(draw, [0,0,W-1,H-1], r=18, fill=BG)

    # Triple marco
    rr(draw, [4,4,W-5,H-5],     r=18, fill=None, outline=GOLD,    w=3)
    rr(draw, [10,10,W-11,H-11], r=14, fill=None, outline=GOLD_DIM,w=1)
    rr(draw, [14,14,W-15,H-15], r=11, fill=None, outline=GOLD_DK, w=1)

    side_diamonds(draw, spacing=52)

    for (cx,cy),(dx,dy) in [((IL,18),(1,1)),((IR,18),(-1,1)),
                             ((IL,H-18),(1,-1)),((IR,H-18),(-1,-1))]:
        corner_ornament(draw, cx, cy, dx, dy)

    draw_crown(draw, W//2, Y_CROWN)

    # Año
    cx_text(draw, card["anio"], f_year, Y_YEAR, GOLD_HI)
    draw.line([(IL+20, Y_YEAR+108),(IR-20, Y_YEAR+108)], fill=GOLD_DIM, width=1)
    for px in [W//2-50, W//2, W//2+50]:
        diamond(draw, px, Y_YEAR+108, 4, GOLD)

    # Banda CARTA ESPECIAL
    rr(draw, [IL, Y_SPEC-2, IR, Y_SPEC+22], r=2,
       fill=(30,22,8), outline=GOLD_DIM, w=1)
    cx_text(draw, "✦  CARTA ESPECIAL  ✦", f_special, Y_SPEC+2, GOLD)

    # Banda título
    rr(draw, [IL, Y_TITLE, IR, Y_TBOT], r=4,
       fill=COPPER_DK, outline=COPPER, w=2)
    draw.line([(IL+6, Y_TITLE+4),(IR-6, Y_TITLE+4)], fill=COPPER, width=1)
    draw.line([(IL+6, Y_TBOT-4),(IR-6, Y_TBOT-4)], fill=COPPER, width=1)

    evento = card["evento"]
    f_ev = f_title
    while draw.textbbox((0,0), evento, font=f_ev)[2] > IR-IL-24 and f_ev.size > 15:
        f_ev = lf(SANS_BD, f_ev.size - 2)
    title_y = Y_TITLE + (Y_TBOT-Y_TITLE - (draw.textbbox((0,0),evento,font=f_ev)[3]-draw.textbbox((0,0),evento,font=f_ev)[1]))//2
    cx_text(draw, evento, f_ev, title_y, CREAM, W)

    # Imagen histórica
    img_path = os.path.join(IMG_DIR, card["img"])
    hist = Image.open(img_path).convert("RGB")
    IW, IH = IR-IL, Y_IBOT-Y_TBOT
    ratio = max(IW/hist.width, IH/hist.height)
    nw, nh = int(hist.width*ratio), int(hist.height*ratio)
    hist = hist.resize((nw, nh), Image.LANCZOS)
    cx2, cy2 = (nw-IW)//2, (nh-IH)//2
    hist = hist.crop((cx2, cy2, cx2+IW, cy2+IH))
    img.paste(hist, (IL, Y_TBOT))

    rr(draw, [IL, Y_TBOT, IR, Y_IBOT], r=0, fill=None, outline=GOLD, w=2)
    rr(draw, [IL+4, Y_TBOT+4, IR-4, Y_IBOT-4], r=0, fill=None, outline=GOLD_DK, w=1)
    for (px,py) in [(IL,Y_TBOT),(IR,Y_TBOT),(IL,Y_IBOT),(IR,Y_IBOT)]:
        diamond(draw, px, py, 6, GOLD)

    # Área de texto
    rr(draw, [IL, Y_TEXT, IR, Y_FLINE-4], r=6,
       fill=DARK_SLATE, outline=GOLD_DIM, w=1)
    TX, TW = IL+16, IR-IL-32
    ty = Y_TEXT + 14
    draw.text((TX, ty), "DESCRIPCIÓN:", font=f_label, fill=GOLD)
    ty += 25
    ty = wrap_draw(draw, card["desc"], f_body, TX, ty, TW, 21, CREAM_DIM) + 10
    draw.text((TX, ty), "PERSONAJES:", font=f_label, fill=GOLD)
    ty += 23
    wrap_draw(draw, card["personajes"], f_body, TX, ty, TW, 21, CREAM)

    # Footer
    draw.line([(IL, Y_FLINE),(IR, Y_FLINE)], fill=GOLD, width=2)
    rr(draw, [IL, Y_FOOT, IR, H-6], r=5, fill=(18,14,4), outline=GOLD_DIM, w=1)
    draw.text((IL+12, Y_FOOT+6), f"ID {card['num']}", font=f_footer, fill=GOLD_HI)
    cx_text(draw, "★  EDICIÓN ESPECIAL  ★", f_footer, Y_FOOT+6, GOLD, W)
    dif_txt = f"◆ {card['dif']}"
    bb = draw.textbbox((0,0), dif_txt, font=f_footer)
    draw.text((IR-(bb[2]-bb[0])-12, Y_FOOT+6), dif_txt, font=f_footer, fill=GOLD_HI)

    out = os.path.join(OUT_DIR, f"id_{card['num']}_carta_v2.png")
    img.save(out, "PNG", dpi=(150, 150))
    print(f"  ✅  {out}")

# ── CARTAS A GENERAR ─────────────────────────────────────────────────────────
# Para agregar una carta nueva, copia el bloque y rellena los campos.
# "num"        → ID de 2 dígitos (ej: "81")
# "anio"       → Año del evento (ej: "1920")
# "evento"     → Título en MAYÚSCULAS (ej: "NOMBRE DEL EVENTO")
# "img"        → Nombre del archivo en imagenes/ (con extensión)
# "desc"       → Descripción para la carta (máx ~300 caracteres)
# "personajes" → Nombres separados por · o coma
# "dif"        → "Fácil", "Media" o "Difícil"

CARTAS = [
    {
        "num": "76", "anio": "1879", "evento": "COMBATE NAVAL DE IQUIQUE",
        "img": "id_76_combate_naval_de_iquique.png",
        "desc": "Fue una batalla naval crucial donde la corbeta Esmeralda fue hundida por el blindado Huáscar. El comandante Arturo Prat se negó a rendirse, transformándose en el héroe naval más importante de la historia chilena.",
        "personajes": "Arturo Prat · Miguel Grau", "dif": "Fácil",
    },
    {
        "num": "77", "anio": "1880", "evento": "CUESTIÓN SOCIAL",
        "img": "id_77_cuestion_social.png",
        "desc": "Miles de familias obreras vivían hacinadas sin agua potable ni atención médica, mientras el país producía una riqueza enorme con el salitre. El despertar de la clase trabajadora cambiaría para siempre la política chilena.",
        "personajes": "Luis Emilio Recabarren", "dif": "Fácil",
    },
    {
        "num": "78", "anio": "1823", "evento": "CONSTITUCIÓN MORALISTA",
        "img": "id_78_constitucion_moralista_1823.png",
        "desc": "Un documento tan exigente que pretendía regular hasta los hábitos privados de los ciudadanos, premiando la virtud y castigando el vicio. Fue inejecutable y abandonada en menos de un año.",
        "personajes": "Juan Egaña", "dif": "Media",
    },
    {
        "num": "79", "anio": "1828", "evento": "CONSTITUCIÓN LIBERAL",
        "img": "id_79_constitucion_liberal_1828.png",
        "desc": "Texto de ideario liberal que fortaleció al Poder Legislativo, consagró derechos individuales y estableció un sistema descentralizado. Fue derrocada por los conservadores tras la batalla de Lircay.",
        "personajes": "Francisco Antonio Pinto · Melchor de Santiago Concha", "dif": "Media",
    },
    {
        "num": "80", "anio": "1833", "evento": "CONSTITUCIÓN DE 1833",
        "img": "id_80_constitucion_de_1833.png",
        "desc": "Marcó el inicio de la estabilidad republicana con un ejecutivo poderoso, posibilidad de reelección y voto censitario. Reconoció la religión católica como oficial del Estado. Rigió por casi cien años.",
        "personajes": "Diego Portales · Mariano Egaña · Manuel José Gandarillas", "dif": "Media",
    },
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Generando {len(CARTAS)} carta(s) premium...\n")
    for card in CARTAS:
        generar_carta(card)
    print(f"\n🏁 Listo.")
