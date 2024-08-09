#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import os
import numpy as np
import pandas as pd
from io import BytesIO
import streamlit as st
import geopandas as gpd


from DashFunciones import Totales_Menu, Mapa_Menu, Puestos_Menu
from DashFunciones import Riesgo_Puestos_Menu, Quejas_Denuncias_Riesgos, Cofiabilidad
from DashFunciones import Nivel_Riesgos_Atencion, Queja_Denuncia, Detalle_Aplicativos
from DashFunciones import Tabla_Aplicativos, Accesos_Aplicaticos, Aplicativos_Mayor_Uso
from DashFunciones import Total_Aplicativo, Puestos_Aplicativos, Puestos_Mayor_sistemas
from DashFunciones import Tabla_App_Servicos, Tabla_to_Excel, Info_Denuncias
from DashFunciones import Velo_Denucias, Dona_Clase


from DashContent import Content_Map, Content_Dona, Content_Barras
from DashContent import Content_Barra_Riesgo, Content_Confia_Riesgo
from DashContent import Content_Niveles_Riesgo, Content_Acceso_Info
from DashContent import Content_TotApp_Desonce, Content_TotApp_Puesto
from DashContent import Content_App_Puesto, Content_App_Empleado



import warnings
warnings.filterwarnings("ignore",
                        category = DeprecationWarning)

project_dir = os.path.dirname(os.path.abspath(__file__))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## Definir la ruta de entrada (Ruta de acceso a los archivos de datos)
Entradas = 'C:/Users/LAAR8976/Ladino_ALL/CECTI/DASHBOARD/'

## Ruta al archivo CSS de Bootstrap
bootstrap_css_path = "C:/Users/LAAR8976/Ladino_ALL/CECTI/DASHBOARD/DASH_Vn/.css/bootstrap.min.css"

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Configuración de la página
st.set_page_config(page_title='Análisis de Riesgos', layout='wide')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
# Leer el contenido del archivo CSS
with open(bootstrap_css_path, "r") as f:
    bootstrap_css_content = f.read()

