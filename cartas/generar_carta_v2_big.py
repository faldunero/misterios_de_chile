"""
generar_id_01_big.py
=====================
Genera id_01_carta_v2_big.png en alta calidad (300 dpi, 2× resolución)
con textos 43% más grandes que el original (30% + 10% adicional),
excepto año y título. Diseño limpio sin corona/carta especial/edición especial.
"""

from PIL import Image, ImageDraw, ImageFont
import os, math

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))   # cartas/
ROOT_DIR  = os.path.dirname(BASE_DIR)                    # Juego Chile/
IMG_DIR   = os.path.join(ROOT_DIR, "imagenes")
OUT_DIR   = BASE_DIR                                     # guarda en cartas/

# ── Escala de calidad ────────────────────────────────────────────────────────
SCALE = 2          # 2× resolución → 1500×2100 px a 300 dpi (impresión premium)
FONT_MULT = 1.43   # 1.3 (30%) × 1.1 (10% adicional)

def S(v):
    return int(round(v * SCALE))

# ── Dimensiones ──────────────────────────────────────────────────────────────
W, H = S(750), S(1050)

# ── Paleta ───────────────────────────────────────────────────────────────────
BG         = (28,  70, 45)      # verde fondo
DARK_SLATE = (235, 218, 180)    # beige área de textos
GOLD_HI    = (255, 215, 80)
GOLD       = (210, 168, 52)
GOLD_DIM   = (160, 128, 38)
GOLD_DK    = (100,  78, 22)
COFFEE_DK  = ( 45,  25, 12)     # banda título
COFFEE_MED = ( 95,  55, 25)
CREAM      = (240, 220, 165)
LABEL_DK   = (110,  65, 20)
BODY_DK    = ( 70,  45, 20)
NAME_DK    = ( 45,  28, 10)

# ── Zonas verticales (aprovechando todo el espacio) ──────────────────────────
Y_YEAR    = S(35)       # subido (antes 60) para aprovechar espacio superior
Y_DIV     = S(150)      # línea bajo año
Y_TITLE   = S(170)
Y_TBOT   = S(232)
Y_IBOT    = S(600)      # imagen ajustada para dar espacio al texto ampliado
Y_TEXT    = S(608)
Y_FLINE   = H - S(108)
Y_FOOT    = H - S(100)
Y_FEND    = H - S(60)
IL, IR    = S(24), W - S(24)

