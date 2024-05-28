import streamlit as st
import base64
import pandas as pd
import streamlit.components.v1 as components  # Corrección en la importación de components
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import geopandas as gpd # Para manejo de datos geoespaciales 
import plotly.express as px



reportes_df = pd.read_csv('reportes_agua_hist.csv')
colonias_gdf = gpd.read_file('colonias_conteo.geojson')



# Filtrar reportes para el año 2021
reportes_df['fecha'] = pd.to_datetime(reportes_df['fecha'])
reportes_2021 = reportes_df[reportes_df['fecha'].dt.year == 2021]
#eliminar los valores NaN
reportes_2021 = reportes_2021.dropna()


# CSS personalizado
st.markdown("""
    <style>
    .header {
        position: fixed;
        top: 50px;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        border-bottom: 2px solid #e9ecef;
        background-color: rgb(14, 17, 23);
        z-index: 1000;    }
    .header img {
        height: 50px;
    }
    .header .title {
        font-size: 24px;
        font-weight: bold;
    }
    .nav {
        display: flex;
        gap: 15px;
    }
    .nav a {
        text-decoration: none;
        color: white;
        font-weight: bold;
    }
    
    </style>
""", unsafe_allow_html=True)

# HTML personalizado para el encabezado
st.markdown("""
    <div class="header">
        <img src="data:image/png;base64,{}" class="logo">
        <div class="title">Reportes de falta de agua en CDMX</div>
        <div class="nav">
            <a href="#mapa-de-reportes-de-falta-de-agua-en-cdmx">Mapa</a>
            <a href="#d7139f63">Alcaldías</a>
            <a href="#dd0c9ac6">Colonias</a>
            <a href="#analisis">Análisis</a>
        </div>
    </div>
""".format(base64.b64encode(open("logo_udc.png", "rb").read()).decode()), unsafe_allow_html=True)
mapa = """ 
El primer paso para entender este problema es visualizar la distribución de los reportes de falta de agua en la Ciudad de México. Para ello se analizaron los datos de la SACMEX sobre todos los reportes recibidos en 2021
"""

description = """ 
La falta de agua en la Ciudad de México es un problema recurrente que afecta a miles de personas cada año. Y no es noticia nueva que esto este sucediendo, a pesar de que solo recientemente ha salido a la luz este dilema. Según datos de SACMEX (Sistema de Aguas de la Ciudad de México), en 2021 se registraron más de 10,000 reportes de falta de agua en la Ciudad de México. Nosotros somos Alejandro Paredes, Paola Robles, Rubén Reyna y Rubén Silva un equipo de amigos y compañeros que nos enfocamos en el análisis de datos para poder entender mejor este problema y poder proponer soluciones."""

# Título y descripción de la aplicación
st.title('La falta de agua en la Ciudad de México en 2021')
st.markdown(description)

# Mostrar el mapa
st.markdown('## Mapa de reportes de falta de agua en CDMX')
st.markdown(mapa)

# Asegúrate de que la ruta del archivo HTML es correcta
with open('mapa.html', 'r', encoding='utf-8') as f:
    html_data = f.read()
components.html(html_data, width=700, height=500)
st.caption("Mapa 1: mapa interactivo de la ciudad de Mexico, creado por Hernandez Paredes Roberto Alejandro")

# Función para reproducir el audio usando JavaScript
def play_audio(audio_file):
    audio_bytes = audio_file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    md = f"""
        <audio id="audio" autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
        document.getElementById('audio').play();
        </script>
        """
    st.markdown(md, unsafe_allow_html=True)