# CSS para aplicar estilos personalizados y la fuente Montserrat
font_css = f"""
<style>
{bootstrap_css_content}

/* Personalización de la fuente Montserrat */
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{project_dir}/.fonts/Montserrat-Regular.ttf') format('truetype');
    font-weight: normal;
}}

@font-face {{
    font-family: 'Montserrat';
    src: url('file://{project_dir}/.fonts/Montserrat-Bold.ttf') format('truetype');
    font-weight: bold;
}}

body {{
    font-family: 'Montserrat', sans-serif !important;
}}

h1, h2, h3, h4, h5, h6, p, div {{
    font-family: 'Montserrat', sans-serif !important;
}}

</style>
"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
st.markdown(font_css, unsafe_allow_html=True)

css_succes = """
<style>
div.stAlert {
    background-color: #006666;
    text-align: center;
}
div.stAlert p {
    color: #FFFFFF;
    font-weight: bold;
}
</style>
"""

# Aplica el CSS
st.markdown(css_succes, unsafe_allow_html=True)

st.markdown("""
        <style>
        .stDownloadButton button {
            background-color: #006666;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Funciones para leer datos y mapa 
@st.cache_data(persist = True)
def read_data(uploaded_file):
    '''Lee los datos del archivo cargado.
    Args:
    archivo_cargado (str): Ruta del archivo cargado por el usuario.
    Returns:
    pandas.DataFrame: El DataFrame con los datos leídos.'''
    BASE_USO = pd.read_pickle(uploaded_file)
    return (BASE_USO)

@st.cache_data(persist = True)
def read_map(uploaded_file):
    '''Lee el mapa del archivo cargado.
    Args:
    archivo_cargado (str): Ruta del archivo cargado por el usuario que
    contiene el mapa.
    Returns:
    geopandas.GeoDataFrame: El GeoDataFrame con el mapa leído.'''
    MAPA_BASE = gpd.read_file(uploaded_file)
    return (MAPA_BASE)

## Lectura de datos y mapa
BASE_USO = read_data(Entradas + "BASEP.pkl")
Spatial = read_map(Entradas + 'UAD_FILE.json')
DENUNCIAS_P = read_data(Entradas + "DENUNCIAS.pkl")

#%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs(["GENERAL", "RIESGOS", "APLICATIVOS", "DENUNCIAS"])

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

with tab1:
    st.success('INFORMACIÓN GENERAL')
    st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    Se presenta de forma general la información al riesgo y los puestos con mas alto riesgo de la Unidad.</p>""", unsafe_allow_html=True)

## Obtener totales (CVE_UNIDAD, TOTAL, SI_R, SI) usando la función Totales_Menu
    CVE_UNIDAD, TOTAL, SI_R, SI = Totales_Menu(BASE_USO)

## Obtener nombre de la unidad
    UNIDAD = SI.iloc[0, 1]

## Crear mapa usando la función Mapa_Menu
    Mapa = Mapa_Menu(CVE_UNIDAD, Spatial)

## Crear gráfico de dona de riesgos usando la función Puestos_Menu
    Dona_Riesgos = Puestos_Menu(BASE_USO)

## Información para el texto del gráfico de dona de riesgos usando la función Puestos_Menu
    DON_VAL = [BASE_USO[BASE_USO['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique(),
               BASE_USO[BASE_USO['PTO_RIESGO'] == 'NO'].PUESTO_NOM.nunique()]


## Crear gráfico de barras de riesgos usando la función Riesgo_Puestos_Menu
    Barras_Riesgo = Riesgo_Puestos_Menu(SI)

## Crear columnas para organizar el layout
    #plot_tab, plot_ries = st.columns(2)
    AP1, AP2 = st.columns([2, 2])

## Mostrar mapa en la columna izquierda
    with AP1:
        st.plotly_chart(Mapa, use_container_width=True)

## Mostrar texto con unidad administrativa en la columna derecha
    with AP2:
        st.plotly_chart(Dona_Riesgos, use_container_width=True)
        #MAPA_CONTENT = Content_Map(CVE_UNIDAD, UNIDAD)
        #st.markdown(MAPA_CONTENT, unsafe_allow_html=True)


## Invertir el orden de las columnas
    BP1, BP2, BP3 = st.columns([1,1,1])

    with BP1:
        MAPA_CONTENT = Content_Map(CVE_UNIDAD, UNIDAD)
        st.markdown(MAPA_CONTENT, unsafe_allow_html=True)        
        #DONA_CONTENT = Content_Dona(DON_VAL)
        #st.markdown(DONA_CONTENT, unsafe_allow_html=True)

## Mostrar gráfico de dona de riesgos en la columna derecha
    with BP2:
        DONA_CONTENT = Content_Dona(DON_VAL)
        st.markdown(DONA_CONTENT, unsafe_allow_html=True)

    with BP3:
        BARRA_CONTENT = Content_Barras(SI)
        st.markdown(BARRA_CONTENT, unsafe_allow_html=True)

## Mostrar gráfico de barras de riesgos en toda la fila
    st.plotly_chart(Barras_Riesgo, use_container_width=True)


with tab2:
    #'''Contenido de la pestaña "Riesgos"
    #Esta sección muestra información sobre los riesgos identificados en el
    #dashboard.
    #Permite filtrar por unidad administrativa, puesto y empleado para obtener
    #resultados más específicos.'''
    
    st.success('RIESGO POR PUESTO EN DESCONCENTRADA')

    st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    Se presenta la información de manera gráfica, destacando los resultados relativos al riesgo por desconcentrada en función de los puestos, 
                    la información sobre quejas y denuncias, y los resultados relacionados con el nivel de confiabilidad.</p>""", unsafe_allow_html=True)
    st.write('Seleccionar y aplicar por:')

## Filtro por unidad administrativa desconcentrada
    l1 = BASE_USO["DESCONCENTRADA"].unique().tolist()
    l2  = []
    l2 = l1[:]
    l2.append('TODAS')
    Deconcentrada_drop = st.multiselect('DESCONCENTRADA', l2, default = 'TODAS')
    if 'TODAS' in Deconcentrada_drop:
        Deconcentrada_drop = l1


## Aplicar filtro de unidad administrativa desconcentrada
    BASE_USO_F1 = BASE_USO.query("DESCONCENTRADA == @Deconcentrada_drop")

## Obtener totales para la unidad administrativa desconcentrada seleccionada
    TOTAL_PUESTOS,TOTAL_PUESTOS_RIESGO,\
        MAYOR_RIESGO, CONFIABILIDAD, NIVEL_RIESGO,QUEJA_DENUNCIA, USUARIOS,\
            USUARIO_CRITICO, USUARIO_ALTOMEDIO = Quejas_Denuncias_Riesgos (BASE_USO_F1)

## Mostrar métricas de totales
    plot_M1, plot_M2 = st.columns(2)
    
    with plot_M1:
        st.metric('Total Puestos', TOTAL_PUESTOS)
    with plot_M2:
        st.metric('Total Puestos Riesgo', TOTAL_PUESTOS_RIESGO)

