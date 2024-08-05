##### Funciones Dashboard-Contenedores SAT-CECTI-2024
#### Elaboro: Ladino Álvarez Ricardo Arturo


#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import os
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
# Empleado Riesgos App

def Content_Acceso_Info(BASE_USO_F3):

    ROL_APP = BASE_USO_F3.ROL_APP.sum()
    PER_APP = round(((BASE_USO_F3.iloc[0, 2]) * 100) / (ROL_APP), 2)
    TOTL_APP = BASE_USO_F3.APLICATIVO.count()
    
    html_content = f"""
    <div class="container-fluid" style="height: 100%; width: 100%;">
        <div class="row" style="height: 100%;">
            <div class="col-12" style="height: 100%;">
                <div class="card" style="width: 100%; height: 100%; border: 2px solid #FFFFFF;">
                    <div class="card-body" style="height: 100%;">
                        <h6 class="card-title"><b>ACCESO A SISTEMAS INFORMÁTICOS</b></h6>
                        <p class="card-text" style="text-left: justify; font-size: 13px;">
                            El empleado <b>{BASE_USO_F3.iloc[0,0]}</b> cuenta con un total de <b>{ROL_APP}</b> roles distintos distribuidos en <b>{TOTL_APP}</b> aplicativos. 
                            El aplicativo con mayor importancia (<b>{PER_APP}%</b>) corresponde a <b>{BASE_USO_F3.iloc[0,1]}</b> con <b>{BASE_USO_F3.iloc[0,2]}</b> roles disntitos.
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

