import yfinance as yf
import psycopg2
from datetime import datetime
import os

# -----------------------------
# Activos que vamos a observar
# -----------------------------
activos = {
    "SP500": "^GSPC",
    "VIX": "^VIX",
    "ORO": "GC=F",
    "PETROLEO": "CL=F",
    "BONO_10Y": "^TNX"
}

# -----------------------------
# Descargar precios del día
# -----------------------------
datos = {}
for nombre, ticker in activos.items():
    activo = yf.Ticker(ticker)
    historial = activo.history(period="1h")  # cada hora
    if not historial.empty:
        precio = historial["Close"].iloc[-1]
        datos[nombre] = precio
    else:
        print(f"No hay datos para {ticker}")
        datos[nombre] = None

# Agregar la fecha y hora
datos["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------
# Conectar a PostgreSQL en Supabase usando secretos
# -----------------------------
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT", "5432")

conn = psycopg2.connect(
    host=PG_HOST,
    database=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD,
    port=PG_PORT
)
cursor = conn.cursor()

# -----------------------------
# Crear tabla si no existe
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS datos_mercado (
    fecha TIMESTAMP PRIMARY KEY,
    SP500 NUMERIC,
    VIX NUMERIC,
    ORO NUMERIC,
    PETROLEO NUMERIC,
    BONO_10Y NUMERIC
)
""")

# -----------------------------
# Insertar o actualizar datos
# -----------------------------
cursor.execute("""
INSERT INTO datos_mercado (fecha, SP500, VIX, ORO, PETROLEO, BONO_10Y)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (fecha)
DO UPDATE SET
    SP500 = EXCLUDED.SP500,
    VIX = EXCLUDED.VIX,
    ORO = EXCLUDED.ORO,
    PETROLEO = EXCLUDED.PETROLEO,
    BONO_10Y = EXCLUDED.BONO_10Y
""", (datos["fecha"], datos["SP500"], datos["VIX"], datos["ORO"], datos["PETROLEO"], datos["BONO_10Y"]))

conn.commit()
cursor.close()
conn.close()

print("Datos guardados en PostgreSQL")
print(datos)
