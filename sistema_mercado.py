import yfinance as yf
import sqlite3
from datetime import datetime

# Activos que vamos a observar
activos = {
    "SP500": "^GSPC",
    "VIX": "^VIX",
    "ORO": "GC=F",
    "PETROLEO": "CL=F",
    "BONO_10Y": "^TNX"
}

# Descargar precios del día
datos = {}
for nombre, ticker in activos.items():
    activo = yf.Ticker(ticker)
    historial = activo.history(period="1d")
    if not historial.empty:
        precio = historial["close"].iloc[-1]
        datos[nombre] = precio
    else:
        print(f"No hay datos para {ticker}")
# Agregar la fecha
datos["fecha"] = datetime.now().strftime("%Y-%m-%d")

# Conectar a SQLite (crea archivo base_mercado.db en la carpeta actual)
conn = sqlite3.connect("base_mercado.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS datos_mercado (
    fecha TEXT PRIMARY KEY,
    SP500 REAL,
    VIX REAL,
    ORO REAL,
    PETROLEO REAL,
    BONO_10Y REAL
)
''')

# Insertar o reemplazar los datos del día
cursor.execute('''
INSERT OR REPLACE INTO datos_mercado (fecha, SP500, VIX, ORO, PETROLEO, BONO_10Y)
VALUES (?, ?, ?, ?, ?, ?)
''', (datos["fecha"], datos["SP500"], datos["VIX"], datos["ORO"], datos["PETROLEO"], datos["BONO_10Y"]))

conn.commit()
conn.close()

print("Datos guardados en SQLite:")
print(datos)
