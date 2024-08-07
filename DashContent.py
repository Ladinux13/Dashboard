##### Funciones Dashboard-Contenedores SAT-CECTI-2024
#### Elaboro: Ladino Álvarez Ricardo Arturo


#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import os
import pandas as pd
import streamlit as st

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor Mapa Menu
def Content_Map(CVE_UNIDAD, UNIDAD):
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>INFORMACIÓN GENERAL</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">Unidad Administrativa <br><b>{UNIDAD}</b></br> </p>
                        <p class="card-text" style="text-align: justify; font-size: 13px;">Clave <br><b>{CVE_UNIDAD}</b></br> </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor Dona Menu
def Content_Dona(DON_VAL):
    P_RS = ((DON_VAL[0])*(100)) / (DON_VAL[0] + DON_VAL[1])
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>RIESGO GENERAL</b></h6>
                        <p class="card-text" style="text-align: justify; font-size: 13px;">La Unidad tiene contabilizados un total de <b>{DON_VAL[0]}</b> 
                        puestos de riesgo, los cuales representan el <b>{P_RS} %</b> del total de puestos de la unidad.</p>                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor Barras Menu
def Content_Barras(SI):
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>PUESTOS CON MAYOR RIESGO</b></h6>
                        <p class="card-text" style="text-align: justify;font-size: 13px;"> Para la unidad el puesto con mayor riesgo corresponde a <b>{SI.iloc[0, 2]}</b> 
                        con un total de <b>{SI.iloc[0, 3]}</b> empleados en función. </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor Barras Riesgo
def Content_Barra_Riesgo(BASE_USO_F1, TOTAL_PUESTOS, TOTAL_PUESTOS_RIESGO, SI_0):
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>RIESGO POR PUESTO EN DESCONCENTRADA</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;"> La <b>{BASE_USO_F1.iloc[0,12]}</b> perteneciente a la unidad <b>{BASE_USO_F1.iloc[0,1]}</b> cuenta con un
                        total de <b>{TOTAL_PUESTOS}</b> puestos, de los cuales <b>{TOTAL_PUESTOS_RIESGO}</b> son de alto riego. El mayor puesto con riesgo corresponde a <b>{SI_0.iloc[0,2]}</b> 
                        con un total de <b>{SI_0.iloc[0,3]}</b> empleados asignados al puesto.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor confiabilidad - Quejas y Denuncias
def Content_Confia_Riesgo(CONFIABILIDAD, QUEJA_DENUNCIA):
    CONFIABILIDAD_S = CONFIABILIDAD.EMPLEADO.sum()
    QUEJA_DENUNCIA_S = QUEJA_DENUNCIA.EMPLEADO.sum()
    NO_APRO = CONFIABILIDAD[CONFIABILIDAD['PREVE_OBS'] == 'NO APROBADO']
    APR_SEG = CONFIABILIDAD[CONFIABILIDAD['PREVE_OBS'] == 'APROBADO CON SEGUIMIENTO']
    Q_DEN = QUEJA_DENUNCIA[QUEJA_DENUNCIA['ESTATUS'] == 'IMPROCEDENTE']

    # Verificar si los DataFrames están vacíos y asigna 0 si es necesario
    NO_APRO_value = NO_APRO.iloc[0, 1] if not NO_APRO.empty else 0
    APR_SEG_value = APR_SEG.iloc[0, 1] if not APR_SEG.empty else 0
    Q_DEN_value = Q_DEN.iloc[0, 1] if not Q_DEN.empty else 0

    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>CONFIABILIDAD, QUEJAS Y DENUNCIAS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;"> La Unidad Administrativa cuenta con un total de <b>{CONFIABILIDAD_S}</b> empleados, de los cuales <b>{NO_APRO_value}</b> 
                        son estado <b>NO APROBADO</b>  y <b>{APR_SEG_value}</b> son <b>APROBADO CON SEGUIMIENTO</b>. En término de quejas y denuncias, la unidad cuenta con un total de <b>{Q_DEN_value}</b> en estado <b>IMPROCEDENTE</b>. </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return (html_content)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
# Contenedor Nivel de Riesgo

def Content_Niveles_Riesgo(NIVEL_RIESGO):
    R_CRITICO = NIVEL_RIESGO[NIVEL_RIESGO['NIVEL_ATENCION'] == 'CRITICO']
    R_ALTO = NIVEL_RIESGO[NIVEL_RIESGO['NIVEL_ATENCION'] == 'ALTO']
    R_MEDIO = NIVEL_RIESGO[NIVEL_RIESGO['NIVEL_ATENCION'] == 'MEDIO']
    
    # Verificar si los DataFrames están vacíos y asigna 0 si es necesario
    critico_value = R_CRITICO.iloc[0, 1] if not R_CRITICO.empty else 0
    alto_value = R_ALTO.iloc[0, 1] if not R_ALTO.empty else 0
    medio_value = R_MEDIO.iloc[0, 1] if not R_MEDIO.empty else 0
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>NIVELES DE RIESGOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            La Unidad cuenta con un total de <b>{critico_value}</b> empleados en nivel de atención <b>CRÍTICO</b>, 
                            <b>{alto_value}</b> empleados en nivel de atención <b>ALTO</b> y <b>{medio_value}</b> en nivel de atención <b>MEDIO</b>.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
##
# Contenedor Acceso a la información