## Si no hay datos para la selección actual, mostrar un mensaje de advertencia
    if BASE_USO_F1.empty:
        st.warning("NO HAY DATOS DISPONIBLES PARA LA SELECCIÓN ACTUAL.")
    else:
        ## Obtener totales para la unidad administrativa desconcentrada y nivel de riesgo
        UNIDAD_0, TOTAL_0, SI_R_0, SI_0 = Totales_Menu(BASE_USO_F1)

        BR1, BR2 = st.columns([2,1])

        with BR1:
            B_R = Riesgo_Puestos_Menu (SI_0)    
            st.plotly_chart(B_R, use_container_width=True)

        with BR2:
            BARRA_CON_RIESGO = Content_Barra_Riesgo(BASE_USO_F1, TOTAL_PUESTOS, TOTAL_PUESTOS_RIESGO, SI_0)
            st.markdown(BARRA_CON_RIESGO, unsafe_allow_html=True)

## Mostrar gráficos de confiablidad, quejas y denuncias

        st.success('CONFIABILIDAD, QUEJAS-DENUNCIAS Y NIVEL DE RIESGOS ')

        CONFI_QUE_DENU = Content_Confia_Riesgo(CONFIABILIDAD, QUEJA_DENUNCIA)
        st.markdown(CONFI_QUE_DENU, unsafe_allow_html=True) 

        FR1, FR2 = st.columns([1.5,1])
       
        with FR1:
            Confi = Cofiabilidad (CONFIABILIDAD)
            st.plotly_chart(Confi, use_container_width=True)


        with FR2:
            QD = Queja_Denuncia (QUEJA_DENUNCIA)
            st.plotly_chart(QD, use_container_width=True)
          

## Mostrar gráficos de nivel de riesgo

        NR1, NR2 = st.columns([1,2])

        with NR1:
            NIVELES_RIESGOS = Content_Niveles_Riesgo(NIVEL_RIESGO)
            st.markdown(NIVELES_RIESGOS, unsafe_allow_html=True)

        with NR2:
            NRA = Nivel_Riesgos_Atencion (NIVEL_RIESGO)
            st.plotly_chart(NRA, use_container_width=True)

        st.success('DETALLES DE APLICATIVOS POR NIVEL DE RIESGO')

## Filtro por puesto

        st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    La tabla presenta información detallada sobre los empleados, incluyendo los puestos que ocupan, los roles asignados y 
                    los niveles de riesgo y atención asociados a cada puesto, en función de la desconcentrada seleccionada previamente.</p>""", unsafe_allow_html=True)
        st.write('Seleccionar y aplicar por:')

        filtered_base = BASE_USO_F1[~BASE_USO_F1['NIVEL_ATENCION'].isin(['NULO', 'BAJO'])]
        M1 = filtered_base["PUESTO_NOM"].unique().tolist()
        M2 = M1[:]
        M2.append('TODOS')
        Puesto_drop = st.multiselect('PUESTO', M2, default = 'TODOS')
        if 'TODOS' in Puesto_drop:
            Puesto_drop = M1
        else:
            Puesto_drop = [p for p in Puesto_drop if p in M1]

## Aplicar filtro de puesto
        BASE_USO_F2 = filtered_base.query("PUESTO_NOM == @Puesto_drop")
    
        TABLA_DETALLE, SISTEMA_INFORMATICO = Detalle_Aplicativos(BASE_USO_F2)

        Tabla_APP = Tabla_Aplicativos (TABLA_DETALLE)

        st.plotly_chart(Tabla_APP, use_container_width=True)


## Filtro por empleado

        st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    La gráfica muestra a detalle el porcentaje de acceso a las aplicaciones, desglosado por empleado, 
                    en función del puesto y la desconcentrada a la que pertenece seleccionada previamente.</p>""", unsafe_allow_html=True)
        st.write('Seleccionar y aplicar por:')

        E1 = SISTEMA_INFORMATICO["NOMBRE_EMP"].unique().tolist()
        E2 = E1[:]
        E2.append('TODOS')
        Empleado_drop = st.multiselect('EMPLEADO', E2, default = 'TODOS')
        if 'TODOS' in Empleado_drop:
            Empleado_drop = E1
        else:
            Empleado_drop = [q for q in Empleado_drop if q in E1]

## Aplicar filtro de empleado

        BASE_USO_F3 = SISTEMA_INFORMATICO.query("NOMBRE_EMP == @Empleado_drop")

