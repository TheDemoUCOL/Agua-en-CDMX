import streamlit as st
import base64
import pandas as pd
import streamlit.components.v1 as components  # Corrección en la importación de components
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import geopandas as gpd # Para manejo de datos geoespaciales 



reportes_df = pd.read_csv('reportes_agua_hist.csv')
colonias_gdf = gpd.read_file('colonias_conteo.geojson')

# Filtrar reportes para el año 2021
reportes_df['fecha'] = pd.to_datetime(reportes_df['fecha'])
reportes_2021 = reportes_df[reportes_df['fecha'].dt.year == 2021]
#eliminar los valores NaN
reportes_2021 = reportes_2021.dropna()
planteamiento = """
La falta de agua el la capital del país, no es una noticia nueva, con la llegada de esta temprada de calor, se ha vuelto un problema más recurrente, todos los días recibimos noticias sobre la ciudad de México que los vecinos pelean a capa y espada las pocas pipas de agua que llegan a suministrar este preciado líquido que es vital para todos. Sin embargo este problema no es único de esta temporada, es un problema concurrente y durante esta investigación hemos analizado la información de la SACMEX para poder entender un poco más sobre este problema. 
"""

# Título y descripción de la aplicación
st.title('Reportes de falta de agua en CDMX')
st.markdown(planteamiento)

# Mostrar el mapa
st.markdown('## Mapa de reportes de falta de agua en CDMX')
st.markdown("""
En este mapa puedes visualizar los reportes de falta de agua registrados en la Ciudad de México durante el año 2021.
El mapa te permite seleccionar las capas de datos que deseas visualizar para obtener una mejor comprensión de la distribución
de los reportes.
""")

# Asegúrate de que la ruta del archivo HTML es correcta
with open('mapa.html', 'r', encoding='utf-8') as f:
    html_data = f.read()
components.html(html_data, width=700, height=500)

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
    marker=dict(color='blue', line=dict(color='rgba(58, 71, 80, 1.0)', width=1)),
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
    marker=dict(color='Blue', line=dict(color='Black', width=1)),
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
