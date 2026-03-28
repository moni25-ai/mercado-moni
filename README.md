# Analizador Automático del Mercado Argentino y Global

Este proyecto realiza un análisis automático y periódico del mercado financiero utilizando datos de Yahoo Finance y la API del dólar argentino. La información recopilada se guarda en una base de datos Supabase para posteriores análisis avanzados.

---

## 🚀 ¿Qué hace este proyecto?

- Obtiene cada hora datos macro y financieros clave:
  - Oro (Gold)
  - Petróleo (Brent/WTI)
  - Índice S&P 500
  - Bonos del Tesoro estadounidense
  - ETFs relevantes

- Obtiene cotizaciones del mercado argentino:
  - Dólar Oficial
  - Dólar Blue
  - Dólar Bolsa (MEP)
  - Dólar CCL (calculado mediante fórmula con activos duales)

- Guarda todos los datos automáticamente en Supabase.
- Todo el proceso corre mediante GitHub Actions.

---

## 🧠 Estructura del proyecto

```
/ (raíz del repositorio)
│
├── scripts/
│   └── market_fetch.py        # Script principal que obtiene y procesa los datos
│
├── workflows/
│   └── fetch_market.yml       # GitHub Actions: automatización para ejecutar el script
│
├── docs/
│   └── niveles_subagentes.md  # Definiciones internas de subagentes y arquitectura
│
└── README.md                   # Este archivo
```

---

## 🚀 Ejecución automática

Este sistema se ejecuta cada 1 hora mediante GitHub Actions.  
Cada ejecución extrae los datos, calcula indicadores y guarda todo en Supabase automáticamente.

---

## 📬 Futuras mejoras

- Modelo predictivo ARIMA / Prophet.
- Envío de alertas a Telegram.
- Tablero visual en Streamlit / PowerBI.
- Más indicadores para dólar MEP, CCL y riesgo país.
- Subagentes especializados para tareas independientes.

---

## ✨ Estado actual del proyecto

- **Subagente 1:** ✔ Completo  
- **Subagente 2:** ⏳ Pendiente  
- **Subagente 3:** ⏳ Próximo  
- **Agente Principal:** ⏳ En desarrollo  

---