## Obtener accesos a aplicaciones por empleado
        Empleado_App = Accesos_Aplicaticos(BASE_USO_F3)

## Mostrar columnas para el layout
        EM1, EM2 = st.columns([1,2])

## Mostrar texto temporal (BLABLAHAHAH) en la columna izquierda
        with EM1:
            Ladino = Content_Acceso_Info(BASE_USO_F3)
            st.markdown(Ladino, unsafe_allow_html=True)
## Mostrar gráfico de accesos a aplicaciones por empleado en la columna derecha
        with EM2:
            st.plotly_chart(Empleado_App, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

with tab3:
    #'''Contenido de Aplicativos
    #Esta sección muestra información sobre los aplicativos utilizados en el
    #dashboard.
    #Permite filtrar por unidad administrativa, puesto y empleado para obtener
    #resultados más específicos.'''
    
    st.success('RIESGO POR APLICATIVOS - GENERAL')

    st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    Se presenta la información de manera gráfica, destacando los resultados relativos al riesgo por aplicativo en la desconcentrada 
                    de forma general.</p>""", unsafe_allow_html=True)

## Mostrar gráfico de barras de aplicaciones por unidad administrativa
    PR1, PR2 = st.columns([2,1])
    TOT_APP = BASE_USO.groupby('DESCONCENTRADA')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)

    with PR1:
        BAR_APLICA = Total_Aplicativo(TOT_APP)
        st.plotly_chart(BAR_APLICA, use_container_width=True)

    with PR2:
        Cont_Apps = Content_TotApp_Desonce(TOT_APP)
        st.markdown(Cont_Apps, unsafe_allow_html=True)


## Mostrar gráfico de barras de aplicaciones por puesto
    AP_R1, AP_R2 = st.columns([1,2])
    TOT_APP_PUESTO = BASE_USO.groupby('PUESTO_NOM')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)

    with AP_R1:
        PUES_APP = Content_TotApp_Puesto(TOT_APP_PUESTO)
        st.markdown(PUES_APP, unsafe_allow_html=True)
    
    with AP_R2: 
        TOTAL_PUESTOS_APP = Puestos_Aplicativos (TOT_APP_PUESTO)
        st.plotly_chart(TOTAL_PUESTOS_APP, use_container_width=True)

    st.success('RIESGO POR APLICATIVOS - DESCONCENTRADA Y PUESTO')

    st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    Se presenta la información de manera gráfica, destacando los resultados relativos al riesgo por aplicativo en la desconcentrada 
                    en función de la información de puestos y empleados.</p>""", unsafe_allow_html=True)
    st.write('Seleccionar y aplicar por:')

## Filtro por unidad administrativa desconcentrada

    A1 = BASE_USO["DESCONCENTRADA"].unique().tolist()
    A2  = []
    A2 = A1[:]
    A2.append('TODAS')
    Deconc_drop = st.multiselect('DESCONCENTRADA', A2, default = 'TODAS', key='Deconc_drop')
    if 'TODAS' in Deconc_drop:
        Deconc_drop = A1

## Aplicar filtro de unidad administrativa desconcentrada
    
    BASE_USO_F3 = BASE_USO.query("DESCONCENTRADA == @Deconc_drop")

## Si no hay datos para la selección actual, mostrar un mensaje de advertencia
    if BASE_USO_F3.empty:
        st.warning("No hay datos disponibles para la selección actual.")

