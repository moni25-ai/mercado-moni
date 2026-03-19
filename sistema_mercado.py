import yfinance as yf
import psycopg2
from datetime import datetime
import os

# Limpiar consola al iniciar
# -----------------------------
os.system('cls' if os.name == 'nt' else 'clear')# -----------------------------
# Activos que vamos a observar
# -----------------------------
activos = {
    "SP500": "^GSPC",
    "VIX": "^VIX",
    "ORO": "GC=F",
    "PETROLEO": "CL=F",
    "BONO_10Y": "^TNX",
    "USDARS": "ARS=X"
}

# -----------------------------
# Descargar precios
# -----------------------------
datos = {}

for nombre, ticker in activos.items():
    activo = yf.Ticker(ticker)

    if nombre == "USDARS":
        historial = activo.history(period="30d")
    else:
        historial = activo.history(period="1d")

    if not historial.empty:
        fila = historial.iloc[-1]

        if nombre == "USDARS":
            datos["USDARS_open"] = float(fila["Open"])
            datos["USDARS_high"] = float(fila["High"])
            datos["USDARS_low"] = float(fila["Low"])
            datos["USDARS_close"] = float(fila["Close"])
            datos["USDARS_adj"] = float(fila["Adj Close"]) if "Adj Close" in fila else float(fila["Close"])
            datos["USDARS_volume"] = int(fila["Volume"])

            # SMA
            historial["SMA5"] = historial["Close"].rolling(5).mean()
            historial["SMA10"] = historial["Close"].rolling(10).mean()
            historial["SMA20"] = historial["Close"].rolling(20).mean()

            datos["USDARS_SMA5"] = float(historial["SMA5"].iloc[-1])
            datos["USDARS_SMA10"] = float(historial["SMA10"].iloc[-1])
            datos["USDARS_SMA20"] = float(historial["SMA20"].iloc[-1])

            # RSI
            delta = historial["Close"].diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            rs = gain / loss
            historial["RSI14"] = 100 - (100 / (1 + rs))
            datos["USDARS_RSI14"] = float(historial["RSI14"].iloc[-1])

            # MACD
            ema12 = historial["Close"].ewm(span=12, adjust=False).mean()
            ema26 = historial["Close"].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()

            datos["USDARS_MACD"] = float(macd.iloc[-1])
            datos["USDARS_MACD_signal"] = float(signal.iloc[-1])

        else:
            datos[nombre] = float(fila["Close"])
    else:
        print(f"No hay datos para {ticker}")

# -----------------------------
# Calcular CCL (más seguro)
# -----------------------------
try:
    hist_pesos = yf.Ticker("AL30.BA").history(period="5d")
    hist_usd = yf.Ticker("AL30").history(period="5d")

    if not hist_pesos.empty and not hist_usd.empty:
        precio_pesos = hist_pesos["Close"].dropna().iloc[-1]
        precio_usd = hist_usd["Close"].dropna().iloc[-1]

        datos["CCL"] = float(precio_pesos) / float(precio_usd)
    else:
        datos["CCL"] = None

except Exception as e:
    print("Error CCL:", e)
    datos["CCL"] = None

# Fecha
from datetime import datetime
from pytz import timezone

# Hora local de Argentina
ahora = datetime.now(timezone('America/Argentina/Buenos_Aires'))

# Generar fecha correcta: YYYY-MM-DD HH:MM:SS
datos["fecha"] = ahora.strftime("%Y-%m-%d %H:%M:%S")

# Conexión a PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=os.getenv("PG_PORT", "5432")
)

cursor = conn.cursor()

# -----------------------------
# Crear tabla
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS datos_mercado (
    fecha TIMESTAMP PRIMARY KEY,
    SP500 NUMERIC,
    VIX NUMERIC,
    ORO NUMERIC,
    PETROLEO NUMERIC,
    BONO_10Y NUMERIC,
    CCL NUMERIC,

    USDARS_open NUMERIC,
    USDARS_high NUMERIC,
    USDARS_low NUMERIC,
    USDARS_close NUMERIC,
    USDARS_adj NUMERIC,
    USDARS_volume BIGINT,

    USDARS_SMA5 NUMERIC,
    USDARS_SMA10 NUMERIC,
    USDARS_SMA20 NUMERIC,
    USDARS_RSI14 NUMERIC,
    USDARS_MACD NUMERIC,
    USDARS_MACD_signal NUMERIC
)
""")

# -----------------------------
# Insertar datos
# -----------------------------
cursor.execute("""
INSERT INTO datos_mercado (
    fecha, SP500, VIX, ORO, PETROLEO, BONO_10Y, CCL,
    USDARS_open, USDARS_high, USDARS_low, USDARS_close, USDARS_adj, USDARS_volume,
    USDARS_SMA5, USDARS_SMA10, USDARS_SMA20, USDARS_RSI14, USDARS_MACD, USDARS_MACD_signal
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (fecha)
DO UPDATE SET
    SP500 = EXCLUDED.SP500,
    VIX = EXCLUDED.VIX,
    ORO = EXCLUDED.ORO,
    PETROLEO = EXCLUDED.PETROLEO,
    BONO_10Y = EXCLUDED.BONO_10Y,
    CCL = EXCLUDED.CCL,

    USDARS_open = EXCLUDED.USDARS_open,
    USDARS_high = EXCLUDED.USDARS_high,
    USDARS_low = EXCLUDED.USDARS_low,
    USDARS_close = EXCLUDED.USDARS_close,
    USDARS_adj = EXCLUDED.USDARS_adj,
    USDARS_volume = EXCLUDED.USDARS_volume,

    USDARS_SMA5 = EXCLUDED.USDARS_SMA5,
    USDARS_SMA10 = EXCLUDED.USDARS_SMA10,
    USDARS_SMA20 = EXCLUDED.USDARS_SMA20,
    USDARS_RSI14 = EXCLUDED.USDARS_RSI14,
    USDARS_MACD = EXCLUDED.USDARS_MACD,
    USDARS_MACD_signal = EXCLUDED.USDARS_MACD_signal
""", (
    datos["fecha"],
    datos.get("SP500"),
    datos.get("VIX"),
    datos.get("ORO"),
    datos.get("PETROLEO"),
    datos.get("BONO_10Y"),
    datos.get("CCL"),

    datos.get("USDARS_open"),
    datos.get("USDARS_high"),
    datos.get("USDARS_low"),
    datos.get("USDARS_close"),
    datos.get("USDARS_adj"),
    datos.get("USDARS_volume"),

    datos.get("USDARS_SMA5"),
    datos.get("USDARS_SMA10"),
    datos.get("USDARS_SMA20"),
    datos.get("USDARS_RSI14"),
    datos.get("USDARS_MACD"),
    datos.get("USDARS_MACD_signal")
))

conn.commit()
cursor.close()
conn.close()

print("Datos guardados en PostgreSQL")
print(datos)
