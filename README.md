# Misterios de Chile — Guía de Desarrollo

## Estructura del proyecto

```
Juego Chile/
├── index.html                          ← App web (se sube a GitHub Pages)
├── imagenes/                           ← Imágenes históricas (van a Firebase Storage)
├── audios/                             ← Audios mp4 (van a Firebase Storage)
├── cartas/                             ← Cartas físicas para imprimir (frente)
├── qr/                                 ← Cartas QR para imprimir (anverso)
├── cartas_qr_png/                      ← Alias local de qr/ (ignorado en git)
├── misterios-seed/                     ← Scripts de administración
│   ├── seed_firestore.js               ← Pobla Firestore con las 75 cartas base
│   ├── add_cartas_76_80.js             ← Agrega cartas 76-80 a Firestore
│   ├── upload_storage_76_80.js         ← Sube imágenes/audios 76-80 a Firebase Storage
│   ├── generar_carta_premium.py        ← Genera cartas físicas premium (diseño negro/dorado)
│   └── generar_qr_premium.py           ← Genera cartas QR premium (diseño negro/dorado)
└── README.md                           ← Este archivo
```

---

## Cómo funciona el sistema

| Fuente | Qué almacena | Usado por |
|--------|-------------|-----------|
| **Firestore** | Datos de cada carta (año, evento, pistas, personajes) | App web en tiempo real |
| **Firebase Storage** | Imágenes `.png` y audios `.mp4` | App web en tiempo real |
| **GitHub** | `index.html`, scripts, cartas físicas para imprimir | GitHub Pages (hosting) |
| **Carpeta local** | Todo lo anterior + archivos de trabajo | Respaldo y generación |

El `index.html` **no lee archivos del repo** — carga imágenes y audios desde Firebase Storage, y los datos de las cartas desde Firestore.

---

## Agregar una carta nueva (ej: carta 81)

### Paso 1 — Preparar los archivos
1. Agregar imagen en `imagenes/id_81_nombre_del_evento.png`
2. Agregar audio en `audios/id_81_nombre_del_evento.mp4`

### Paso 2 — Generar la carta física premium
Editar `misterios-seed/generar_carta_premium.py`, agregar al array `CARTAS`:
```python
{
    "num": "81",
    "anio": "1920",
    "evento": "NOMBRE DEL EVENTO EN MAYÚSCULAS",
    "img": "id_81_nombre_del_evento.png",
    "desc": "Descripción breve para la carta (máx ~300 caracteres).",
    "personajes": "Nombre Persona · Otro Nombre",
    "dif": "Fácil",   # opciones: "Fácil", "Media", "Difícil"
},
```
Luego correr:
```bash
cd misterios-seed
python generar_carta_premium.py
```

### Paso 3 — Generar el QR premium
Editar `misterios-seed/generar_qr_premium.py`, agregar `"81"` al array `IDS`:
```python
IDS = ["76", "77", "78", "79", "80", "81"]
```
Luego correr:
```bash
python generar_qr_premium.py
```

### Paso 4 — Actualizar los scripts JS
En `misterios-seed/add_cartas_76_80.js`, agregar la carta 81 al objeto `cartas` con sus datos completos (año, evento, pistas, personajes).

En `misterios-seed/upload_storage_76_80.js`, agregar la imagen y audio de la carta 81 al array `archivos`.

### Paso 5 — Subir todo
```bash
# Subir imagen y audio a Firebase Storage
node upload_storage_76_80.js

# Agregar carta a Firestore
node add_cartas_76_80.js

# Subir archivos actualizados a GitHub
git add .
git commit -m "Agrega carta 81 — Nombre del evento"
git push origin main
```

---

## Diseño de cartas

### Cartas estándar (01–75)
- Fondo verde oscuro con borde dorado
- Año en dorado, banda marrón con título, imagen histórica, área crema con texto
- Generadas originalmente con herramienta externa

### Cartas Premium / Deluxe (76–80)
- Fondo negro profundo con triple marco dorado
- Corona en la parte superior
- Banda "✦ CARTA ESPECIAL ✦" bajo el año
- Imagen histórica con marco dorado interior
- Área de texto en slate oscuro azulado
- Footer "★ EDICIÓN ESPECIAL ★"
- Script: `misterios-seed/generar_carta_premium.py`

### Cartas QR Premium (76–80)
- Mismo diseño negro/dorado que la carta premium
- QR real escaneable apuntando a `https://misteriosdechile.com?id=XX`
- Corona, "★ EDICIÓN ESPECIAL ★", estrella de 8 puntas en separador
- Script: `misterios-seed/generar_qr_premium.py`

---

## Credenciales Firebase

Los scripts Node.js usan Application Default Credentials. Antes de correrlos asegurarse de tener autenticación activa:

```bash
# Opción A — Variable de entorno con clave de servicio
export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/serviceAccountKey.json"

# Opción B — gcloud autenticado
gcloud auth application-default login
```

Proyecto Firebase: `misteriosdechile-7a538`
Bucket Storage: `misteriosdechile-7a538.firebasestorage.app`
Colección Firestore: `cartas`

---

## Repositorio GitHub

```
https://github.com/faldunero/misterios_de_chile
```

Rama principal: `main`
Hosting: GitHub Pages con dominio `misteriosdechile.com`

---

## Reglas del juego (resumen técnico)

- **Jugadores:** 2 a 5
- **Cartas:** 80 (75 estándar + 5 Deluxe — sin diferencia de reglas)
- **Fichas por jugador:** 50
- **Objetivo:** Ubicar cartas en línea de tiempo cronológica
- **Pistas:** 3 niveles (1, 2 y 3 fichas)
- **Victoria:** Más fichas al agotar el mazo

---

*Diseño: Felipe Ignacio Aldunate Romero*
