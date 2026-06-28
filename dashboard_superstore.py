"""
Dashboard Interactivo - Análisis de Ventas Superstore
=====================================================
Ejecutar con: python dashboard_superstore.py
Acceder en: http://127.0.0.1:8050
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input

# === CARGAR Y PREPARAR DATOS ===
df = pd.read_csv('Superstore_Sales.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

# Traducciones
df['Segmento'] = df['Segment'].map({
    'Consumer': 'Consumidor', 'Corporate': 'Corporativo', 'Home Office': 'Oficina en casa'
})
df['Categoría'] = df['Category'].map({
    'Furniture': 'Muebles', 'Office Supplies': 'Suministros de oficina', 'Technology': 'Tecnología'
})
df['Subcategoría'] = df['Sub-Category'].map({
    'Bookcases': 'Estanterías', 'Chairs': 'Sillas', 'Labels': 'Etiquetas',
    'Tables': 'Mesas', 'Storage': 'Almacenamiento', 'Furnishings': 'Decoración',
    'Art': 'Arte', 'Phones': 'Teléfonos', 'Binders': 'Carpetas',
    'Appliances': 'Electrodomésticos', 'Paper': 'Papel', 'Accessories': 'Accesorios',
    'Envelopes': 'Sobres', 'Fasteners': 'Sujetadores', 'Supplies': 'Insumos',
    'Machines': 'Máquinas', 'Copiers': 'Copiadoras'
})
df['Modo de envío'] = df['Ship Mode'].map({
    'Standard Class': 'Clase estándar', 'Second Class': 'Segunda clase',
    'First Class': 'Primera clase', 'Same Day': 'Mismo día'
})
df['Región'] = df['Region'].map({
    'South': 'Sur', 'West': 'Oeste', 'Central': 'Central', 'East': 'Este'
})

# === PALETA DE COLORES ===
PALETA = ['#1B3A5C', '#5B2D8E', '#2E8B8B', '#C4A835']
PALETA_EXTENDIDA = ['#1B3A5C', '#5B2D8E', '#2E8B8B', '#C4A835', '#3D6098', '#7B4DB5', '#4AAFAF', '#8E7CC3']
COLOR_FONDO = '#F8F9FA'
COLOR_TARJETA = '#FFFFFF'

# === KPIs ===
ventas_totales = df['Sales'].sum()
total_ordenes = df['Order ID'].nunique()
total_transacciones = len(df)
ticket_promedio = ventas_totales / total_transacciones  # Promedio por transacción (línea de venta)
total_clientes = df['Customer ID'].nunique()
envio_promedio = df['Shipping Days'].mean()

# Crecimiento YoY (último año vs penúltimo)
ventas_por_año = df.groupby('Order Year')['Sales'].sum()
años = sorted(ventas_por_año.index)
if len(años) >= 2:
    ventas_ultimo = ventas_por_año[años[-1]]
    ventas_penultimo = ventas_por_año[años[-2]]
    crecimiento_yoy = ((ventas_ultimo - ventas_penultimo) / ventas_penultimo) * 100
else:
    crecimiento_yoy = 0

# Variación envío promedio YoY
envio_por_año = df.groupby('Order Year')['Shipping Days'].mean()
if len(años) >= 2:
    envio_ultimo = envio_por_año[años[-1]]
    envio_penultimo = envio_por_año[años[-2]]
    variacion_envio = ((envio_ultimo - envio_penultimo) / envio_penultimo) * 100
else:
    variacion_envio = 0

# === CREAR APP DASH ===
app = Dash(__name__)
app.title = "Dashboard Superstore - Análisis de Ventas"

# === ESTILO GLOBAL PARA TEXTOS GRANDES ===
ESTILO_TITULO_PRINCIPAL = {
    'fontSize': '42px', 'fontWeight': 'bold', 'color': '#1B3A5C',
    'textAlign': 'center', 'marginBottom': '10px', 'fontFamily': 'Segoe UI, Arial'
}
ESTILO_SUBTITULO = {
    'fontSize': '20px', 'color': '#5A6C7D', 'textAlign': 'center',
    'marginBottom': '30px', 'fontFamily': 'Segoe UI, Arial'
}
ESTILO_KPI_VALOR = {
    'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1B3A5C',
    'marginBottom': '2px', 'marginTop': '0px', 'fontFamily': 'Segoe UI, Arial'
}
ESTILO_KPI_LABEL = {
    'fontSize': '13px', 'color': '#5A6C7D', 'fontFamily': 'Segoe UI, Arial', 'marginBottom': '0px'
}
ESTILO_TARJETA = {
    'backgroundColor': COLOR_TARJETA, 'borderRadius': '10px',
    'padding': '15px 20px', 'textAlign': 'center',
    'boxShadow': '0 2px 6px rgba(0,0,0,0.06)', 'margin': '8px'
}
ESTILO_GRAFICO_CONTAINER = {
    'backgroundColor': COLOR_TARJETA, 'borderRadius': '12px',
    'padding': '20px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
    'margin': '15px 0'
}

# Layout global para gráficos con textos grandes
LAYOUT_DASHBOARD = dict(
    font=dict(family='Segoe UI, Arial', size=16, color='#2C3E50'),
    title=dict(font=dict(size=24, color='#1B3A5C', family='Segoe UI Semibold'), x=0.5, xanchor='center'),
    xaxis=dict(
        title_font=dict(size=18, color='#2C3E50'),
        tickfont=dict(size=14, color='#5A6C7D'),
        gridcolor='#E8ECF0'
    ),
    yaxis=dict(
        title_font=dict(size=18, color='#2C3E50'),
        tickfont=dict(size=14, color='#5A6C7D'),
        gridcolor='#E8ECF0'
    ),
    plot_bgcolor='#FAFBFD',
    paper_bgcolor='white',
    margin=dict(t=80, b=60, l=80, r=40),
    hoverlabel=dict(bgcolor='white', font_size=14, font_family='Segoe UI'),
    legend=dict(font=dict(size=14))
)


# === FUNCIONES DE GRÁFICOS ===
def crear_grafico_lineas():
    """Evolución temporal de ventas por año"""
    ventas_mes = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
    ventas_mes.columns = ['Año', 'Mes', 'Ventas']

    fig = px.line(
        ventas_mes, x='Mes', y='Ventas', color='Año',
        title='Evolución Mensual de Ventas por Año',
        labels={'Mes': 'Mes del año', 'Ventas': 'Ventas (USD)', 'Año': 'Año'},
        color_discrete_sequence=PALETA,
        markers=True
    )
    fig.update_traces(line_width=3, marker_size=9)
    fig.update_layout(**LAYOUT_DASHBOARD)
    fig.update_layout(
        legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2, font=dict(size=16)),
        xaxis=dict(dtick=1)
    )
    return fig


def crear_grafico_barras_categoria():
    """Ventas por categoría (animado por año)"""
    ventas_cat = df.groupby(['Order Year', 'Categoría'])['Sales'].sum().reset_index()
    ventas_cat.columns = ['Año', 'Categoría', 'Ventas']

    fig = px.bar(
        ventas_cat, x='Categoría', y='Ventas', color='Categoría',
        animation_frame='Año',
        title='Ventas por Categoría (Evolución Anual)',
        labels={'Ventas': 'Ventas (USD)', 'Categoría': 'Categoría'},
        color_discrete_sequence=PALETA[:3],
        text_auto='.2s'
    )
    fig.update_traces(textfont_size=16, textposition='outside')
    fig.update_layout(**LAYOUT_DASHBOARD)
    fig.update_layout(showlegend=False, yaxis_range=[0, ventas_cat['Ventas'].max() * 1.2])
    return fig


def crear_grafico_subcategorias():
    """Top subcategorías por ventas"""
    ventas_sub = df.groupby('Subcategoría')['Sales'].sum().sort_values(ascending=True).tail(10).reset_index()
    ventas_sub.columns = ['Subcategoría', 'Ventas']

    fig = px.bar(
        ventas_sub, x='Ventas', y='Subcategoría', orientation='h',
        title='Top 10 Subcategorías por Ventas',
        labels={'Ventas': 'Ventas (USD)', 'Subcategoría': ''},
        color='Ventas', color_continuous_scale=['#C4A835', '#5B2D8E', '#1B3A5C'],
        text_auto='.3s'
    )
    fig.update_traces(textfont_size=14, textposition='outside')
    fig.update_layout(**LAYOUT_DASHBOARD)
    fig.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(tickfont=dict(size=15)),
        margin=dict(t=80, b=60, l=140, r=80),
        xaxis=dict(range=[0, ventas_sub['Ventas'].max() * 1.18])
    )
    return fig


def crear_grafico_region():
    """Distribución de ventas por región"""
    ventas_reg = df.groupby('Región')['Sales'].sum().reset_index()
    ventas_reg.columns = ['Región', 'Ventas']
    ventas_reg = ventas_reg.sort_values('Región').reset_index(drop=True)

    fig = px.pie(
        ventas_reg, values='Ventas', names='Región',
        title='Distribución de Ventas por Región',
        color_discrete_sequence=PALETA,
        hole=0.4
    )
    fig.update_traces(
        textposition='outside', textinfo='label+percent',
        textfont_size=16, pull=[0] * len(ventas_reg)
    )
    fig.update_layout(**LAYOUT_DASHBOARD)
    return fig


def crear_grafico_segmento():
    """Ventas por segmento y categoría"""
    ventas_seg = df.groupby(['Segmento', 'Categoría'])['Sales'].sum().reset_index()
    ventas_seg.columns = ['Segmento', 'Categoría', 'Ventas']

    fig = px.bar(
        ventas_seg, x='Segmento', y='Ventas', color='Categoría',
        title='Ventas por Segmento y Categoría',
        labels={'Ventas': 'Ventas (USD)', 'Segmento': ''},
        color_discrete_sequence=PALETA[:3],
        barmode='group', text_auto='.2s'
    )
    fig.update_traces(textfont_size=13, textposition='outside')
    fig.update_layout(**LAYOUT_DASHBOARD)
    fig.update_layout(legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2, font=dict(size=15)))
    return fig


def crear_grafico_envio():
    """Distribución de tiempos de envío por modo"""
    fig = px.box(
        df, x='Modo de envío', y='Shipping Days', color='Modo de envío',
        title='Tiempos de Envío por Modalidad',
        labels={'Shipping Days': 'Días de envío', 'Modo de envío': ''},
        color_discrete_sequence=PALETA
    )
    fig.update_layout(**LAYOUT_DASHBOARD)
    fig.update_layout(showlegend=False)
    return fig


# === LAYOUT DEL DASHBOARD ===
app.layout = html.Div(style={'backgroundColor': COLOR_FONDO, 'minHeight': '100vh', 'padding': '30px'}, children=[

    # Título principal
    html.H1("Dashboard de Ventas - Superstore", style=ESTILO_TITULO_PRINCIPAL),
    html.P("Análisis interactivo de ventas y rentabilidad | Dataset: Superstore Sales (2015-2018)",
           style=ESTILO_SUBTITULO),

    # === FILA DE KPIs (3 arriba + 3 abajo) ===
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap', 'marginBottom': '5px'}, children=[
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"${ventas_totales:,.0f}", style=ESTILO_KPI_VALOR),
            html.P("Ventas Totales", style=ESTILO_KPI_LABEL),
            html.P(f"▲ {crecimiento_yoy:+.1f}% YoY", style={
                'fontSize': '12px', 'color': '#27AE60' if crecimiento_yoy >= 0 else '#E74C3C',
                'fontWeight': 'bold', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"{total_ordenes:,}", style=ESTILO_KPI_VALOR),
            html.P("Órdenes Únicas", style=ESTILO_KPI_LABEL),
            html.P(f"{total_transacciones:,} transacciones", style={
                'fontSize': '11px', 'color': '#5A6C7D', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"${ticket_promedio:,.0f}", style=ESTILO_KPI_VALOR),
            html.P("Ticket Promedio", style=ESTILO_KPI_LABEL),
            html.P("por transacción", style={
                'fontSize': '11px', 'color': '#5A6C7D', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
    ]),
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"{total_clientes:,}", style=ESTILO_KPI_VALOR),
            html.P("Clientes Únicos", style=ESTILO_KPI_LABEL),
            html.P(f"{len(df['State'].unique())} estados", style={
                'fontSize': '11px', 'color': '#5A6C7D', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"{crecimiento_yoy:+.1f}%", style=ESTILO_KPI_VALOR | {
                'color': '#27AE60' if crecimiento_yoy >= 0 else '#E74C3C'
            }),
            html.P("Crecimiento YoY", style=ESTILO_KPI_LABEL),
            html.P(f"{'▲' if crecimiento_yoy >= 0 else '▼'} {años[-1]} vs {años[-2]}", style={
                'fontSize': '11px', 'color': '#27AE60' if crecimiento_yoy >= 0 else '#E74C3C',
                'fontWeight': 'bold', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
        html.Div(style=ESTILO_TARJETA | {'flex': '1', 'minWidth': '220px', 'maxWidth': '280px'}, children=[
            html.P(f"{envio_promedio:.1f} días", style=ESTILO_KPI_VALOR),
            html.P("Envío Promedio", style=ESTILO_KPI_LABEL),
            html.P(f"{'▼' if variacion_envio <= 0 else '▲'} {variacion_envio:+.1f}% YoY", style={
                'fontSize': '12px', 'color': '#27AE60' if variacion_envio <= 0 else '#E74C3C',
                'fontWeight': 'bold', 'marginTop': '3px', 'marginBottom': '0px', 'fontFamily': 'Segoe UI, Arial'
            })
        ]),
    ]),

    # === FILTRO INTERACTIVO ===
    html.Div(style=ESTILO_GRAFICO_CONTAINER | {'marginBottom': '20px'}, children=[
        html.Label("Filtrar por Región:", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#1B3A5C', 'marginRight': '15px'}),
        dcc.Dropdown(
            id='filtro-region',
            options=[{'label': 'Todas', 'value': 'Todas'}] + [{'label': r, 'value': r} for r in sorted(df['Región'].unique())],
            value='Todas',
            style={'width': '250px', 'fontSize': '16px', 'display': 'inline-block', 'verticalAlign': 'middle'}
        )
    ]),

    # === FILA 1: Evolución temporal + Categorías ===
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}, children=[
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-lineas', figure=crear_grafico_lineas(), config={'displayModeBar': True})
        ]),
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-categorias', figure=crear_grafico_barras_categoria(), config={'displayModeBar': True})
        ]),
    ]),

    # === FILA 2: Subcategorías + Región ===
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}, children=[
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-subcategorias', figure=crear_grafico_subcategorias(), config={'displayModeBar': True})
        ]),
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-region', figure=crear_grafico_region(), config={'displayModeBar': True})
        ]),
    ]),

    # === FILA 3: Segmentos + Tiempos de envío ===
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}, children=[
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-segmento', figure=crear_grafico_segmento(), config={'displayModeBar': True})
        ]),
        html.Div(style=ESTILO_GRAFICO_CONTAINER | {'flex': '1', 'minWidth': '500px'}, children=[
            dcc.Graph(id='grafico-envio', figure=crear_grafico_envio(), config={'displayModeBar': True})
        ]),
    ]),

    # === PIE DE PÁGINA ===
    html.Div(style={'textAlign': 'center', 'marginTop': '40px', 'padding': '20px', 'color': '#8E99A4'}, children=[
        html.P("Evaluación Parcial 3 - Programación para la Ciencia de Datos", style={'fontSize': '16px'}),
        html.P("Dashboard desarrollado con Python, Pandas, Plotly y Dash", style={'fontSize': '14px'})
    ])
])


# === CALLBACKS INTERACTIVOS ===
@callback(
    [Output('grafico-lineas', 'figure'),
     Output('grafico-subcategorias', 'figure'),
     Output('grafico-segmento', 'figure'),
     Output('grafico-envio', 'figure'),
     Output('grafico-region', 'figure')],
    Input('filtro-region', 'value')
)
def actualizar_por_region(region):
    """Filtra los gráficos según la región seleccionada"""
    if region == 'Todas':
        df_filtrado = df
    else:
        df_filtrado = df[df['Región'] == region]

    # Gráfico de líneas
    ventas_mes = df_filtrado.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
    ventas_mes.columns = ['Año', 'Mes', 'Ventas']
    fig_lineas = px.line(
        ventas_mes, x='Mes', y='Ventas', color='Año',
        title=f'Evolución Mensual de Ventas por Año{" - " + region if region != "Todas" else ""}',
        labels={'Mes': 'Mes del año', 'Ventas': 'Ventas (USD)', 'Año': 'Año'},
        color_discrete_sequence=PALETA, markers=True
    )
    fig_lineas.update_traces(line_width=3, marker_size=9)
    fig_lineas.update_layout(**LAYOUT_DASHBOARD)
    fig_lineas.update_layout(legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2, font=dict(size=16)), xaxis=dict(dtick=1))

    # Gráfico subcategorías
    ventas_sub = df_filtrado.groupby('Subcategoría')['Sales'].sum().sort_values(ascending=True).tail(10).reset_index()
    ventas_sub.columns = ['Subcategoría', 'Ventas']
    fig_sub = px.bar(
        ventas_sub, x='Ventas', y='Subcategoría', orientation='h',
        title=f'Top 10 Subcategorías{" - " + region if region != "Todas" else ""}',
        labels={'Ventas': 'Ventas (USD)', 'Subcategoría': ''},
        color='Ventas', color_continuous_scale=['#C4A835', '#5B2D8E', '#1B3A5C'], text_auto='.3s'
    )
    fig_sub.update_traces(textfont_size=14, textposition='outside')
    fig_sub.update_layout(**LAYOUT_DASHBOARD)
    fig_sub.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(tickfont=dict(size=15)),
        margin=dict(t=80, b=60, l=140, r=80),
        xaxis=dict(range=[0, ventas_sub['Ventas'].max() * 1.18])
    )

    # Gráfico segmento
    ventas_seg = df_filtrado.groupby(['Segmento', 'Categoría'])['Sales'].sum().reset_index()
    ventas_seg.columns = ['Segmento', 'Categoría', 'Ventas']
    fig_seg = px.bar(
        ventas_seg, x='Segmento', y='Ventas', color='Categoría',
        title=f'Ventas por Segmento y Categoría{" - " + region if region != "Todas" else ""}',
        labels={'Ventas': 'Ventas (USD)', 'Segmento': ''},
        color_discrete_sequence=PALETA[:3], barmode='group', text_auto='.2s'
    )
    fig_seg.update_traces(textfont_size=13, textposition='outside')
    fig_seg.update_layout(**LAYOUT_DASHBOARD)
    fig_seg.update_layout(legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2, font=dict(size=15)))

    # Gráfico envío
    fig_envio = px.box(
        df_filtrado, x='Modo de envío', y='Shipping Days', color='Modo de envío',
        title=f'Tiempos de Envío{" - " + region if region != "Todas" else ""}',
        labels={'Shipping Days': 'Días de envío', 'Modo de envío': ''},
        color_discrete_sequence=PALETA
    )
    fig_envio.update_layout(**LAYOUT_DASHBOARD)
    fig_envio.update_layout(showlegend=False)

    # Gráfico de región (dona) - siempre usa datos completos, resalta la seleccionada
    ventas_reg = df.groupby('Región')['Sales'].sum().reset_index()
    ventas_reg.columns = ['Región', 'Ventas']
    ventas_reg = ventas_reg.sort_values('Región').reset_index(drop=True)

    # Pull dinámico: resalta la región seleccionada
    if region == 'Todas':
        pull_values = [0] * len(ventas_reg)
    else:
        pull_values = [0.08 if r == region else 0 for r in ventas_reg['Región']]

    fig_region = px.pie(
        ventas_reg, values='Ventas', names='Región',
        title=f'Distribución de Ventas por Región{" (seleccionada: " + region + ")" if region != "Todas" else ""}',
        color_discrete_sequence=PALETA,
        hole=0.4
    )
    fig_region.update_traces(
        textposition='outside', textinfo='label+percent',
        textfont_size=16, pull=pull_values
    )
    fig_region.update_layout(**LAYOUT_DASHBOARD)

    return fig_lineas, fig_sub, fig_seg, fig_envio, fig_region


# === EJECUTAR SERVIDOR ===
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  DASHBOARD SUPERSTORE - ANÁLISIS DE VENTAS")
    print("  Abrir en navegador: http://127.0.0.1:8050")
    print("=" * 60 + "\n")
    app.run(debug=True)
