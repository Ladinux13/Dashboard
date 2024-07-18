#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd

from DashFunciones import Totales_Menu, Mapa_Menu, Puestos_Menu
from DashFunciones import Riesgo_Puestos_Menu, Quejas_Denuncias_Riesgos, Cofiabilidad
from DashFunciones import Nivel_Riesgos_Atencion, Queja_Denuncia, Detalle_Aplicativos
from DashFunciones import Tabla_Aplicativos, Accesos_Aplicaticos

import warnings
warnings.filterwarnings("ignore",
                        category = DeprecationWarning)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Entradas = 'C:/Users/LAAR8976/Ladino_ALL/CECTI/DASHBOARD/'
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
st.set_page_config(page_title='Análisis de Riesgos',
                   layout='wide')

st.markdown("""<style> span[data-baseweb="tag"] {background-color: rgb(0, 102, 102) !important;}</style>""",
            unsafe_allow_html=True)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
@st.cache_data(persist = True)
def read_data(uploaded_file):
    BASE_USO = pd.read_pickle(uploaded_file)
    return (BASE_USO)

@st.cache_data(persist = True)
def read_map(uploaded_file):
    MAPA_BASE = gpd.read_file(uploaded_file)
    return (MAPA_BASE)

BASE_USO = read_data(Entradas + "BASEP.pkl")
Spatial = read_map(Entradas + 'UAD_FILE.json')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 

