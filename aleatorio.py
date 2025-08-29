from narwhals import col
import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import base64
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Programa Saludablemente - Sorteo de Alianzas",
    page_icon="👥",
    layout="wide"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .stButton>button {
        background-color: #FFD700;
        color: #003366;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #ffcc00;
        transform: scale(1.05);
        transition: all 0.3s;
    }
    .header {
        text-align: center;
        padding: 1rem;
        background-color: #FFD700;
        border-bottom: 5px solid #007BFF;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #007BFF;
        margin: 1rem 0;
    }
    .alliance-card {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .alliance-green {
        border: 2px solid #28a745;
        background-color: #f8fff8;
    }
    .alliance-blue {
        border: 2px solid #007BFF;
        background-color: #f8f8ff;
    }
    .count-box {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título y logo
st.markdown("""
    <div class="header">
        <h1>👥 Programa Saludablemente</h1>
        <p>Fortaleciendo la integración, participación y bienestar de nuestros funcionarios</p>
    </div>
""", unsafe_allow_html=True)

# Carga del logo (el usuario puede subirlo)
st.sidebar.header("")
logo = "NUEVO LOGO.png"
if logo:
    image = Image.open(logo)
    st.sidebar.image(image, width=150)
else:
    st.sidebar.info("Por favor, sube el logo de la institución")

# Explicación del programa
st.markdown("""
    <div class="info-box">
        <h4>🎯 Bienvenido al Sorteo de Alianzas</h4>
        <p>Carga tu archivo Excel con los funcionarios y realiza un sorteo aleatorio.</p>
    </div>
""", unsafe_allow_html=True)

# Carga del archivo Excel
uploaded_file = st.file_uploader("📁 Cargar archivo excel con los funcionarios", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file)
        
        # Validar columnas requeridas
        required_columns = ['NOMBRE_COMPLETO', 'GENERO']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ El archivo debe contener las columnas: {', '.join(required_columns)}")
            st.stop()
            
        # Validar valores de género
        valid_genders = ['HOMBRE', 'MUJER']
        if not all(g in valid_genders for g in df['GENERO'].unique()):
            st.warning(f"Se encontraron valores inesperados en la columna 'Género'. Asegúrate de que solo contenga: {', '.join(valid_genders)}")
        
        # Limpiar datos
        df = df.dropna(subset=['NOMBRE_COMPLETO', 'GENERO'])
        df = df[df['GENERO'].isin(valid_genders)]
        
        st.success(f"✅ {len(df)} funcionarios cargados correctamente.")
        
        # Mostrar vista previa
        with st.expander("👁️ Vista previa de los datos"):
            st.dataframe(df, use_container_width=True)
        
        # Verificación de conteos
        hombres = df[df['GENERO'] == 'HOMBRE']
        mujeres = df[df['GENERO'] == 'MUJER']
        
        if len(hombres) < 54 or len(mujeres) < 103:
            st.error(f"""
            ❌ No hay suficientes participantes:
            - Hombres necesarios: 54 (disponibles: {len(hombres)})
            - Mujeres necesarias: 103 (disponibles: {len(mujeres)})
            """)
            st.stop()
        
        # Botones de acción
        btn = st.button("🎯 Realizar Sorteo")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if btn:
                # Mostrar animación de tómbola
                st.markdown("### 🎉 Sorteo realizado")
                
                # Carga del GIF de tómbola (el usuario puede subirlo)
                tombola_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGU2c2FhNHQxdzFuMGdyajIycWFxdW9uc2FoeGN2b2ZhYnIwZzJqeiZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/ivLRjWgb6VO17B4EC4/giphy.gif"
                
                if tombola_gif:
                    st.image(tombola_gif, use_container_width=True)
                else:
                    # GIF de ejemplo
                    st.markdown("""
                    <div style="text-align: center;">
                        <img src="https://media.giphy.com/media/3o7TKqn2NeTr7KXDTm/giphy.gif" 
                             style="border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2);" width="300">
                    </div>
                    """, unsafe_allow_html=True)
                
                # Simular tiempo de procesamiento
                import time
                with st.spinner("Asignando funcionarios a las alianzas..."):
                    time.sleep(2)
                
                # Realizar el sorteo
                # Mezclar aleatoriamente
                hombres_sample = hombres.sample(frac=1, random_state=random.randint(1, 1000)).reset_index(drop=True)
                mujeres_sample = mujeres.sample(frac=1, random_state=random.randint(1, 1000)).reset_index(drop=True)
                
                # Asignar equipos
                alianza_verde_hombres = hombres_sample.iloc[:27]
                alianza_azul_hombres = hombres_sample.iloc[27:54]
                alianza_verde_mujeres = mujeres_sample.iloc[:51]
                alianza_azul_mujeres = mujeres_sample.iloc[51:103]
                
                # Crear DataFrames de alianzas
                alianza_verde = pd.concat([alianza_verde_hombres, alianza_verde_mujeres]).reset_index(drop=True)
                alianza_verde['Alianza'] = 'Verde'
                
                alianza_azul = pd.concat([alianza_azul_hombres, alianza_azul_mujeres]).reset_index(drop=True)
                alianza_azul['Alianza'] = 'Azul'
                
                # Combinar resultados
                resultados = pd.concat([alianza_verde, alianza_azul]).reset_index(drop=True)
                
                # Guardar en sesión
                st.session_state.resultados = resultados
                st.session_state.alianza_verde = alianza_verde
                st.session_state.alianza_azul = alianza_azul
                st.session_state.df_original = df
        
        # Mostrar resultados si existen
        if 'resultados' in st.session_state:
            resultados = st.session_state.resultados
            alianza_verde = st.session_state.alianza_verde
            alianza_azul = st.session_state.alianza_azul
            
            # Métricas generales
            st.markdown("## 📊 Resultados del Sorteo")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class="count-box">
                    <h3>👥</h3>
                    <p><strong>Total Procesados</strong></p>
                    <h2>{}</h2>
                </div>
                """.format(len(st.session_state.df_original)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="count-box">
                    <h3>👨</h3>
                    <p><strong>Hombres</strong></p>
                    <h2>{}</h2>
                </div>
                """.format(len(hombres)), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="count-box">
                    <h3>👩</h3>
                    <p><strong>Mujeres</strong></p>
                    <h2>{}</h2>
                </div>
                """.format(len(mujeres)), unsafe_allow_html=True)
            
            # Mostrar alianzas
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="alliance-card alliance-green">
                    <h3>🟩 Alianza Verde</h3>
                    <p><strong>Composición:</strong> 27 Hombres + 51 Mujeres = {} integrantes</p>
                </div>
                """.format(len(alianza_verde)), unsafe_allow_html=True)
                
                # Mostrar lista
                for idx, row in alianza_verde.iterrows():
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.2rem 0; border-left: 4px solid #28a745; background-color: #f0f8f0; border-radius: 5px;">
                        {row['NOMBRE_COMPLETO']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="alliance-card alliance-blue">
                    <h3>🔵 Alianza Azul</h3>
                    <p><strong>Composición:</strong> 27 Hombres + 52 Mujeres = {} integrantes</p>
                </div>
                """.format(len(alianza_azul)), unsafe_allow_html=True)
                
                # Mostrar lista
                for idx, row in alianza_azul.iterrows():
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.2rem 0; border-left: 4px solid #007BFF; background-color: #f0f0ff; border-radius: 5px;">
                        {row['NOMBRE_COMPLETO']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Gráficos
            st.markdown("## 📈 Distribución de Alianzas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de barras por género y alianza
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Hombres',
                    x=['Verde', 'Azul'],
                    y=[len(alianza_verde[alianza_verde['GENERO'] == 'HOMBRE']), 
                       len(alianza_azul[alianza_azul['GENERO'] == 'HOMBRE'])],
                    marker_color='#28a745'
                ))
                
                fig.add_trace(go.Bar(
                    name='Mujeres',
                    x=['Verde', 'Azul'],
                    y=[len(alianza_verde[alianza_verde['GENERO'] == 'MUJER']), 
                       len(alianza_azul[alianza_azul['GENERO'] == 'MUJER'])],
                    marker_color='#007BFF'
                ))
                
                fig.update_layout(
                    title="Distribución por GENERO y Alianza",
                    xaxis_title="Alianza",
                    yaxis_title="Cantidad de Funcionarios",
                    barmode='group',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de torta por alianza
                fig2 = go.Figure(data=[go.Pie(
                    labels=['Alianza Verde', 'Alianza Azul'],
                    values=[len(alianza_verde), len(alianza_azul)],
                    marker_colors=['#28a745', '#007BFF'],
                    textinfo='label+percent',
                    insidetextorientation='radial'
                )])
                
                fig2.update_layout(
                    title="Distribución por Alianza",
                    height=400
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Botones de descarga y reinicio
            col1, col2 = st.columns([1,1])
            
            with col1:
                # Preparar archivo para descarga
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    resultados = resultados[['NOMBRE_COMPLETO', 'Alianza']]
                    resultados.to_excel(writer, sheet_name='Resultados', index=False)
                    df.to_excel(writer, sheet_name='Original', index=False)
                
                st.download_button(
                    label="📥 Descargar Resultados en Excel",
                    data=output.getvalue(),
                    file_name="resultados_sorteo_alianzas.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                if st.button("🔄 Reiniciar Sorteo"):
                    # Limpiar resultados y volver a mezclar
                    del st.session_state.resultados
                    del st.session_state.alianza_verde
                    del st.session_state.alianza_azul
                    st.rerun()
            
            
            
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

else:
    st.info("""
    🔽 Por favor, carga un archivo Excel con las siguientes columnas:
    - **Nombre completo**
    - **Género** (con valores 'Hombre' o 'Mujer')
    
    El sistema dividirá automáticamente a los funcionarios en dos alianzas:
    - **Alianza Verde**: 27 hombres + 51 mujeres
    - **Alianza Azul**: 27 hombres + 52 mujeres
    """)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #666; font-size: 0.9em;">
        <hr>
        © Programa Saludablemente | Fomentando la integración y el bienestar laboral
    </div>
            
""", unsafe_allow_html=True)
sb1,sb2,sb3 = st.columns(3)
with sb2:
    with st.container():
                st.markdown("""
                    <div style='text-align: center; color: #888888; font-size: 15px; padding-bottom: 20px;'>
                        💼 Aplicación desarrollada por <strong>AAS</strong> <br>
                        🌐 Más información en: <a href="https://alain-antinao-s.notion.site/Alain-C-sar-Antinao-Sep-lveda-1d20a081d9a980ca9d43e283a278053e" target="_blank" style="color: #4A90E2;">Mi página personal</a>
                    </div>
                """, unsafe_allow_html=True)