# ── Fuentes ──────────────────────────────────────────────────────────────────
def lf(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

SANS_BD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS     = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF_BD = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
if not os.path.exists(SERIF_BD):
    for p in ["/System/Library/Fonts/Times New Roman Bold.ttf",
              "/Library/Fonts/Times New Roman Bold.ttf",
              SANS_BD]:
        if os.path.exists(p): SERIF_BD = p; break

# Año y título: solo escala de calidad (sin 43%)
f_year    = lf(SERIF_BD, S(104))
f_title   = lf(SANS_BD,  S(26))
# Resto: +43% (30% + 10% adicional) × escala de calidad
f_label   = lf(SANS_BD,  int(round(19 * FONT_MULT * SCALE)))
f_body    = lf(SANS,     int(round(18 * FONT_MULT * SCALE)))
f_footer  = lf(SANS_BD,  int(round(17 * FONT_MULT * SCALE)))
BODY_LH   = int(round(21 * FONT_MULT * SCALE))

# ── Helpers ──────────────────────────────────────────────────────────────────
def rr(draw, xy, r, fill=None, outline=None, w=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def cx_text(draw, text, font, y, color, width=None):
    if width is None: width = W
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

def corner_ornament(draw, cx, cy, dx, dy, arm=None):
    if arm is None: arm = S(44)
    draw.line([(cx, cy),(cx+dx*arm, cy)],     fill=GOLD,    width=S(2))
    draw.line([(cx, cy),(cx, cy+dy*arm)],     fill=GOLD,    width=S(2))
    draw.line([(cx, cy),(cx+dx*(arm//2), cy)],fill=GOLD_HI, width=S(1))
    draw.line([(cx, cy),(cx, cy+dy*(arm//2))],fill=GOLD_HI, width=S(1))
    pts = star_points(cx, cy, S(10), S(4), n=8)
    draw.polygon(pts, fill=GOLD)
    diamond(draw, cx+dx*(arm+S(7)), cy, S(5), GOLD_DIM)
    diamond(draw, cx, cy+dy*(arm+S(7)), S(5), GOLD_DIM)

def side_diamonds(draw, spacing=None):
    if spacing is None: spacing = S(52)
    for y in range(spacing//2, H, spacing):
        diamond(draw, S(9),     y, S(3), GOLD_DIM)
        diamond(draw, W-S(9),   y, S(3), GOLD_DIM)
    for x in range(spacing//2, W, spacing):
        diamond(draw, x, S(9),   S(3), GOLD_DIM)
        diamond(draw, x, H-S(9), S(3), GOLD_DIM)

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

def count_wrap_lines(draw, text, font, max_w):
    words = text.split()
    lines, cur = 0, ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0,0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur: lines += 1
            cur = w
    if cur: lines += 1
    return max(lines, 1)

def fit_body_font(draw, card, TW, available_h):
    """Busca el tamaño de fuente más grande (hasta FONT_MULT) que permita
    que DESCRIPCIÓN + PERSONAJES entren en el área disponible sin cortarse."""
    label_advance_1 = int(round(25 * FONT_MULT * SCALE))  # espacio bajo "DESCRIPCIÓN:"
    label_advance_2 = int(round(23 * FONT_MULT * SCALE))  # espacio bajo "PERSONAJES:"
    gap_between    = S(10)
    for mult in [FONT_MULT, 1.38, 1.33, 1.28, 1.23, 1.18, 1.13, 1.08, 1.03, 1.0]:
        body_sz = int(round(18 * mult * SCALE))
        lh      = int(round(21 * mult * SCALE))
        f_b     = lf(SANS, body_sz)
        d_lines = count_wrap_lines(draw, card["desc"], f_b, TW)
        p_lines = count_wrap_lines(draw, card["personajes"], f_b, TW)
        total = label_advance_1 + d_lines*lh + gap_between + label_advance_2 + p_lines*lh
        if total <= available_h:
            return f_b, lh
    return f_b, lh  # última intentada (más pequeña)

# ── Función principal ─────────────────────────────────────────────────────────
def generar_carta(card, out_name):
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    rr(draw, [0,0,W-1,H-1], r=S(18), fill=BG)

    # Triple marco
    rr(draw, [S(4), S(4), W-S(5), H-S(5)],     r=S(18), fill=None, outline=GOLD,    w=S(3))
    rr(draw, [S(10),S(10),W-S(11),H-S(11)],    r=S(14), fill=None, outline=GOLD_DIM,w=S(1))
    rr(draw, [S(14),S(14),W-S(15),H-S(15)],    r=S(11), fill=None, outline=GOLD_DK, w=S(1))

    side_diamonds(draw)

    for (cx,cy),(dx,dy) in [((IL,S(18)),(1,1)),((IR,S(18)),(-1,1)),
                             ((IL,H-S(18)),(1,-1)),((IR,H-S(18)),(-1,-1))]:
        corner_ornament(draw, cx, cy, dx, dy)

    # Año
    cx_text(draw, card["anio"], f_year, Y_YEAR, GOLD_HI)
    draw.line([(IL+S(20), Y_DIV),(IR-S(20), Y_DIV)], fill=GOLD_DIM, width=S(1))
    for px in [W//2-S(50), W//2, W//2+S(50)]:
        diamond(draw, px, Y_DIV, S(4), GOLD)

    # Banda título (café oscuro)
    rr(draw, [IL, Y_TITLE, IR, Y_TBOT], r=S(4),
       fill=COFFEE_DK, outline=COFFEE_MED, w=S(2))
    draw.line([(IL+S(6), Y_TITLE+S(4)),(IR-S(6), Y_TITLE+S(4))], fill=COFFEE_MED, width=S(1))
    draw.line([(IL+S(6), Y_TBOT-S(4)),(IR-S(6), Y_TBOT-S(4))],   fill=COFFEE_MED, width=S(1))

    evento = card["evento"]
    f_ev = f_title
    while draw.textbbox((0,0), evento, font=f_ev)[2] > IR-IL-S(24) and f_ev.size > S(15):
        f_ev = lf(SANS_BD, f_ev.size - S(2))
    title_y = Y_TITLE + (Y_TBOT-Y_TITLE - (draw.textbbox((0,0),evento,font=f_ev)[3]-draw.textbbox((0,0),evento,font=f_ev)[1]))//2
    cx_text(draw, evento, f_ev, title_y, CREAM)

    # Imagen histórica (contain: muestra imagen completa con fondo café
    # oscuro alrededor si la proporción no coincide con la zona destino)
    img_path = os.path.join(IMG_DIR, card["img"])
    hist = Image.open(img_path).convert("RGB")
    IW, IH = IR-IL, Y_IBOT-Y_TBOT
    ratio = min(IW/hist.width, IH/hist.height)  # contain
    nw, nh = int(hist.width*ratio), int(hist.height*ratio)
    hist = hist.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (IW, IH), COFFEE_DK)
    ox, oy = (IW-nw)//2, (IH-nh)//2
    canvas.paste(hist, (ox, oy))
    img.paste(canvas, (IL, Y_TBOT))

    rr(draw, [IL, Y_TBOT, IR, Y_IBOT], r=0, fill=None, outline=GOLD,    w=S(2))
    rr(draw, [IL+S(4), Y_TBOT+S(4), IR-S(4), Y_IBOT-S(4)], r=0, fill=None, outline=GOLD_DK, w=S(1))
    for (px,py) in [(IL,Y_TBOT),(IR,Y_TBOT),(IL,Y_IBOT),(IR,Y_IBOT)]:
        diamond(draw, px, py, S(6), GOLD)

    # Área de texto (beige) — ajuste automático de fuente si no entra el texto
    rr(draw, [IL, Y_TEXT, IR, Y_FLINE-S(4)], r=S(6),
       fill=DARK_SLATE, outline=GOLD_DIM, w=S(1))
    TX, TW = IL+S(16), IR-IL-S(32)
    ty_start = Y_TEXT + S(14)
    available_h = (Y_FLINE - S(4)) - ty_start - S(6)
    f_body_fit, lh_fit = fit_body_font(draw, card, TW, available_h)

    ty = ty_start
    draw.text((TX, ty), "DESCRIPCIÓN:", font=f_label, fill=LABEL_DK)
    ty += int(round(25 * FONT_MULT * SCALE))
    ty = wrap_draw(draw, card["desc"], f_body_fit, TX, ty, TW, lh_fit, BODY_DK) + S(10)
    draw.text((TX, ty), "PERSONAJES:", font=f_label, fill=LABEL_DK)
    ty += int(round(23 * FONT_MULT * SCALE))
    wrap_draw(draw, card["personajes"], f_body_fit, TX, ty, TW, lh_fit, NAME_DK)

    # Footer — beige, mismo estilo que descripción
    draw.line([(IL, Y_FLINE),(IR, Y_FLINE)], fill=GOLD, width=S(2))
    rr(draw, [IL, Y_FOOT, IR, Y_FEND], r=S(5), fill=DARK_SLATE, outline=GOLD_DIM, w=S(1))
    foot_ty = Y_FOOT + (Y_FEND - Y_FOOT - f_footer.size) // 2
    draw.text((IL+S(14), foot_ty), f"ID {card['num']}", font=f_footer, fill=BODY_DK)
    dif_txt = f"DIFICULTAD: {card['dif']}"
    bb = draw.textbbox((0,0), dif_txt, font=f_footer)
    draw.text((IR-(bb[2]-bb[0])-S(14), foot_ty), dif_txt, font=f_footer, fill=BODY_DK)

    # Tamaño poker: 2.5" x 3.5" = 63.5 x 88.9 mm
    # 1500 x 2100 px @ 600 dpi = exactamente tamaño poker en altísima calidad
    out = os.path.join(OUT_DIR, out_name)
    img.save(out, "PNG", dpi=(600, 600))
    print(f"  OK  {out}  ({W}x{H} @ 600 dpi -> 2.5\" x 3.5\" poker size)")

# ── CARTAS A GENERAR ─────────────────────────────────────────────────────────
# Datos: "num", "anio" (del año solo dígitos), "evento" (MAYÚSCULAS),
#        "img" (nombre archivo en imagenes/), "desc", "personajes", "dif".

CARTAS = [
    {
        "num": "01", "anio": "1536", "evento": "EXPEDICIÓN DE ALMAGRO",
        "img": "id_01_expedicion_almagro.png",
        "desc": "Diego de Almagro salió del Cusco buscando oro y riquezas. Cruzó la helada Cordillera de los Andes, donde muchos de sus hombres sufrieron por el frío. Al llegar al valle de Copiapó en 1536, se dio cuenta de que no había el oro que buscaba y decidió regresar, siendo el primero en explorar Chile.",
        "personajes": "Diego de Almagro", "dif": "Media",
    },
    {
        "num": "02", "anio": "1541", "evento": "FUNDACIÓN DE SANTIAGO",
        "img": "id_02_fundacion_de_santiago.png",
        "desc": "Pedro de Valdivia fundó la ciudad el 12 de febrero de 1541 al pie del cerro Huelén. Eligió este lugar porque los brazos del río Mapocho permitían defender mejor la aldea. Fue el punto de partida para organizar la vida española y construir las primeras casas, calles y la Plaza de Armas.",
        "personajes": "Pedro de Valdivia, Inés de Suárez", "dif": "Fácil",
    },
    {
        "num": "03", "anio": "1541", "evento": "DESTRUCCIÓN DE SANTIAGO",
        "img": "id_03_destruccion_de_santiago.png",
        "desc": "En septiembre de 1541, el cacique Michimalonco lideró a miles de guerreros para atacar la joven ciudad. Santiago fue incendiada y quedó casi en ruinas. La resistencia de los españoles, liderada por Inés de Suárez, fue clave para que no abandonaran Chile y lograran reconstruir lo perdido.",
        "personajes": "Michimalonco, Inés de Suárez", "dif": "Difícil",
    },
    {
        "num": "04", "anio": "1550", "evento": "FUNDACIÓN DE CONCEPCIÓN",
        "img": "id_04_fundacion_de_concepcion.png",
        "desc": "Pedro de Valdivia fundó esta ciudad en 1550 a orillas de la bahía de Penco. Su objetivo era establecer una base militar para avanzar hacia el sur y controlar el territorio cerca del río Biobío. Se transformó en un lugar clave para la defensa y el comercio durante la Colonia.",
        "personajes": "Pedro de Valdivia, Jerónimo de Alderete", "dif": "Media",
    },
    {
        "num": "05", "anio": "1553", "evento": "BATALLA DE TUCAPEL",
        "img": "id_05_batalla_de_tucapel.png",
        "desc": "Fue una victoria decisiva de los mapuches en 1553. Lautaro, usando sus brillantes tácticas, logró matar y derrotar a las fuerzas españolas. En este combate capturaron y dieron muerte al gobernador Pedro de Valdivia, lo que produjo un grave temor en los colonizadores y cambió el rumbo de la conquista.",
        "personajes": "Lautaro, Pedro de Valdivia, Caupolicán", "dif": "Media",
    },
    {
        "num": "06", "anio": "1557", "evento": "BATALLA DE LAGUNILLAS",
        "img": "id_06_batalla_de_lagunillas.png",
        "desc": "En 1557, los españoles y mapuches se enfrentaron cerca de lagunas en el sur. Fue una batalla muy feroz donde los españoles usaron sus caballos para romper las líneas indígenas. Aquí fue capturado el guerrero Galvarino, a quien le cortaron las manos como castigo, convirtiéndose en un símbolo de valor.",
        "personajes": "García Hurtado de Mendoza, Galvarino", "dif": "Difícil",
    },
    {
        "num": "07", "anio": "1598", "evento": "DESASTRE DE CURALABA",
        "img": "id_07_desastre_de_curalaba.png",
        "desc": "Ocurrió en 1598, fue un gran levantamiento mapuche liderado por Pelantaro. Sorprendieron al gobernador Óñez de Loyola mientras dormía, derrotando a sus tropas. Obligó a los españoles a abandonar todas las ciudades al sur del río Biobío, marcando el fin de la Conquista y el inicio de la Colonia.",
        "personajes": "Pelantaro, Martín García Óñez de Loyola", "dif": "Difícil",
    },
    {
        "num": "08", "anio": "1600", "evento": "REAL SITUADO",
        "img": "id_08_real_situado.png",
        "desc": "Era un cargamento de dinero, ropa y alimentos enviado anualmente desde el Virreinato del Perú hacia Chile. Su fin era pagar los sueldos de los soldados del ejército profesional. Esta ayuda era clave para mantener la defensa del reino, ya que Chile no tenía recursos suficientes para costear la guerra por sí solo.",
        "personajes": "Rey de España, Virrey del Perú, Soldados del ejército profesional", "dif": "Difícil",
    },
    {
        "num": "09", "anio": "1608", "evento": "ESCLAVITUD INDÍGENA",
        "img": "id_09_esclavitud_indigena.png",
        "desc": "Durante un tiempo, una ley permitió capturar como esclavos a los indígenas que luchaban contra los españoles. Esto se hizo para obligarlos a trabajar en minas y campos. Fue una época muy dura y triste, ya que no se respetaban sus derechos básicos ni su libertad.",
        "personajes": "Gobernador Alonso de Ribera, Rey Felipe III", "dif": "Media",
    },
    {
        "num": "10", "anio": "1641", "evento": "PARLAMENTO DE QUILÍN",
        "img": "id_10_parlamento_de_quilin.png",
        "desc": "Fue una gran reunión de paz en 1641. El Gobernador y los jefes mapuches se juntaron para conversar, comer y dar regalos. Por primera vez, los españoles aceptaron que los mapuches eran libres y dueños de las tierras al sur del río Biobío, tratando de frenar las batallas.",
        "personajes": "Marqués de Baides, Jefes Mapuches (Toquis)", "dif": "Media",
    },
    {
        "num": "11", "anio": "1647", "evento": "EL TERREMOTO MAGNO",
        "img": "id_11_el_terremoto_magno.png",
        "desc": "En 1647, un terremoto gigante destruyó casi todo Santiago. Las casas de barro se cayeron y la ciudad quedó en ruinas. Fue un momento de mucho miedo donde la gente sufrió mucho y pensaron que todo había sido un castigo de la naturaleza.",
        "personajes": "Gobernador Martín de Mujica, Obispo Gaspar de Villarroel", "dif": "Fácil",
    },
    {
        "num": "12", "anio": "1700", "evento": "EL INQUILINO",
        "img": "id_12_el_inquilino.png",
        "desc": "Era un campesino que vivía con su familia dentro de una gran hacienda. El dueño le prestaba un pedazo de tierra para vivir y cultivar comida; a cambio, el inquilino debía trabajar para el patrón en las tierras del campo, como los sembríos y las cosechas.",
        "personajes": "El Patrón de fundo, El Inquilino", "dif": "Fácil",
    },
    {
        "num": "13", "anio": "1767", "evento": "EXPULSIÓN JESUITAS",
        "img": "id_13_expulsion_jesuita.png",
        "desc": "Los Jesuitas eran sacerdotes muy educados que tenían colegios y haciendas modernas. En 1767, el Rey de España ordenó que se fueran de Chile para siempre. Esto causó gran impacto porque eran muy queridos y ayudaban mucho en la educación y la economía del país.",
        "personajes": "Rey Carlos III, Sacerdotes Jesuitas", "dif": "Media",
    },
    {
        "num": "14", "anio": "1791", "evento": "ABOLICIÓN ENCOMIENDA",
        "img": "id_14_abolicion_encomienda.png",
        "desc": "El Gobernador Ambrosio O'Higgins decidió terminar con la encomienda porque había muchos abusos. Con esta ley, los indígenas ya no estaban obligados a trabajar gratis para los españoles, permitiendo que fueran personas más libres y recibieran un trato más justo.",
        "personajes": "Ambrosio O'Higgins", "dif": "Difícil",
    },
    {
        "num": "15", "anio": "1792", "evento": "CAMINO SANTIAGO-VALPARAÍSO",
        "img": "id_15_camino_santiago_valparaiso.png",
        "desc": "Fue una de las obras más importantes de la Colonia para conectar la capital con el mar. Gracias a este camino, las carretas podían transportar productos y noticias que llegaban directamente al puerto. Fue clave para el comercio y el crecimiento de Chile en aquella época.",
        "personajes": "Ambrosio O'Higgins, Ingenieros coloniales", "dif": "Media",
    },
    {
        "num": "16", "anio": "1810", "evento": "PRIMERA JUNTA DE GOBIERNO",
        "img": "id_16_primera_junta_de_gobierno.png",
        "desc": "El 18 de septiembre de 1810, los vecinos se reunieron para decidir cómo gobernar mientras el Rey estaba preso. No fue la independencia total, sino el primer gran paso donde los chilenos empezaron a tomar sus propias decisiones y a soñar con un país libre.",
        "personajes": "Mateo de Toro y Zambrano, Juan Martínez de Rozas", "dif": "Fácil",
    },
    {
        "num": "17", "anio": "1811", "evento": "PRIMER CONGRESO NACIONAL",
        "img": "id_17_primer_congreso_nacional.png",
        "desc": "Se creó en 1811 para que representantes de todo Chile pudieran discutir y crear leyes propias. Fue una asamblea muy importante donde se buscaba que el poder ya no estuviera en una sola persona, sino en un grupo que representara los deseos de la gente de la época.",
        "personajes": "Juan Antonio Ovalle, José Miguel Carrera", "dif": "Media",
    },
    {
        "num": "18", "anio": "1811", "evento": "LIBERTAD DE VIENTRE",
        "img": "id_18_libertad_de_vientres.png",
        "desc": "Fue una ley muy valiente que decía que todos los hijos de esclavos que nacieran en Chile serían libres. Gracias a esta medida, impulsada por Manuel de Salas, nuestro país se convirtió en uno de los primeros del mundo en avanzar hacia el fin de la esclavitud.",
        "personajes": "Manuel de Salas, José Miguel Carrera", "dif": "Media",
    },
    {
        "num": "19", "anio": "1812", "evento": "LA AURORA DE CHILE",
        "img": "id_19_la_aurora_de_chile.png",
        "desc": "Fue el primer periódico de nuestra historia. Fray Camilo Henríquez lo fundó para explicar a las personas por qué era importante la libertad. A través de sus páginas, las ideas patriotas se repartieron por todo el país, motivando a muchos a luchar por la patria.",
        "personajes": "Fray Camilo Henríquez", "dif": "Fácil",
    },
    {
        "num": "20", "anio": "1812", "evento": "REGLAMENTO CONSTITUCIONAL",
        "img": "id_20_reglamento_constitucional.png",
        "desc": "Creado en 1812, fue un conjunto de reglas que decía que aunque el Rey fuera el jefe, debía respetar las leyes chilenas. También estableció que ningún país extranjero podía dar órdenes en nuestra Colonia, marcando un camino claro hacia una nación soberana y distinta.",
        "personajes": "José Miguel Carrera", "dif": "Difícil",
    },
    {
        "num": "21", "anio": "1813", "evento": "FUNDACIÓN INST. NACIONAL",
        "img": "id_21_instituto_nacional.png",
        "desc": "Se fundó para entregar la mejor educación a los jóvenes y prepararlos para ser los líderes del nuevo país. Su lema dice que 'el trabajo de la instrucción es la base de la libertad', confirmando que la libertad se lograba con un pueblo educado en un pueblo libre.",
        "personajes": "José Miguel Carrera, Mariano Egaña", "dif": "Fácil",
    },
    {
        "num": "22", "anio": "1814", "evento": "DESASTRE DE RANCAGUA",
        "img": "id_22_desastre_de_rancagua.png",
        "desc": "Fue una batalla muy dura en 1814 donde los patriotas fueron rodeados por el ejército español en la plaza de la ciudad. A pesar de luchar con todo su valor, tuvieron que retirarse, marcando el fin de la Patria Vieja y el inicio de un tiempo difícil de persecución.",
        "personajes": "Bernardo O'Higgins, José Miguel Carrera, Mariano Osorio", "dif": "Fácil",
    },
    {
        "num": "23", "anio": "1815", "evento": "LOS TALAVERAS",
        "img": "id_23_los_talavera.png",
        "desc": "Era un regimiento de soldados españoles muy temidos y estrictos que llegaron a Chile durante la Reconquista. Su misión era mantener el orden y castigar a quienes luchaban por la independencia, convirtiéndose en el símbolo del control de España sobre el territorio.",
        "personajes": "Vicente San Bruno, Casimiro Marcó del Pont", "dif": "Difícil",
    },
    {
        "num": "24", "anio": "1816", "evento": "ESPIONAJE PATRIOTA",
        "img": "id_24_manuel_rodriguez.png",
        "desc": "Durante la Reconquista, Manuel Rodríguez viajaba disfrazado de mendigo o arriero para vigilar a los españoles sin que lo notaran. Llevaba mensajes secretos y engañaba al enemigo en todo momento, manteniendo viva la esperanza de la libertad entre la gente del pueblo.",
        "personajes": "Manuel Rodríguez, José de San Martín", "dif": "Media",
    },
    {
        "num": "25", "anio": "1817", "evento": "BATALLA DE CHACABUCO",
        "img": "id_25_batalla_de_chacabuco.png",
        "desc": "En 1817, después de cruzar la Cordillera de los Andes, el ejército patriota derrotó a los españoles en esta gran batalla. Gracias a esta victoria, los chilenos recuperaron el control de Santiago y pudieron empezar a organizar definitivamente su independencia.",
        "personajes": "José de San Martín, Bernardo O'Higgins, Rafael Maroto", "dif": "Fácil",
    },
    {
        "num": "26", "anio": "1818", "evento": "PROCLAMACIÓN INDEPENDENCIA",
        "img": "id_26_proclamacion_independencia.png",
        "desc": "El 12 de febrero de 1818, Bernardo O'Higgins firmó el documento que declaraba formalmente que Chile era un país libre y soberano. Con esta firma, se anunciaba al mundo entero que Chile ya no obedecía al Rey de España y que comenzaba su propia historia como una república independiente.",
        "personajes": "Bernardo O'Higgins", "dif": "Fácil",
    },
    {
        "num": "27", "anio": "1818", "evento": "BATALLA DE MAIPÚ",
        "img": "id_27_batalla_de_maipu.png",
        "desc": "Fue la batalla decisiva en 1818 donde el ejército patriota derrotó definitivamente a las fuerzas españolas en los campos de Maipú. Con esta victoria se aseguró la libertad de la zona central de Chile. Es famosa por el 'Abrazo de Maipú' entre los generales San Martín y O'Higgins.",
        "personajes": "Bernardo O'Higgins, Miguel Zañartu", "dif": "Fácil",
    },
    {
        "num": "28", "anio": "1820", "evento": "TOMA DE VALDIVIA",
        "img": "id_28_toma_de_valdivia.png",
        "desc": "Fue una increíble hazaña marina liderada por Lord Cochrane en 1820. Con muy pocos hombres y mucha astucia, los patriotas capturaron los fuertes de Valdivia que estaban en manos españolas. Esta victoria fue clave para expulsar a los realistas del sur y consolidar el territorio chileno.",
        "personajes": "José de San Martín, Bernardo O'Higgins, Mariano Osorio", "dif": "Media",
    },
    {
        "num": "29", "anio": "1823", "evento": "ABDICACIÓN DE OHIGGINS",
        "img": "id_29_abdicacion_de_ohiggins.png",
        "desc": "En 1823, para evitar una guerra entre chilenos, Bernardo O'Higgins decidió dejar su cargo de Director Supremo. En una reunión emocionante, se quitó la banda tricolor y entregó el poder, partiendo luego al exilio en Perú para asegurar que el país pudiera vivir en paz.",
        "personajes": "Lord Cochrane, Jorge Beauchef, Bernardo O'Higgins", "dif": "Media",
    },
    {
        "num": "30", "anio": "1823", "evento": "ABOLICIÓN ESCLAVITUD",
        "img": "id_30_abolicion_esclavitud.png",
        "desc": "En 1823, Chile se convirtió en uno de los primeros países del mundo en prohibir totalmente la esclavitud. Gracias a esta ley, impulsada bajo el gobierno de Ramón Freire, todas las personas esclavizadas pasaron a ser libres y cualquier persona que pisara nuestro territorio sería libre.",
        "personajes": "José Miguel Infante, Ramón Freire, Mariano Egaña", "dif": "Media",
    },
    {
        "num": "31", "anio": "1823", "evento": "CONSTITUCIÓN MORALISTA",
        "img": "id_31_constitucion_moralista.png",
        "desc": "En 1823, Juan Egaña redactó una constitución tan exigente que pretendía regular hasta la vida privada de los ciudadanos, premiando la virtud y castigando los vicios. Fue tan estricta e impracticable que debió ser abandonada en menos de un año.",
        "personajes": "Juan Egaña", "dif": "Media",
    },
    {
        "num": "32", "anio": "1826", "evento": "LEYES FEDERALES",
        "img": "id_32_leyes_federales.png",
        "desc": "En 1826, José Miguel Infante impulsó un conjunto de leyes que dividieron a Chile en ocho provincias autónomas, buscando repartir el poder que estaba concentrado en Santiago. Fue una breve experiencia de organización política que terminó por ser revocada.",
        "personajes": "José Miguel Infante", "dif": "Media",
    },
    {
        "num": "33", "anio": "1826", "evento": "TRATADO DE TANTAUCO",
        "img": "id_33_tratado_de_tantauco.png",
        "desc": "En 1826, bajo el gobierno de Ramón Freire, se firmó este tratado que selló la rendición española en Chiloé y la incorporación definitiva del archipiélago a Chile. Marcó la expulsión final de los últimos soldados del Rey en territorio nacional.",
        "personajes": "Ramón Freire", "dif": "Media",
    },
    {
        "num": "34", "anio": "1828", "evento": "CONSTITUCIÓN LIBERAL",
        "img": "id_34_constitucion_liberal.png",
        "desc": "En 1828, José Joaquín de Mora redactó una carta fundamental de ideario liberal que fortaleció al Poder Legislativo, consagró derechos individuales y estableció un sistema descentralizado. Fue derrocada por los conservadores tras la batalla de Lircay.",
        "personajes": "José Joaquín de Mora", "dif": "Media",
    },
    {
        "num": "35", "anio": "1830", "evento": "BATALLA DE LIRCAY",
        "img": "id_35_batalla_lircay.png",
        "desc": "En 1830, a orillas del río Lircay, se libró la batalla decisiva de la guerra civil entre liberales y conservadores. La victoria de las fuerzas conservadoras lideradas por José Joaquín Prieto marcó el fin del período liberal y el inicio de un orden autoritario.",
        "personajes": "José Joaquín Prieto", "dif": "Media",
    },
    {
        "num": "36", "anio": "1831", "evento": "EL PESO DE LA NOCHE",
        "img": "id_36_el_peso_de_la_noche.png",
        "desc": "Frase acuñada por el ministro Diego Portales que expresaba su idea de orden y autoridad: los chilenos, por costumbre y cansancio, obedecerían a un gobierno firme. Fue la base del pensamiento político que marcó la República Conservadora durante gran parte del siglo XIX.",
        "personajes": "Diego Portales", "dif": "Difícil",
    },
    {
        "num": "37", "anio": "1832", "evento": "DESCUBRIMIENTO DE CHAÑARCILLO",
        "img": "id_37_descubrimiento_chanarcillo.png",
        "desc": "En 1832, el arriero Juan Godoy descubrió cerca de Copiapó un yacimiento de plata que resultó ser uno de los más grandes del país. Chañarcillo enriqueció a la nación, modernizó el norte y transformó la economía chilena durante décadas.",
        "personajes": "Juan Godoy", "dif": "Media",
    },
    {
        "num": "38", "anio": "1833", "evento": "CONSTITUCIÓN DE 1833",
        "img": "id_38_constitucion_de_1833.png",
        "desc": "Redactada bajo el impulso de Diego Portales y Mariano Egaña, otorgó un poder casi total al Presidente de la República y reconoció al catolicismo como religión oficial. Rigió durante casi cien años y trajo a Chile la mayor estabilidad política del continente.",
        "personajes": "Mariano Egaña, Diego Portales", "dif": "Media",
    },
    {
        "num": "39", "anio": "1836", "evento": "GUERRA DE LA CONFEDERACIÓN",
        "img": "id_39_guerra_confederacion.png",
        "desc": "En 1836, Chile declaró la guerra a la Confederación Perú-Boliviana creada por Andrés de Santa Cruz, para evitar que la unión de los vecinos amenazara el equilibrio del Pacífico. Fue la primera gran guerra internacional de la república, impulsada por Diego Portales.",
        "personajes": "Diego Portales", "dif": "Media",
    },
    {
        "num": "40", "anio": "1839", "evento": "BATALLA DE YUNGAY",
        "img": "id_40_batalla_de_yungay.png",
        "desc": "El 20 de enero de 1839, las tropas chilenas al mando del general Manuel Bulnes vencieron al ejército de Santa Cruz en el pueblo peruano de Yungay. La victoria disolvió la Confederación Perú-Boliviana y consolidó el liderazgo de Chile en el sur del continente.",
        "personajes": "Manuel Bulnes", "dif": "Media",
    },
    {
        "num": "41", "anio": "1842", "evento": "LEY DE COLONIZACIÓN",
        "img": "id_41_ley_de_colonizacion.png",
        "desc": "Bajo el gobierno de Manuel Bulnes, el Estado promovió la llegada de familias alemanas al sur de Chile para poblar y producir en tierras aisladas. La inmigración dio origen a la profunda influencia cultural alemana en Valdivia, Osorno y Llanquihue.",
        "personajes": "Manuel Bulnes", "dif": "Media",
    },
    {
        "num": "42", "anio": "1843", "evento": "TOMA DEL ESTRECHO",
        "img": "id_42_toma_del_estrecho.png",
        "desc": "En 1843, la Goleta Ancud, comandada por Juan Williams, zarpó desde Chiloé y tomó posesión del Estrecho de Magallanes en nombre de Chile. La expedición aseguró la soberanía del extremo sur del continente y dio origen al Fuerte Bulnes.",
        "personajes": "Juan Williams", "dif": "Media",
    },
    {
        "num": "43", "anio": "1843", "evento": "UNIVERSIDAD DE CHILE",
        "img": "id_43_universidad_de_chile.png",
        "desc": "En 1843 se fundó la Universidad de Chile, con Andrés Bello como su primer rector. Heredera de la antigua Universidad de San Felipe, se transformó en el gran centro de la investigación, la cultura y las letras nacionales, base del sistema educativo moderno.",
        "personajes": "Andrés Bello", "dif": "Fácil",
    },
    {
        "num": "44", "anio": "1844", "evento": "RECONOCIMIENTO DE ESPAÑA",
        "img": "id_44_reconocimiento_espana.png",
        "desc": "En 1844, la reina Isabel II firmó el tratado mediante el cual España reconoció oficialmente la independencia de Chile. Fue el cierre diplomático definitivo de la lucha contra el reino español y el inicio de relaciones formales entre ambas naciones.",
        "personajes": "Isabel II de España", "dif": "Media",
    },
    {
        "num": "45", "anio": "1848", "evento": "CÓDIGO CIVIL",
        "img": "id_45_codigo_civil.png",
        "desc": "Redactado por Andrés Bello durante casi veinte años, el Código Civil chileno ordenó de forma moderna los contratos, la propiedad y la vida familiar. Promulgado más tarde en 1855, sigue siendo la base del sistema jurídico chileno y modelo para toda Hispanoamérica.",
        "personajes": "Andrés Bello", "dif": "Media",
    },
    {
        "num": "46", "anio": "1851", "evento": "PRIMER FERROCARRIL",
        "img": "id_46_primer_ferrocarril.png",
        "desc": "En 1851 se inauguró la línea Copiapó-Caldera, impulsada por el empresario William Wheelwright. Fue el primer ferrocarril en funcionar en Chile y en toda Sudamérica, marcando el inicio de la era del transporte a vapor y de la modernización del norte minero.",
        "personajes": "William Wheelwright", "dif": "Media",
    },
    {
        "num": "47", "anio": "1851", "evento": "REVOLUCIÓN DE 1851",
        "img": "id_47_revolucion_1851.png",
        "desc": "Tras la elección de Manuel Montt, sectores liberales se levantaron en armas en La Serena y Concepción contra el gobierno conservador. La guerra civil fue sofocada por las fuerzas del general Bulnes y marcó un quiebre político al interior del país.",
        "personajes": "Manuel Montt", "dif": "Difícil",
    },
    {
        "num": "48", "anio": "1852", "evento": "EL TELÉGRAFO",
        "img": "id_48_el_telegrafo.png",
        "desc": "En 1852 entró en operación la primera línea telegráfica entre Santiago y Valparaíso, impulsada por William Wheelwright. Las señales eléctricas permitieron enviar mensajes de forma casi inmediata y transformaron la comunicación, el comercio y la política del país.",
        "personajes": "William Wheelwright", "dif": "Media",
    },
    {
        "num": "49", "anio": "1856", "evento": "CUESTIÓN DEL SACRISTÁN",
        "img": "id_49_cuestion_del_sacristan.png",
        "desc": "Un conflicto que empezó por el despido de un sacristán de la Catedral escaló hasta enfrentar a la Iglesia con el Estado y provocar un quiebre entre el gobierno de Manuel Montt y los conservadores, dando origen a nuevas alianzas políticas en el país.",
        "personajes": "Manuel Montt", "dif": "Difícil",
    },
    {
        "num": "50", "anio": "1860", "evento": "LEY INSTRUCCIÓN PRIMARIA",
        "img": "id_50_ley_instruccion_primaria.png",
        "desc": "Promulgada bajo el gobierno de Manuel Montt, esta ley hizo al Estado responsable de garantizar educación primaria gratuita para todos los niños del país. Fue el inicio de la instrucción pública masiva y un paso decisivo hacia la alfabetización nacional.",
        "personajes": "Manuel Montt", "dif": "Media",
    },
    {
        "num": "51", "anio": "1861", "evento": "FUSIÓN LIBERAL-CONSERVADORA",
        "img": "id_51_fusion_liberal_conservadora.png",
        "desc": "Alianza política inédita entre liberales moderados y conservadores que llevó a la presidencia a José Joaquín Pérez. Buscaba democratizar el país, modernizar las leyes y poner fin al autoritarismo, abriendo la puerta al período conocido como República Liberal.",
        "personajes": "José Joaquín Pérez", "dif": "Difícil",
    },
    {
        "num": "52", "anio": "1863", "evento": "EL CUERPO DE BOMBEROS",
        "img": "id_52_el_cuerpo_de_bomberos.png",
        "desc": "Tras un devastador incendio en la Iglesia de la Compañía que dejó más de dos mil muertos, ciudadanos voluntarios fundaron el primer Cuerpo de Bomberos en Santiago. La institución, totalmente voluntaria, se convirtió en una de las más respetadas del país.",
        "personajes": "Ciudadanía", "dif": "Media",
    },
    {
        "num": "53", "anio": "1866", "evento": "GUERRA CONTRA ESPAÑA",
        "img": "id_53_guerra_contra_espana.png",
        "desc": "En 1866, una flota española bombardeó Valparaíso causando graves daños al puerto. Chile se unió a Perú, Ecuador y Bolivia contra la agresión europea en defensa de la soberanía del Pacífico sur, en uno de los últimos conflictos con la antigua metrópoli.",
        "personajes": "José Joaquín Pérez", "dif": "Media",
    },
    {
        "num": "54", "anio": "1871", "evento": "FIN REELECCIÓN INMEDIATA",
        "img": "id_54_fin_reeleccion_inmediata.png",
        "desc": "Reforma constitucional promulgada bajo Federico Errázuriz Zañartu que prohibió al Presidente ser reelegido para un período inmediatamente siguiente. Buscó asegurar la alternancia en el poder y evitar la concentración prolongada del mando político.",
        "personajes": "Federico Errázuriz Zañartu", "dif": "Media",
    },
    {
        "num": "55", "anio": "1874", "evento": "REFORMA ELECTORAL",
        "img": "id_55_reforma_electoral.png",
        "desc": "Gran reforma impulsada por Federico Errázuriz Zañartu que eliminó el requisito de riqueza para votar, ampliando el derecho a sufragio a todos los hombres que supieran leer y escribir. Fue un paso decisivo en la democratización del sistema electoral chileno.",
        "personajes": "Federico Errázuriz Zañartu", "dif": "Difícil",
    },
    {
        "num": "56", "anio": "1877", "evento": "DECRETO AMUNÁTEGUI",
        "img": "id_56_decreto_amunategui.png",
        "desc": "Firmado por el ministro Miguel Luis Amunátegui, este decreto autorizó oficialmente el ingreso de las mujeres a la Universidad de Chile. Fue un hito histórico para la igualdad de género en la educación, abriendo las puertas de la ciencia y las profesiones.",
        "personajes": "Miguel Luis Amunátegui", "dif": "Media",
    },
    {
        "num": "57", "anio": "1879", "evento": "GUERRA DEL PACÍFICO",
        "img": "id_57_guerra_del_pacifico.png",
        "desc": "Conflicto contra Perú y Bolivia por el control del salitre en el norte, también conocido como el 'oro blanco'. Iniciada bajo el gobierno de Aníbal Pinto, fue la guerra más extensa y transformadora del territorio nacional, cambiando para siempre las fronteras.",
        "personajes": "Aníbal Pinto", "dif": "Fácil",
    },
    {
        "num": "58", "anio": "1879", "evento": "COMBATE DE ANGAMOS",
        "img": "id_58_combate_de_angamos.png",
        "desc": "El 8 de octubre de 1879, la marina chilena capturó el temible monitor Huáscar frente a la costa de Angamos tras una persecución épica. La derrota del almirante Grau dio a Chile el dominio absoluto del mar y fue decisiva para el curso de la Guerra del Pacífico.",
        "personajes": "Juan José Latorre", "dif": "Media",
    },
    {
        "num": "59", "anio": "1881", "evento": "TRATADO DE LÍMITES",
        "img": "id_59_tratado_de_limites.png",
        "desc": "Acuerdo firmado con Argentina bajo el gobierno de Domingo Santa María que definió la frontera entre ambos países siguiendo las altas cumbres de la cordillera de los Andes. Buscó evitar conflictos territoriales y asegurar la paz en plena Guerra del Pacífico.",
        "personajes": "Domingo Santa María", "dif": "Media",
    },
    {
        "num": "60", "anio": "1881", "evento": "TOMA DE LIMA",
        "img": "id_60_toma_de_lima.png",
        "desc": "En enero de 1881, las tropas chilenas al mando del general Manuel Baquedano entraron triunfantes en la capital peruana tras las batallas de Chorrillos y Miraflores. La ocupación de Lima marcó el punto más alto del avance chileno en la Guerra del Pacífico.",
        "personajes": "Manuel Baquedano", "dif": "Media",
    },
    {
        "num": "61", "anio": "1882", "evento": "BATALLA DE LA CONCEPCIÓN",
        "img": "id_61_batalla_de_concepcion.png",
        "desc": "En julio de 1882, en plena campaña de la Sierra peruana, 77 soldados chilenos al mando de Ignacio Carrera Pinto resistieron heroicamente el ataque de miles de combatientes en el pueblo de La Concepción. Ninguno se rindió. Es el máximo símbolo del sacrificio militar chileno.",
        "personajes": "Ignacio Carrera Pinto", "dif": "Difícil",
    },
    {
        "num": "62", "anio": "1883", "evento": "LEY DE CEMENTERIOS",
        "img": "id_62_ley_de_cementerios.png",
        "desc": "Promulgada bajo el gobierno de Domingo Santa María, esta ley laica permitió que personas de toda creencia fueran enterradas en cementerios públicos, no sólo los católicos. Generó un fuerte debate con la Iglesia y aseguró la dignidad en la muerte para todos los chilenos.",
        "personajes": "Domingo Santa María", "dif": "Media",
    },
    {
        "num": "63", "anio": "1884", "evento": "LEY DE MATRIMONIO CIVIL",
        "img": "id_63_ley_atrimonio_civil.png",
        "desc": "Impulsada por Domingo Santa María, esta ley estableció que el único matrimonio válido ante el Estado era el celebrado civilmente. Quitó a la Iglesia el control exclusivo del vínculo matrimonial y fue uno de los hitos laicizadores más importantes del siglo XIX.",
        "personajes": "Domingo Santa María", "dif": "Media",
    },
    {
        "num": "64", "anio": "1884", "evento": "LEY REGISTRO CIVIL",
        "img": "id_64_ley_registro_civil.png",
        "desc": "Con esta ley, el Estado asumió el registro oficial de nacimientos, matrimonios y defunciones, función hasta entonces en manos de la Iglesia. Creó la base del sistema de identidad de cada ciudadano y terminó de consolidar la laicización de la vida pública chilena.",
        "personajes": "Domingo Santa María", "dif": "Media",
    },
    {
        "num": "65", "anio": "1888", "evento": "ANEXIÓN ISLA DE PASCUA",
        "img": "id_65_anexion_isla_de_pascua.png",
        "desc": "El 9 de septiembre de 1888, el capitán Policarpo Toro firmó con los jefes rapanui el acuerdo que incorporó Isla de Pascua a la soberanía chilena. Rapa Nui, en medio del Pacífico, pasó a ser oficialmente parte del territorio nacional.",
        "personajes": "Policarpo Toro", "dif": "Media",
    },
    {
        "num": "66", "anio": "1888", "evento": "PONTIFICIA UNIVERSIDAD CATÓLICA",
        "img": "id_66_universidad_catolica.png",
        "desc": "Fundada por el arzobispo Mariano Casanova y con Joaquín Larraín Gandarillas como primer rector, la Universidad Católica nació como alternativa confesional a la Universidad de Chile. Hoy es una de las casas de estudios más influyentes del país.",
        "personajes": "Joaquín Larraín Gandarillas", "dif": "Media",
    },
    {
        "num": "67", "anio": "1890", "evento": "VIADUCTO DEL MALLECO",
        "img": "id_67_el_viaducto_del_malleco.png",
        "desc": "Inaugurado por el presidente José Manuel Balmaceda, el Viaducto del Malleco fue en su momento uno de los puentes de hierro más altos del mundo. Permitió extender el ferrocarril hacia La Araucanía y es un símbolo de la modernización impulsada en esa época.",
        "personajes": "José Manuel Balmaceda", "dif": "Media",
    },
    {
        "num": "68", "anio": "1891", "evento": "GUERRA CIVIL DE 1891",
        "img": "id_68_guerra_civil_de_1981.png",
        "desc": "Enfrentamiento entre el presidente José Manuel Balmaceda y el Congreso por el control del poder político. La violenta guerra civil dividió al país, terminó con la derrota del ejecutivo y dio paso al sistema parlamentario que marcaría las siguientes décadas.",
        "personajes": "José Manuel Balmaceda", "dif": "Difícil",
    },
    {
        "num": "69", "anio": "1891", "evento": "BATALLA DE PLACILLA",
        "img": "id_69_batalalla_de_placilla.png",
        "desc": "Librada el 28 de agosto de 1891 en las cercanías de Valparaíso, la batalla de Placilla fue la victoria decisiva del ejército del Congreso, liderado por Estanislao del Canto. Selló el desenlace de la guerra civil y provocó la caída del gobierno de Balmaceda.",
        "personajes": "Estanislao del Canto", "dif": "Difícil",
    },
    {
        "num": "70", "anio": "1892", "evento": "LA COMUNA AUTÓNOMA",
        "img": "id_70_lacomuna_autonoma.png",
        "desc": "Impulsada por Manuel José Irarrázaval, esta ley dio independencia económica y política a los municipios del país. Buscaba descentralizar el poder concentrado en Santiago y fue uno de los grandes proyectos de reforma del inicio del período parlamentario.",
        "personajes": "Manuel José Irarrázaval", "dif": "Difícil",
    },
    {
        "num": "71", "anio": "1895", "evento": "ALUMBRADO ELÉCTRICO",
        "img": "id_71_alumbrado_electrico.png",
        "desc": "En 1895, Santiago comenzó a iluminarse con energía eléctrica, despidiendo definitivamente a los antiguos faroles de gas. La nueva luz transformó la vida nocturna, mejoró la seguridad y marcó la entrada de la capital chilena a la era moderna.",
        "personajes": "Ciudadanía", "dif": "Media",
    },
    {
        "num": "72", "anio": "1896", "evento": "CINE EN CHILE",
        "img": "id_72_cine_en_chile.png",
        "desc": "El 25 de agosto de 1896 se realizó en Santiago la primera exhibición cinematográfica del país. Por primera vez, los chilenos vieron imágenes en movimiento proyectadas en una pantalla, marcando el inicio de la fascinación nacional por el cine.",
        "personajes": "Ciudadanía", "dif": "Media",
    },
    {
        "num": "73", "anio": "1900", "evento": "EL TRANVÍA ELÉCTRICO",
        "img": "id_73_el_travia_electrico.png",
        "desc": "En 1900, los carros tirados por caballos fueron reemplazados por modernos tranvías eléctricos en Santiago y Valparaíso. La revolución del transporte público cambió la vida cotidiana de las ciudades y simbolizó el progreso tecnológico de fin de siglo.",
        "personajes": "Ciudadanía", "dif": "Media",
    },
    {
        "num": "74", "anio": "1907", "evento": "MATANZA ESCUELA SANTA MARÍA",
        "img": "id_74_matanza_escuela_santa_maria.png",
        "desc": "El 21 de diciembre de 1907, en Iquique, miles de obreros del salitre y sus familias fueron masacrados por el Ejército mientras protestaban pacíficamente en la Escuela Santa María. Bajo el gobierno de Pedro Montt, fue una de las tragedias más dolorosas de la historia social chilena.",
        "personajes": "Pedro Montt", "dif": "Difícil",
    },
    {
        "num": "75", "anio": "1910", "evento": "CENTENARIO DE CHILE",
        "img": "id_75_centenario_de_chile.png",
        "desc": "En septiembre de 1910, Chile celebró cien años de independencia con grandes fiestas, monumentos y obras públicas. Bajo Emiliano Figueroa Larraín, el país mostró al mundo su orgullo republicano, aunque también afloraron las contradicciones de la cuestión social.",
        "personajes": "Emiliano Figueroa", "dif": "Media",
    },
    {
        "num": "76", "anio": "1879", "evento": "COMBATE NAVAL DE IQUIQUE",
        "img": "id_76_combate_naval_de_iquique.png",
        "desc": "El 21 de mayo de 1879, la corbeta Esmeralda al mando de Arturo Prat fue hundida por el blindado Huáscar de Miguel Grau frente a Iquique. El sacrificio del comandante Prat, que se negó a rendirse, lo convirtió en el héroe naval más importante de Chile.",
        "personajes": "Arturo Prat, Miguel Grau", "dif": "Fácil",
    },
    {
        "num": "77", "anio": "1880", "evento": "CUESTIÓN SOCIAL",
        "img": "id_77_cuestion_social.png",
        "desc": "Miles de familias obreras del salitre, el carbón y las ciudades vivían hacinadas y sin atención médica, mientras el país producía una riqueza enorme. El despertar del movimiento obrero, liderado por figuras como Luis Emilio Recabarren, cambió para siempre la política chilena.",
        "personajes": "Luis Emilio Recabarren", "dif": "Fácil",
    },
    {
        "num": "78", "anio": "1823", "evento": "CONSTITUCIÓN MORALISTA 1823",
        "img": "id_78_constitucion_moralista_1823.png",
        "desc": "Redactada por Juan Egaña, fue una constitución tan exigente que pretendía regular hasta los hábitos privados de los ciudadanos, premiando la virtud y castigando el vicio. Resultó inejecutable y debió ser abandonada en menos de un año de vigencia.",
        "personajes": "Juan Egaña", "dif": "Media",
    },
    {
        "num": "79", "anio": "1828", "evento": "CONSTITUCIÓN LIBERAL 1828",
        "img": "id_79_constitucion_liberal_1828.png",
        "desc": "Promulgada bajo Francisco Antonio Pinto, esta carta liberal fortaleció al Poder Legislativo, consagró derechos individuales y estableció un sistema descentralizado. Fue derrocada por los conservadores tras la batalla de Lircay en 1830.",
        "personajes": "Francisco Antonio Pinto, Melchor de Santiago Concha", "dif": "Media",
    },
    {
        "num": "80", "anio": "1833", "evento": "CONSTITUCIÓN DE 1833",
        "img": "id_80_constitucion_de_1833.png",
        "desc": "Redactada por Mariano Egaña y Manuel José Gandarillas bajo la influencia de Diego Portales, marcó el inicio de la estabilidad republicana con un Ejecutivo poderoso, voto censitario y reconocimiento del catolicismo como religión oficial. Rigió por casi cien años.",
        "personajes": "Diego Portales, Mariano Egaña, Manuel José Gandarillas", "dif": "Media",
    },
]

# Por defecto se generan todas las cartas del array CARTAS.
# Para generar solo algunas, filtra por num en la línea de abajo.
SOLO_NUMS = None   # ej: ["02","03"] para generar esas dos; None = todas

if __name__ == "__main__":
    import sys
    os.makedirs(OUT_DIR, exist_ok=True)
    # Permite pasar los IDs por línea de comando: python3 script.py 02 03 04
    if len(sys.argv) > 1:
        SOLO_NUMS = sys.argv[1:]
    cartas = CARTAS if SOLO_NUMS is None else [c for c in CARTAS if c["num"] in SOLO_NUMS]
    print(f"Generando {len(cartas)} carta(s)...\n")
    for card in cartas:
        generar_carta(card, f"id_{card['num']}_carta_v2_big.png")
    print("\nListo.")