tab1, tab2, tab3, tab4 = st.tabs(["Generales", "Riesgos", "Aplicativos", "Denuncias"])

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab1:

    st.write("Contenido General")

    UNIDAD, TOTAL, SI_R, SI = Totales_Menu(BASE_USO)

    Mapa = Mapa_Menu (UNIDAD, Spatial)
    Dona_Riesgos = Puestos_Menu(BASE_USO)
    Barras_Riesgo = Riesgo_Puestos_Menu (SI)
    
    plot_tab, plot_ries = st.columns(2)
    plot_tab.plotly_chart(Mapa,use_container_width=True)
    plot_ries.plotly_chart(Dona_Riesgos, use_container_width=True)

    st.plotly_chart(Barras_Riesgo, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab2:

    st.write("Contenido de Riesgos")

# > Filtro Desconcentrada
    l1 = BASE_USO["DESCONCENTRADA"].unique().tolist()
    l2  = []
    l2 = l1[:]
    l2.append('TODAS')
    Deconcentrada_drop = st.multiselect('DESCONCENTRADA', l2, default = 'TODAS')
    if 'TODAS' in Deconcentrada_drop:
        Deconcentrada_drop = l1


# > Filtro Desconcentrada Aplicado
    BASE_USO_F1 = BASE_USO.query("DESCONCENTRADA == @Deconcentrada_drop")

   # if BASE_USO_F1.empty:
    #    st.warning("No hay datos disponibles para la selección actual.")
    #else:
     #   TOTAL_PUESTOS,TOTAL_PUESTOS_RIESGO,\
      #  MAYOR_RIESGO, CONFIABILIDAD, NIVEL_RIESGO,QUEJA_DENUNCIA, USUARIOS,\
       #     USUARIO_CRITICO, USUARIO_ALTOMEDIO = Quejas_Denuncias_Riesgos (BASE_USO_F1)



    TOTAL_PUESTOS,TOTAL_PUESTOS_RIESGO,\
        MAYOR_RIESGO, CONFIABILIDAD, NIVEL_RIESGO,QUEJA_DENUNCIA, USUARIOS,\
            USUARIO_CRITICO, USUARIO_ALTOMEDIO = Quejas_Denuncias_Riesgos (BASE_USO_F1)


    plot_M1, plot_M2 = st.columns(2)
    with plot_M1:
        st.metric('Total Puestos', TOTAL_PUESTOS)
    with plot_M2:
        st.metric('Total Puestos Riesgo', TOTAL_PUESTOS_RIESGO)


    if BASE_USO_F1.empty:
        st.warning("No hay datos disponibles para la selección actual.")
    else:
        UNIDAD_0, TOTAL_0, SI_R_0, SI_0 = Totales_Menu(BASE_USO_F1)

    #UNIDAD_0, TOTAL_0, SI_R_0, SI_0 = Totales_Menu(BASE_USO_F1)
        B_R = Riesgo_Puestos_Menu (SI_0)    
        st.plotly_chart(B_R, use_container_width=True)

        P_M1, P_M2, P_M3 = st.columns(3)
        with P_M1:
            Confi = Cofiabilidad (CONFIABILIDAD)
            st.plotly_chart(Confi, use_container_width=True)
        with P_M2:
            NRA = Nivel_Riesgos_Atencion (NIVEL_RIESGO)
            st.plotly_chart(NRA, use_container_width=True)
        with P_M3:
            QD = Queja_Denuncia (QUEJA_DENUNCIA)
            st.plotly_chart(QD, use_container_width=True)  

# > Filtro Puesto
        filtered_base = BASE_USO_F1[~BASE_USO_F1['NIVEL_ATENCION'].isin(['NULO', 'BAJO'])]
        M1 = filtered_base["PUESTO_NOM"].unique().tolist()
        M2 = M1[:]
        M2.append('TODOS')
        Puesto_drop = st.multiselect('PUESTO', M2, default = 'TODOS')
        if 'TODOS' in Puesto_drop:
            Puesto_drop = M1
        else:
            Puesto_drop = [p for p in Puesto_drop if p in M1]

# > Filtro Puesto Aplicado
        BASE_USO_F2 = filtered_base.query("PUESTO_NOM == @Puesto_drop")
    
        TABLA_DETALLE, SISTEMA_INFORMATICO = Detalle_Aplicativos(BASE_USO_F2)

        Tabla_APP = Tabla_Aplicativos (TABLA_DETALLE)

        st.plotly_chart(Tabla_APP, use_container_width=True)

# > Filtro Empleado
        E1 = SISTEMA_INFORMATICO["NOMBRE_EMP"].unique().tolist()
        E2 = E1[:]
        E2.append('TODOS')
        Empleado_drop = st.multiselect('EMPLEADO', E2, default = 'TODOS')
        if 'TODOS' in Empleado_drop:
            Empleado_drop = E1
        else:
            Empleado_drop = [q for q in Empleado_drop if q in E1]

# > Filtro Empleado Aplicado

        BASE_USO_F3 = SISTEMA_INFORMATICO.query("NOMBRE_EMP == @Empleado_drop")

        Empleado_App = Accesos_Aplicaticos(BASE_USO_F3)

        st.plotly_chart(Empleado_App, use_container_width=True)
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab3:

    st.write("Contenido de Aplicativos")

    TOT_APP = BASE_USO.groupby('DESCONCENTRADA')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
    BAR_APLICA = Total_Aplicativo(TOT_APP)
    st.plotly_chart(BAR_APLICA, use_container_width=True)

    TOT_APP_PUESTO = BASE_USO.groupby('PUESTO_NOM')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
    TOTAL_PUESTOS_APP = Puestos_Aplicativos (TOT_APP_PUESTO)
    st.plotly_chart(TOTAL_PUESTOS_APP, use_container_width=True)

# > Filtro Empleado Aplicado

    A1 = BASE_USO["DESCONCENTRADA"].unique().tolist()
    A2  = []
    A2 = l1[:]
    A2.append('TODAS')
    Deconc_drop = st.multiselect('DESCONCENTRADA', A2, default = 'TODAS', key='Deconc_drop')
    if 'TODAS' in Deconc_drop:
        Deconc_drop = A1

# > Filtro Puesto Aplicado
    
    BASE_USO_F3 = BASE_USO.query("DESCONCENTRADA == @Deconc_drop")

    if BASE_USO_F3.empty:
        st.warning("No hay datos disponibles para la selección actual.")
    else:
        PUESTO_SISTEMAS = BASE_USO_F3.groupby('PUESTO_NOM')['APLICATIVO'].nunique().reset_index().sort_values(by=['APLICATIVO'], ascending=False)
        SISTEMAS_PUESTO = Puestos_Mayor_sistemas(PUESTO_SISTEMAS)
        st.plotly_chart(SISTEMAS_PUESTO, use_container_width=True)
        
        APLICATIVOS_USO = BASE_USO_F3.groupby('APLICATIVO')['EMPLEADO'].\
                  count().reset_index().sort_values(by=['EMPLEADO'], ascending=False).head(10)
        ROSA = Aplicativos_Mayor_Uso(APLICATIVOS_USO)
        st.plotly_chart(ROSA, use_container_width=True)

        # > Filtro Puesto Nombre
        PT1 = BASE_USO_F3["PUESTO_NOM"].unique().tolist()
        PT2 = PT1[:]
        PT2.append('TODOS')
        PUESTO_drop = st.multiselect('PUESTO', PT2, default = 'TODOS', key='PUESTO_drop')
        if 'TODOS' in PUESTO_drop:
            PUESTO_drop = PT1
        else:
            PUESTO_drop = [r for r in PUESTO_drop if r in PT1]

        BASE_USO_F4 = BASE_USO_F3.query("PUESTO_NOM == @PUESTO_drop")

        # > Filtro Puesto Nombre - Empleado
        ET1 = BASE_USO_F4["NOMBRE_EMP"].unique().tolist()
        ET2 = ET1[:]
        ET2.append('TODOS')
        EMPLET_drop = st.multiselect('EMPLEADO', ET2, default = 'TODOS', key='EMPLET_drop')
        if 'TODOS' in EMPLET_drop:
            EMPLET_drop = ET1
        else:
            EMPLET_drop = [s for s in EMPLET_drop if s in ET1]

        BASE_USO_F5 = BASE_USO_F4.query("NOMBRE_EMP == @EMPLET_drop")
        TABLA_APPS =  Tabla_App_Servicos(BASE_USO_F5)
        st.plotly_chart(TABLA_APPS, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
with tab4:
    st.write("Contenido de Denuncias")
