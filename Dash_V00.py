#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import os
import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd

from DashFunciones import Totales_Menu, Mapa_Menu, Puestos_Menu
from DashFunciones import Riesgo_Puestos_Menu, Quejas_Denuncias_Riesgos, Cofiabilidad
from DashFunciones import Nivel_Riesgos_Atencion, Queja_Denuncia, Detalle_Aplicativos
from DashFunciones import Tabla_Aplicativos, Accesos_Aplicaticos, Aplicativos_Mayor_Uso
from DashFunciones import Total_Aplicativo, Puestos_Aplicativos, Puestos_Mayor_sistemas
from DashFunciones import Tabla_App_Servicos


from DashContent import Content_Map, Content_Dona, Content_Barras
from DashContent import Content_Barra_Riesgo



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



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs(["GENERAL", "RIESGOS", "APLICATIVOS", "DENUNCIAS"])

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

with tab1:
    #'''Contenido de la pestaña "Generales"
    #Esta sección muestra información general del dashboard.'''

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
    AP1, AP2 = st.columns([2, 1])

## Mostrar mapa en la columna izquierda
    with AP1:
        st.plotly_chart(Mapa, use_container_width=True)

## Mostrar texto con unidad administrativa en la columna derecha
    with AP2:
        MAPA_CONTENT = Content_Map(CVE_UNIDAD, UNIDAD)
        st.markdown(MAPA_CONTENT, unsafe_allow_html=True)


## Invertir el orden de las columnas
    BP1, BP2 = st.columns([1, 2])
    plot_ries, plot_tab = st.columns(2)

## Mostrar texto temporal (BLABLAHHH) en la columna izquierda
    with BP1:
        DONA_CONTENT = Content_Dona(DON_VAL)
        st.markdown(DONA_CONTENT, unsafe_allow_html=True)

## Mostrar gráfico de dona de riesgos en la columna derecha
    with BP2:
        st.plotly_chart(Dona_Riesgos, use_container_width=True)

## Mostrar texto temporal (BLABLAHHH) debajo del gráfico
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
    
    #st.write("Contenido de Riesgos")

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

## Mostrar gráficos y texto temporal (BLABLAHHH)

        FR1, FR2 = st.columns([1,1])
       
        with FR1:
            Confi = Cofiabilidad (CONFIABILIDAD)
            st.plotly_chart(Confi, use_container_width=True)


        with FR2:
            QD = Queja_Denuncia (QUEJA_DENUNCIA)
            st.plotly_chart(QD, use_container_width=True)       

        st002, P_M2 = st.columns(2)

        with P_M2:
            NRA = Nivel_Riesgos_Atencion (NIVEL_RIESGO)
            st.plotly_chart(NRA, use_container_width=True)
            st002.write('BLABLAHHH  ')

        P_M3, st0002 = st.columns(2)

        with P_M3:
            QD = Queja_Denuncia (QUEJA_DENUNCIA)
            st.plotly_chart(QD, use_container_width=True)
            st0002.write('BLABLAHHH  ')

## Filtro por puesto
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
        st.write('BLABLAAHAH')
## Filtro por empleado
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
        st021, st21 = st.columns(2)

## Mostrar texto temporal (BLABLAHAHAH) en la columna izquierda
        st021.write('BLABLAHAHAH')
## Mostrar gráfico de accesos a aplicaciones por empleado en la columna derecha
        st21.plotly_chart(Empleado_App, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

with tab3:
    '''Contenido de Aplicativos
    Esta sección muestra información sobre los aplicativos utilizados en el
    dashboard.
    Permite filtrar por unidad administrativa, puesto y empleado para obtener
    resultados más específicos.'''
    
    st.write("Contenido de Aplicativos")

## Mostrar gráfico de barras de aplicaciones por unidad administrativa
    st31, st03 = st.columns(2)
    
    TOT_APP = BASE_USO.groupby('DESCONCENTRADA')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
    BAR_APLICA = Total_Aplicativo(TOT_APP)
    st31.plotly_chart(BAR_APLICA, use_container_width=True)
    st03.write('BLABLAHAHAH')

## Mostrar gráfico de barras de aplicaciones por puesto
    st003, st32 = st.columns(2)
    
    TOT_APP_PUESTO = BASE_USO.groupby('PUESTO_NOM')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
    TOTAL_PUESTOS_APP = Puestos_Aplicativos (TOT_APP_PUESTO)
    st003.write('BLABLAHAHAH')
    st32.plotly_chart(TOTAL_PUESTOS_APP, use_container_width=True)
           
## Filtro por unidad administrativa desconcentrada

    A1 = BASE_USO["DESCONCENTRADA"].unique().tolist()
    A2  = []
    A2 = l1[:]
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
        st33, st0003 = st.columns(2) 
        
        PUESTO_SISTEMAS = BASE_USO_F3.groupby('PUESTO_NOM')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
        SISTEMAS_PUESTO = Puestos_Mayor_sistemas(PUESTO_SISTEMAS)
        st33.plotly_chart(SISTEMAS_PUESTO, use_container_width=True)
        st0003.write('BLABLAHAHAH')   

        st00003, st34 = st.columns(2)
        
## Mostrar gráfico de barras de aplicaciones más utilizadas        
        APLICATIVOS_USO = BASE_USO_F3.groupby('APLICATIVO')['EMPLEADO'].\
                  count().reset_index().sort_values(by=['EMPLEADO'], ascending=False).head(10)
        ROSA = Aplicativos_Mayor_Uso(APLICATIVOS_USO)
        st00003.write('BLABLAHAHAH')
        st34.plotly_chart(ROSA, use_container_width=True)

        #PT1, ET1 = st.columns(2)   
        
## Filtro por puesto
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

## Filtro por empleado
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
        TABLA_APPS =  Tabla_App_Servicos(BASE_USO_F5)
## Mostrar gráfico de la tabla de aplicaciones y servicios
        st.plotly_chart(TABLA_APPS, use_container_width=True)

## Texto temporal (se puede reemplazar con información relevante)
        st.write('BLABLAHHH  ')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab4:
    st.write("Contenido de Denuncias")


hide_streamlit_style = """
                      <style>
                      #MainMenu {visibility: hidden;}
                      footer {visibility: hidden;}
                      </style>
                      """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)