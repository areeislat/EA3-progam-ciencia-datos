# Análisis de Ventas y Rentabilidad - Superstore Sales

Proyecto de la **Evaluación Parcial 3** de Programación para la Ciencia de Datos. Análisis exploratorio de datos de ventas con visualizaciones interactivas y dashboard web.

## Objetivo

Analizar qué categorías, subcategorías, regiones y segmentos de clientes están asociados a mejores o peores resultados comerciales, utilizando el dataset Superstore Sales (9,800 registros, periodo 2015-2018).

## Herramientas utilizadas

| Herramienta | Uso |
|-------------|-----|
| Python 3.x | Lenguaje principal |
| Pandas | Manejo y limpieza de datos |
| Plotly | Visualizaciones interactivas |
| Dash | Dashboard web interactivo |
| Jupyter Notebook | Desarrollo del análisis |
| python-pptx + Kaleido | Generación de presentación PPT |
| Git / GitHub | Control de versiones |

## Estructura del repositorio

```
├── analisis_superstore.ipynb      # Notebook con análisis completo y visualizaciones
├── dashboard_superstore.py        # Dashboard interactivo con Dash
├── generar_presentacion.py        # Script generador de la presentación PPT
├── Presentacion_Superstore_DuocUC.pptx   # Presentación 
├── informe_EA3.md                 # Informe del proyecto
├── Superstore_Sales.csv           # Dataset original
├── requirements.txt               # Dependencias del proyecto
├── readme.md                      # Este archivo
└── img_ppt/                       # Imágenes de gráficos para la PPT
```

## Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el notebook (análisis completo)
```bash
jupyter notebook analisis_superstore.ipynb
```

### 3. Ejecutar el dashboard interactivo
```bash
python dashboard_superstore.py
```
Abrir en el navegador: http://127.0.0.1:8050

## Análisis realizados

- Limpieza de datos (nulos, duplicados, tipos de datos)
- Creación de variables derivadas (año, mes, días de envío)
- Traducción de campos categóricos al español
- Evolución temporal de ventas (gráfico de líneas)
- Ventas por categoría con animación anual (barras)
- Ranking de subcategorías (barras horizontales)
- Distribución por región (dona interactiva)
- Segmentación de clientes (barras agrupadas)
- Análisis logístico de tiempos de envío (boxplot)
- Top 10 estados por facturación
- Mini dashboard con KPIs y métricas clave

## Dashboard (Dash)

El dashboard incluye:
- 6 KPIs con indicadores de tendencia (▲▼)
- Filtro interactivo por región
- 6 gráficos que se actualizan dinámicamente
- Diseño responsive con paleta profesional

## Principales hallazgos

1. **Crecimiento sostenido** — Ventas con tendencia positiva interanual (+20.3% YoY)
2. **Tecnología lidera** — $827K (36.6% del total), mayor potencial de crecimiento
3. **Consumidor dominante** — 50.8% del mercado, pero Corporativo ofrece mayor estabilidad
4. **Concentración geográfica** — Oeste + Este = 61% de ingresos
5. **Oportunidad logística** — Clase estándar con variabilidad en tiempos de entrega
