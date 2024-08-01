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
# Contenedor Barras Riesgo
def Content_Confia_Riesgo():
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