## Mostrar gráfico de barras de mayor cantidad de sistemas por puesto
    else:

        DP1, DP2 = st.columns([2,1])

        with DP1:
            PUESTO_SISTEMAS = BASE_USO_F3.groupby(['DESCONCENTRADA','PUESTO_NOM'])['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
            SISTEMAS_PUESTO = Puestos_Mayor_sistemas(PUESTO_SISTEMAS)
            st.plotly_chart(SISTEMAS_PUESTO, use_container_width=True)

        with DP2:

            PUESTO_DESCO = Content_App_Puesto(PUESTO_SISTEMAS)
            st.markdown(PUESTO_DESCO, unsafe_allow_html=True) 

## Mostrar gráfico de barras de aplicaciones más utilizadas  
        RWID1, RWID2 = st.columns([1,2])

        APLICATIVOS_USO = BASE_USO_F3.groupby(['DESCONCENTRADA','APLICATIVO'])['EMPLEADO'].\
                  count().reset_index().sort_values(by=['EMPLEADO'], ascending=False).head(10)

        with RWID1:
            PUESTO_APP = Content_App_Empleado(APLICATIVOS_USO)
            st.markdown(PUESTO_APP, unsafe_allow_html=True) 

        with RWID2:
            ROSA = Aplicativos_Mayor_Uso(APLICATIVOS_USO)
            st.plotly_chart(ROSA, use_container_width=True)
            
########################

        st.success('RIESGO POR APLICATIVOS - DESCONCENTRADA, PUESTO y EMPLEADO')

        st.markdown("""<p style="text-align: justify; font-size: 16px; font-style: italic;">
                    La tabla proporciona una descripción detallada de la información referente al empleado, 
                    incluyendo el puesto que ocupa, el aplicativo utilizado, los roles asignados y 
                    el alcance de las funciones que desempeña en cada uno de estos roles.</p>""", unsafe_allow_html=True)
        st.write('Seleccionar y aplicar por:')
        
## Filtro por puesto
        FIL1, FIL2 = st.columns([1,1])

        with FIL1:
            PT1 = BASE_USO_F3["PUESTO_NOM"].unique().tolist()
            PT2 = PT1[:]
            PT2.append('TODOS')
            PUESTO_drop = st.multiselect('PUESTO', PT2, default = 'TODOS', key='PUESTO_drop')
            if 'TODOS' in PUESTO_drop:
                PUESTO_drop = PT1
            else:
                PUESTO_drop = [r for r in PUESTO_drop if r in PT1]

## Aplicar filtro de puesto
        BASE_USO_F4 = BASE_USO_F3.query("PUESTO_NOM == @PUESTO_drop")        


        with FIL2:
            ET1 = BASE_USO_F4["NOMBRE_EMP"].unique().tolist()
            ET2 = ET1[:]
            ET2.append('TODOS')
            EMPLET_drop = st.multiselect('EMPLEADO', ET2, default = 'TODOS', key='EMPLET_drop')
            if 'TODOS' in EMPLET_drop:
                EMPLET_drop = ET1
            else:
                EMPLET_drop = [s for s in EMPLET_drop if s in ET1]

## Aplicar filtro de empleado
        BASE_USO_F5 = BASE_USO_F4.query("NOMBRE_EMP == @EMPLET_drop")
        

## Obtener tabla de aplicaciones y servicios por empleado
        LA_TABLA, export_df = Tabla_App_Servicos(BASE_USO_F5)
## Mostrar gráfico de la tabla de aplicaciones y servicios
        st.plotly_chart(LA_TABLA, use_container_width=True)

        st.download_button(label = "DESCARGAR TABLA",
                           data = Tabla_to_Excel(export_df),
                           file_name = 'Tabla_Empleado_App.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab4:

    DEN1, DEN2 = st.columns([1,1])

    with DEN1:
        min_year = DENUNCIAS_P['Año'].min()
        max_year = DENUNCIAS_P['Año'].max()
        
        year_range = st.slider("AÑO:",
                               min_value = min_year, 
                               max_value = max_year, 
                               value = (min_year, max_year))
                               
        BASE_FILTRADA = DENUNCIAS_P[(DENUNCIAS_P['Año'] >= year_range[0]) & 
                                    (DENUNCIAS_P['Año'] <= year_range[1])]

    with DEN2:
        EDE1 = BASE_FILTRADA["NOMBRE"].unique().tolist()
        EDE2 = EDE1[:]
        EDE2.append('TODOS')
        EMPDEN_drop = st.multiselect('EMPLEADO', EDE2, default = 'TODOS', key='EMPDEN_drop')
        if 'TODOS' in EMPDEN_drop:
            EMPDEN_drop = EDE1
        else:
            EMPDEN_drop = [md for md in EMPDEN_drop if md in EDE1]
        
        DENU_EMPLE = BASE_FILTRADA.query("NOMBRE == @EMPDEN_drop")


    D7, D9, D10 = Info_Denuncias(DENU_EMPLE)

    st.metric('Total de Folios', D7)

    MEN1, MEN2 = st.columns([2,1])

    with MEN1:
        Velocimetro = Velo_Denucias (D10)
        st.plotly_chart(Velocimetro, use_container_width=True)

    with MEN2:
        st.write('Generar contenedor de interpretación')

    NEN1, NEN2 = st.columns([1,2.5])

    with NEN1:
        st.write('Generar contenedor de interpretación')

    with NEN2:
        Clasifica_Dona = Dona_Clase (D9)
        st.plotly_chart(Clasifica_Dona, use_container_width=True)





hide_streamlit_style = """
                      <style>
                      #MainMenu {visibility: hidden;}
                      footer {visibility: hidden;}
                      </style>
                      """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