def Content_Acceso_Info(BASE_USO_F3):

    if len(BASE_USO_F3) > 0:
        EMPLEADO = BASE_USO_F3.iloc[0, 0] if not pd.isna(BASE_USO_F3.iloc[0, 0]) else 0
        APLICATIVO = BASE_USO_F3.iloc[0, 1] if not pd.isna(BASE_USO_F3.iloc[0, 1]) else 0
        ROLES = BASE_USO_F3.iloc[0, 2] if not pd.isna(BASE_USO_F3.iloc[0, 2]) else 0
    else:
        EMPLEADO = 0
        APLICATIVO = 0
        ROLES = 0

    ROL_APP = BASE_USO_F3.ROL_APP.sum() if not BASE_USO_F3.empty else 0
    PER_APP = round((ROLES * 100) / ROL_APP, 2) if ROL_APP != 0 else 0
    TOTL_APP = BASE_USO_F3.APLICATIVO.count() if not BASE_USO_F3.empty else 0
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>ACCESO A SISTEMAS INFORMÁTICOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El empleado <b>{EMPLEADO}</b> cuenta con un total de <b>{ROL_APP}</b> roles distintos distribuidos en <b>{TOTL_APP}</b> aplicativos. 
                            El aplicativo con mayor importancia (<b>{PER_APP}%</b>) corresponde a <b>{APLICATIVO}</b> con <b>{ROLES}</b> roles distintos.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor total de aplicativos por desconcentrada

def Content_TotApp_Desonce(TOT_APP):

    DESCO = TOT_APP.iloc[0, 0]
    DES_T = TOT_APP.iloc[0, 1]
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>TOTAL DE APLICATIVOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El mayor riesgo por aplicativos se identifica en la Desconcentrada de <b>{DESCO}</b>, con un total de <b>{DES_T}</b> aplicativos distintos en uso por sus empleados.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor total de aplicativos por desconcentrada
def Content_TotApp_Puesto(TOT_APP_PUESTO):

    SUM_P = TOT_APP_PUESTO.APLICATIVO.sum()
    PSTR1 = TOT_APP_PUESTO.iloc[0, 0]
    FRS1 = TOT_APP_PUESTO.iloc[0, 1]
    PRS1 = round(((FRS1)*100)/(SUM_P),2)
    PSTR2 = TOT_APP_PUESTO.iloc[1, 0]
    FRS2 = TOT_APP_PUESTO.iloc[1, 1]
    PRS2 = round(((FRS2 )*100)/(SUM_P),2)
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>TOTAL DE APLICATIVOS POR PUESTOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El puesto <b>{PSTR1}</b> presenta el mayor riesgo al tener <b>{FRS1} ({PRS1}%)</b> aplicativos distintos en uso por los empleados. 
                            El puesto con segundo riesgo corresponde a <b>{PSTR2}</b> con <b>{FRS2} ({PRS2}%)</b> aplicativos distintos.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor total de aplicativos por puesto
def Content_App_Puesto(PUESTO_SISTEMAS):

    DESCN = PUESTO_SISTEMAS.iloc[0,0] if not pd.isna(PUESTO_SISTEMAS.iloc[0,0]) else 0
    PSTO1 = PUESTO_SISTEMAS.iloc[0,1] if not pd.isna(PUESTO_SISTEMAS.iloc[0,1]) else 0
    VLTO1 = PUESTO_SISTEMAS.iloc[0,2] if not pd.isna(PUESTO_SISTEMAS.iloc[0,2]) else 0
    PSTO2 = PUESTO_SISTEMAS.iloc[1,1] if len(PUESTO_SISTEMAS) > 1 and not pd.isna(PUESTO_SISTEMAS.iloc[1,1]) else 0
    VLTO2 = PUESTO_SISTEMAS.iloc[1,2] if len(PUESTO_SISTEMAS) > 1 and not pd.isna(PUESTO_SISTEMAS.iloc[1,2]) else 0
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>APLICATIVOS POR DESCONCETRADA Y PUESTO</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El puesto <b>{PSTO1}</b> en la Desconcentrada de <b>{DESCN}</b> se considera de mayor riesgo, con un total de <b>{VLTO1}</b> aplicativos distintos en uso por parte de sus empleados.
                            El segundo puesto con mayor riesgo en la Desconcentrada corresponde a <b>{PSTO2}</b>, con <b>{VLTO2}</b> aplicativos en uso.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## 
# Contenedor Empleados por aplicativo en puesto
def Content_App_Empleado(APLICATIVOS_USO):

    DESCN = APLICATIVOS_USO.iloc[0,0] if not pd.isna(APLICATIVOS_USO.iloc[0,0]) else 0
    PSTO1 = APLICATIVOS_USO.iloc[0,1] if not pd.isna(APLICATIVOS_USO.iloc[0,1]) else 0
    VLTO1 = APLICATIVOS_USO.iloc[0,2] if not pd.isna(APLICATIVOS_USO.iloc[0,2]) else 0

    PSTO2 = APLICATIVOS_USO.iloc[1,1] if len(APLICATIVOS_USO) > 1 and not pd.isna(APLICATIVOS_USO.iloc[1,1]) else 0
    VLTO2 = APLICATIVOS_USO.iloc[1,2] if len(APLICATIVOS_USO) > 1 and not pd.isna(APLICATIVOS_USO.iloc[1,2]) else 0
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>APLICATIVOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El aplicativo <b>{PSTO1}</b> en la Desconcentrada de <b>{DESCN}</b> se considera de mayor riesgo, con un total de <b>{VLTO1}</b> empleados asignados.
                            El segundo puesto con mayor riesgo en la Desconcentrada corresponde al aplicativo <b>{PSTO2}</b>, con <b>{VLTO2}</b> empleados registrados.
                        </p>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_content
