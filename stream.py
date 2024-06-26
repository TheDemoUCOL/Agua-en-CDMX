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
        z-index: 1000;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header img {
        height: 50px;
    }
    .header .title {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    .nav {
        display: flex;
        gap: 15px;
        color: white;
    }
    .nav a {
        text-decoration: none;
        color: white;
        font-weight: bold;
    }
    .footer {
        width: 900px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        border-top: 2px solid #e9ecef;
        background-color: rgb(14, 17, 23);
        color: #bbbbbb;
        margin-top: 20px;
    }
    .footer div referencias {
        width: 300px;
            
    }
    .footer p {
        margin: 5px 0;
    }
    .footer a {
        color: #bbbbbb;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# HTML personalizado para el encabezado
st.markdown("""
    <div class="header">
        <div class="logo-container">
            <img src="data:image/png;base64,{}" class="logo">        </div>
        <div class="title">Reportes de falta de agua en CDMX</div>
        <div class="nav">
            <a href="#mapa-de-reportes-de-falta-de-agua-en-cdmx">Mapa</a>
            <a href="#d7139f63">Alcaldías</a>
            <a href="#dd0c9ac6">Colonias</a>
            <a href="#53ca301e">Resultados</a>
        </div>
        <div class="logo-container">
            <img src="data:image/png;base64,{}" class="logo">
        </div>
    </div>
""".format(
    base64.b64encode(open("logo_ici.png", "rb").read()).decode(),
    base64.b64encode(open("logo_udc.png", "rb").read()).decode()
), unsafe_allow_html=True)


mapa = """ 
El primer paso para entender este problema es visualizar la distribución de los reportes de falta de agua en la Ciudad de México. Para ello se analizaron los datos proporcionados por el [gobierno mexiquense] sobre todos los reportes recibidos en 2021, estos nos darán una idea de las zonas más afectadas por la falta de agua en la Ciudad de México y concentrar nuestros esfuerzos en esas áreas.

[gobierno mexiquense]: https://datos.cdmx.gob.mx/dataset/reportes-de-agua
"""


description = """ 
La falta de agua en la Ciudad de México es un problema recurrente que afecta a miles de personas cada año. Y no es noticia nueva que esto este sucediendo, a pesar de que solo recientemente ha salido a la luz este dilema. Según datos de [SACMEX] (Sistema de Aguas de la Ciudad de México), en 2021 se registraron más de 10,000 reportes de falta de agua en la Ciudad de México. Nosotros somos Alejandro Paredes, Paola Robles, Rubén Reyna y Rubén Silva un equipo de amigos y compañeros que nos enfocamos en el análisis de datos para poder entender mejor este problema y poder proponer soluciones.

[SACMEX]: https://www.gob.mx/imta/articulos/vulnerabilidad-del-cutzamala?idiom=es
"""

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
El mapa refleja una distribución de los reportes de falta de agua en la Ciudad de México, donde más reportes podemos encontrar es en la alcaldía Coyoacán, seguido de Talpan y Gustavo A. Madero. Vamos a profundizar en los reportes de falta de agua en la alcaldía Coyoacán para entender mejor la situación en esa zona.""")
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
st.caption("Grafica 1: Cantidad de reportes por alcaldia de la ciudad de mexico.")

# Mostrar la gráfica de barras de reportes por colonia
st.markdown('## Reportes de falta de agua por colonia en Coyoacán en 2021')
st.markdown("""
Dentro de la alcaldía Coyoacán, la colonia con más reportes de falta de agua es Pedregal de santo Domingo, es supera por poco menos del doble de reportes a la colonia Ajusco, lo que indica un serio problema en esa colonia. Un dato a tomar en cuenta es que la colonia Pedregal se encuentra justo a un lado de ciudad universitaria, lo que podría indicar que la falta de agua en la colonia es un problema que afecta a la universidad. Vamos a profundizar en los reportes de falta de agua en la colonia Pedregal de Santo Domingo explorando las características de las viviendas en esa colonia.
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
La tabla 1 representa la distribución de los reoprtes de agua que posteriormente podemos ver en la gráfica 3, en la cual podemos observar una caída en los reportes en el mes de julio, justo como indica [Conagua] en su reporte de precipitaciones para el año 2021, Julio fue un mes con bastante precipitación, lo interesante viene después de este mes.

[Conagua]: https://smn.conagua.gob.mx/tools/DATA/Climatolog%C3%ADa/Pron%C3%B3stico%20clim%C3%A1tico/Temperatura%20y%20Lluvia/PREC/2021.pdf 
""")

# Lectura del archivo CSV
df = pd.read_csv('reportes_colonia_fechas.csv')
st.caption("Tabla 1: Reportes de falta de agua por colonia en Coyoacán en 2021.")

# Mostrar la tabla
st.dataframe(df, width=1000, height=500)

####Analisis de temporada ####

# Mostrar la línea de tiempo de reportes
st.markdown('## Línea de tiempo de reportes de falta de agua en CDMX en 2021')
st.markdown("""
La linea de tiempo nuestra esta caída repentina que hubo en el mes de junio y es interesante observar que después de este mes los reportes vuelven a subir, esto podría indicar que los pozos donde se abastece la Ciudad de México no están siendo suficientes para abastecer a la ciudad, lo que podría ser un problema a largo plazo.
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
st.markdown("""La mayoría de la población de la colonia Pedregal tiene preparación para recibir agua entubada, sin embargo, no todos cuentan con un lugar donde almacenar el agua, dependiendo unicamente del abastececimiento de agua entubada. Una solución a este problema podría ser la instalación de tinacos o cisternas para almacenar agua y evitar la falta de agua en la colonia, promover el cuidado de este líquido vital y evitar las fugas por lo menos en lo que respecta a nuestros domicilios, pues el sistema de agua en la Ciudad de México es un problema que se debe atacar desde la raíz, y no solo con soluciones temporales. El sistema [cutzamala] que abastece a la Ciudad de México, es un sistema que se encuentra en peligro de desaparecer, por lo que es importante que se tomen medidas para evitar que esto suceda.
            
[cutzamala]: https://www.gob.mx/imta/articulos/vulnerabilidad-del-cutzamala?idiom=es
            """)


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



################### pie de pagina ####################
# HTML personalizado para el pie de página
# Agregar el pie de página
st.markdown("""
   
   ## Hecho por:
   - Roberto Alejandro Hernandez Paredes
   - Paola Berenice Robles Becerra
   - Rubén Reyna Alonso
   - Rubén Abraham Silva Vazquez
   
   ## Referencias
   - SACMEX. (2024, marzo). Reportes de agua SACMEX. Recuperado 13 de mayo de 2024, de https://datos.cdmx.gob.mx/dataset/groups/reportes-de-agua
   - Gaceta UNAM. (2021, 18 marzo). México experimenta escasez de agua y falta de equidad en su distribución - Gaceta UNAM. https://www.gaceta.unam.mx/mexico-experimenta-escasez-de-agua-y-falta-de-equidad-en-su-distribucion/#:~:text=De%20acuerdo%20con%20datos%20de,los%20d%C3%ADas%20y%2018%20por
   - INEGI (Ed.). (2022, 17 marzo). Viviendas que no disponen de drenaje. Recuperado 10 de mayo de 2024, de https://datos.cdmx.gob.mx/dataset/viviendas-que-no-disponen-de-drenaje
   - Sistema de aguas de la ciudad de México (Ed.). (2023). Sistema de aguas en la Ciudad de México. Agua En Tu Colonia. Recuperado 13 de mayo de 2024, de https://aguaentucolonia.sacmex.cdmx.gob.mx/#/search/1268         
    
""")