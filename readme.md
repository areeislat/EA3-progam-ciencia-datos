# Superstore Sales Analysis

Este proyecto analiza datos de ventas de una tienda Superstore con el objetivo de identificar patrones de ventas y rentabilidad por categorías, regiones y segmentos de clientes.

## Objetivo

Analizar qué categorías, subcategorías, regiones y segmentos de clientes están asociados a mejores o peores resultados comerciales, utilizando visualizaciones interactivas para comunicar los hallazgos.

## Herramientas utilizadas

- Python
- Pandas
- Plotly (visualizaciones interactivas)
- Jupyter Notebook
- Git y GitHub

## Contenido del repositorio

- `Superstore_Sales.csv`: dataset utilizado para el análisis.
- `analisis_superstore.ipynb`: notebook principal con todo el desarrollo del análisis.
- `requirements.txt`: librerías necesarias para ejecutar el proyecto.

## Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Abrir el notebook:
   ```bash
   jupyter notebook analisis_superstore.ipynb
   ```

## Principales análisis realizados

- Limpieza básica de datos (nulos, duplicados).
- Conversión de fechas a formato datetime.
- Creación de variables derivadas (año, mes, días de envío).
- Análisis temporal de ventas (evolución mensual).
- Análisis de ventas por categoría y subcategoría.
- Análisis por región y segmento de clientes.
- Análisis de tiempos de envío por modo.
- Top 10 estados por ventas.
- Mini dashboard consolidado con indicadores clave.

## Visualizaciones incluidas

- Gráfico de líneas: evolución mensual de ventas.
- Gráfico de barras: ventas por categoría y subcategoría.
- Gráfico de dispersión: relación órdenes vs venta promedio por región.
- Gráfico de barras agrupadas: ventas por segmento y categoría.
- Boxplot: distribución de días de envío.
- Dashboard con subplots (pies y barras).