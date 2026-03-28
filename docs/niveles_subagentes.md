# Niveles de Subagentes y Arquitectura Interna del Sistema

Este documento define la estructura interna del proyecto, los roles, las responsabilidades y el flujo de trabajo de los subagentes y del agente principal.  
Su objetivo es organizar y profesionalizar el sistema, permitiendo que cada componente tenga funciones claras y escalables.

---

# 🧩 Arquitectura General

El sistema está dividido en **subagentes** y un **agente principal**, cada uno encargado de tareas específicas:

- **Subagentes** → Tareas automatizadas, repetitivas o técnicas.
- **Agente Principal** → Integración, análisis profundo y toma de decisiones.

Esta separación permite que el proyecto crezca sin volverse caótico.

---

# 🟦 Subagente 1 — Extracción y Carga de Datos (ETL)
**Estado:** ✔ Completo  
**Archivo relacionado:** `scripts/market_fetch.py`

### ✔ Responsabilidades principales
- Conectarse a Yahoo Finance y obtener indicadores globales.
- Obtener todas las cotizaciones del dólar argentino vía API.
- Calcular el CCL mediante fórmula con activos duales.
- Transformar y normalizar datos.
- Guardar resultados en Supabase.
- Registrar logs básicos para auditoría.

### ✔ Qué NO hace
- No analiza tendencias.
- No genera alertas.
- No predice movimientos.

**Rol:** Es el “motor base” del sistema.

---

# 🟧 Subagente 2 — Análisis Técnico Inicial
**Estado:** ⏳ Pendiente  
**Archivo futuro:** `scripts/technical_analysis.py`

### 🛠 Funciones previstas
- Calcular indicadores avanzados:
  - RSI
  - MACD
  - Medias móviles (SMA/EMA)
  - Bandas de Bollinger
- Detectar señales simples:
  - Sobrecompra / sobreventa
  - Cruces de medias
- Guardar estos indicadores en Supabase.

**Rol:** Preprocesar señales para el agente principal.

---

# 🟪 Subagente 3 — Señales de Mercado y Reglas Inteligentes
**Estado:** ⏳ Próximo  
**Archivo futuro:** `scripts/signal_engine.py`

### 🛠 Funciones previstas
- Interpretar indicadores técnicos junto con datos macro.
- Generar señales como:
  - “Atención: CCL subiendo más de X%”
  - “El oro rompe resistencia”
  - “El S&P 500 entra en zona de miedo”
- Emitir alertas hacia Telegram o Discord.
- Crear un mapa de riesgo diario.

**Rol:** Convertir datos en información accionable.

---

# 🟩 Agente Principal — Análisis Integral y Decisiones
**Estado:** ⏳ En desarrollo  
**Archivo futuro:** `scripts/master_agent.py`

### 🧠 Funciones previstas
- Conectar todos los subagentes.
- Generar informes automáticos:
  - Riesgo macro
  - Fuerza del dólar
  - Estado del mercado global
- Identificar correlaciones no evidentes.
- Evaluar oportunidades basadas en contexto.
- Ejecutar o recomendar acciones.

**Rol:** La “inteligencia central” del sistema.

---

# 🔄 Flujo de Trabajo General

```
Subagente 1 (ETL)
        ↓
Subagente 2 (Indicadores)
        ↓
Subagente 3 (Señales)
        ↓
Agente Principal (Análisis Integral)
```

Cada nivel depende del anterior y amplía la capacidad del sistema.

---

# 🧱 Estándares Técnicos del Proyecto

### 📌 Nombres de archivos
- `market_fetch.py` → Subagente 1  
- `technical_analysis.py` → Subagente 2  
- `signal_engine.py` → Subagente 3  
- `master_agent.py` → Agente Principal  

### 📌 Formato de logs
- Fecha y hora  
- Subagente ejecutado  
- Estado final (OK / ERROR)  
- Detalles clave (cantidad de registros, símbolos usados)

### 📌 Estilo de código
- Python 3.11+
- PEP8  
- Modularidad estricta  
- 1 subagente = 1 responsabilidad

---

# 🧭 Futuras ampliaciones

- Subagente 4 → News Sentiment (análisis de noticias)
- Subagente 5 → Correlaciones históricas
- Subagente 6 → Análisis de flujos (volumen)
- Agente Principal v2 → Capacidad predictiva híbrida

---

# 💠 Propósito

Este documento sirve como guía oficial de arquitectura.  
Permite mantener claridad, profesionalismo y escalabilidad a medida que el sistema crece.