# Agregar CSS personalizado para posicionar el botón en la esquina inferior derecha
st.markdown(
    """
    <style>
    .fixed-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crear el botón con la clase CSS personalizada
if st.button('?', help='Haz clic para escuchar la explicación de la falta de agua en la Ciudad de México', key='fixed-button'):
    with open('reporte_voz.mp3', 'rb') as audio_file:
        play_audio(audio_file)

# Mostrar la gráfica de barras de reportes por alcaldía
# Mostrar la gráfica de barras de reportes por alcaldía
st.markdown('## Reportes de falta de agua por alcaldía en 2021')
st.markdown("""
Esta sección muestra el número de reportes de falta de agua por cada alcaldía en la Ciudad de México durante el año 2021.
Al hacer clic en una barra, se resaltará la alcaldía correspondiente para facilitar la visualización de los datos.
""")
# Gráfica de barras interactiva de reportes por alcaldía
reportes_por_alcaldia = reportes_2021['alcaldia'].value_counts().reset_index()
reportes_por_alcaldia.columns = ['Alcaldía', 'Número de reportes']

# Crear la figura
fig = go.Figure()

fig.add_trace(go.Bar(
    x=reportes_por_alcaldia['Número de reportes'],
    y=reportes_por_alcaldia['Alcaldía'],
    orientation='h',
    marker=dict(color='#19468D', line=dict(color='black', width=1)),
    name='Número de reportes'
))

fig.update_layout(
    #title='Reportes de fallas en el suministro de agua por alcaldía en 2021',
    xaxis_title='Número de reportes',
    yaxis_title='Alcaldía',
    clickmode='event+select'
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, width=1000, height=500)
st.caption("Grafica 1: Cantidad de reportes  de falta de agua por alcaldia a lo largo del tiempo en 2021.")

# Mostrar la gráfica de barras de reportes por colonia
st.markdown('## Reportes de falta de agua por colonia en Coyoacán en 2021')
st.markdown("""
En esta sección, puedes ver los reportes de falta de agua desglosados por colonia en la alcaldía de Coyoacán.
Solo se muestran las colonias que tienen más de 100 reportes durante el año 2021.
""")
alcaldia_seleccionada = 'Coyoacán'
colonias_filtradas = colonias_gdf[colonias_gdf['alc'] == alcaldia_seleccionada]

# Filtrar las colonias con más de 100 reportes
colonias_filtradas = colonias_filtradas[colonias_filtradas['conteo'] > 100]

# Ordenar las colonias por el conteo de reportes
colonias_filtradas = colonias_filtradas.sort_values(by='conteo', ascending=False)

# Crear el gráfico de barras interactivo
fig_colonias = go.Figure()

fig_colonias.add_trace(go.Bar(
    x=colonias_filtradas['conteo'],
    y=colonias_filtradas['colonia'],
    orientation='h',
    marker=dict(color='#19468D', line=dict(color='Black', width=1)),
    name='Número de reportes'
))

fig_colonias.update_layout(
    #title=f'Reportes de fallas en el suministro de agua por colonia en {alcaldia_seleccionada} con más de 100 reportes en 2021',
    xaxis_title='Número de reportes',
    yaxis_title='Colonia',
    clickmode='event+select'
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig_colonias)
st.caption(f"Grafica 2: Reportes de fallas en el suministro de agua por colonia en {alcaldia_seleccionada} con más de 100 reportes en 2021.")


# Título y descripción
st.markdown('## Reportes de falta de agua por colonia en Coyoacán en 2021')
st.markdown("""
Esta tabla muestra el número de reportes de falta de agua por colonia en la alcaldía de Coyoacán durante el año 2021.
Los datos están ordenados por fecha y puedes explorarlos para identificar patrones o tendencias en los reportes.
""")

# Lectura del archivo CSV
df = pd.read_csv('reportes_colonia_fechas.csv')

# Mostrar la tabla
st.dataframe(df, width=1000, height=500)

####Analisis de temporada ####

# Mostrar la línea de tiempo de reportes
st.markdown('## Línea de tiempo de reportes de falta de agua en CDMX en 2021')
st.markdown("""
Esta línea de tiempo muestra la evolución de los reportes de falta de agua en la Ciudad de México a lo largo del año 2021.
Puedes interactuar con la gráfica para ver los detalles de los reportes en cada mes.
""")

# Supongo que tienes los datos en un DataFrame llamado reportes_2021
# Si no lo tienes, carga los datos adecuados aquí
reportes_2021['fecha'] = pd.to_datetime(reportes_2021['fecha'])
reportes_2021['mes'] = reportes_2021['fecha'].dt.to_period('M')

reportes_por_mes = reportes_2021.groupby('mes').size().reset_index(name='Número de reportes')
reportes_por_mes['mes'] = reportes_por_mes['mes'].dt.to_timestamp()  # Convertir a timestamp

# Crear la línea de tiempo
fig_timeline = px.line(reportes_por_mes, x='mes', y='Número de reportes', title='Evolución de reportes de falta de agua en CDMX en 2021')

fig_timeline.update_layout(
    xaxis_title='Mes',
    yaxis_title='Número de reportes',
    hovermode='x unified'
)

# Mostrar la línea de tiempo en Streamlit
st.plotly_chart(fig_timeline)
st.caption("Grafica 3: Evolución de los reportes de falta de agua en la Ciudad de México a lo largo del año 2021.")




# Análisis de Día de la Semana
st.markdown('## Análisis por Día de la Semana')
st.markdown("""
Esta sección muestra si hay días de la semana con más reportes de falta de agua.
""")

# Agregar columna de día de la semana
reportes_2021['dia_semana'] = reportes_2021['fecha'].dt.day_name()

# Grafica la cantidad de reportes por día de la semana
reportes_por_dia = reportes_2021['dia_semana'].value_counts().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
fig_dia = go.Figure()

fig_dia.add_trace(go.Bar(
    x=reportes_por_dia.index,
    y=reportes_por_dia.values,
    marker=dict(color='#19468D', line=dict(color='rgba(58, 71, 80, 1.0)', width=1)),
    name='Número de reportes'
))

fig_dia.update_layout(
    title='Cantidad de reportes por día de la semana en 2021',
    xaxis_title='Día de la semana',
    yaxis_title='Número de reportes',
    clickmode='event+select'
)
st.plotly_chart(fig_dia)
st.caption("Grafica 4: Cantidad de reportes de falta de agua por día de la semana en 2021.")




##### Graficas de ruben #####

#abrir el archivo

st.markdown('## Caracteristicas de las viviendas en colonias con mas reportes de falta de agua')


# Lectura del archivo CSV
reportes_df = pd.read_csv('sumado.csv')

# Renombrar las columnas del DataFrame
reportes_df.rename(columns={
    "VPH_AEASP": "Disponen de agua entubada",
    "VPH_AGUAFV": "No disponen de agua entubada",
    "VPH_TINACO": "Tienen tinaco",
    "VPH_CISTER": "Tienen cisterna",
    "VPH_EXCSA": "Tienen excusado",
    "VPH_LETR": "Tienen letrina",
    "VPH_DRENAJ": "Tienen drenaje",
    "VPH_NODREN": "No tienen drenaje",
    "VPH_CEL": "Tienen teléfonos",
    "VPH_TV": "Tienen televisión"
}, inplace=True)

# Crear la figura
df_sums = reportes_df.drop(columns=['count'])
df_sums = df_sums.sum().reset_index()
df_sums.columns = ['Característica', 'Cantidad']

fig_viviendas = go.Figure()

fig_viviendas.add_trace(go.Bar(
    x=df_sums['Cantidad'],
    y=df_sums['Característica'],
    orientation='h',
    marker=dict(color='#19468D', line=dict(color='Black', width=1)),
    name='Cantidad de viviendas'
))

fig_viviendas.update_layout(
    #title='Características de las viviendas en Coyoacán',
    xaxis_title='Cantidad de viviendas',
    yaxis_title='Características de las viviendas',
    clickmode='event+select'
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig_viviendas)
st.caption("Grafica 5: Características de las viviendas en la alcaldía de Coyoacán.")

