import streamlit as st
import base64
import pandas as pd

st.title('Reportes de falta de agua en CDMX')
st.markdown('Este es un tablero interactivo para explorar los reportes de falta de agua en la Ciudad de México en 2021.')

# Mostrar el mapa
st.markdown('## Mapa de reportes de falta de agua en CDMX')
st.markdown('Este mapa muestra los reportes de falta de agua en la Ciudad de México en 2021.')
st.markdown('Puedes seleccionar las capas que deseas visualizar en el mapa.')

# Asegúrate de que la ruta del archivo HTML es correcta
with open('mapa.html', 'r', encoding='utf-8') as f:
    html_data = f.read()
st.components.v1.html(html_data, width=1000, height=500)

#hacer un boton con un icono de interrogacion para mostrar el audio

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
if st.button('?', help='Haz clic para escuchar la explicacion de la falta de agua en la Ciudad de México', key='fixed-button'):
    with open('reporte_voz.mp3', 'rb') as audio_file:
        play_audio(audio_file)

    

# Mostrar la gráfica de barras de reportes por alcaldía
st.markdown('## Reportes de falta de agua por alcaldía en 2021')
st.markdown('Esta gráfica muestra el número de reportes de falta de agua por alcaldía en la Ciudad de México en 2021.')
# Asegúrate de que la ruta de la imagen es correcta
st.image('reportes_por_alcaldia.png', width=1000)

# Mostrar la gráfica de barras de reportes por colonia
st.markdown('## Reportes de falta de agua por colonia en Coyoacán en 2021')
st.markdown('Esta gráfica muestra el número de reportes de falta de agua por colonia en Coyoacán en 2021.')
# Asegúrate de que la ruta de la imagen es correcta
st.image('reportes_por_colonia.png', width=1000)



# Título y descripción
st.markdown('## Reportes de falta de agua por colonia en Coyoacán en 2021')
st.markdown('Esta tabla muestra el número de reportes de falta de agua por colonia en Coyoacán en 2021.')

# Lectura del archivo CSV
df = pd.read_csv('reportes_colonia_fechas.csv')

# Mostrar la tabla
st.dataframe(df, width=10000, height=500)

