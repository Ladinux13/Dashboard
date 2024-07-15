##### Funciones Dashboard SAT-CECTI-2024
#### Elaboro: Ladino Álvarez Ricardo Arturo


#%%%%%%%%%%%%%%%% Librerias %%%%%%%%%%%%%%%%

import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.colors as mcolors

import warnings
warnings.filterwarnings("ignore",
                        category = DeprecationWarning)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Totales_Menu(Tabla):
    ''' '''
    TOTAL = Tabla.groupby(['PUESTO_NOM','PTO_RIESGO'])['EMPLEADO'].nunique().sum()
    SI = Tabla[Tabla['PTO_RIESGO'] == 'SI'].groupby(['CVE_UNIDAD','PUESTO_NOM'])['EMPLEADO'].\
         nunique().reset_index().sort_values(by=['EMPLEADO'], 
                                             ascending=False)
    SI_R  = SI.sum().iloc[2]
    UNIDAD = SI.iloc[0, 0]
    return (UNIDAD, TOTAL, SI_R, SI )


def Mapa_Menu (UNIDAD, GEOJSON):
    ''' '''
    GEOJSON['color'] = GEOJSON['UNIDAD_ADM'].apply(lambda x: 'red' if x == UNIDAD else 'grey')
    MAPA = px.choropleth_mapbox(GEOJSON, 
                                geojson=GEOJSON['geometry'],
                                locations=GEOJSON.index,
                                color='color',
                                color_discrete_map={'red': 'rgb(153, 0, 51)', 'grey': 'rgb(0, 102, 102)'},
                                mapbox_style="open-street-map",
                                center={'lat': 23.1898375, 'lon': -102.4821213},
                                zoom=3.5,
                                opacity=0.5,
                                hover_data= {'color': False}
                               )
    MAPA.update_traces(marker_line_width=0.5, hovertemplate=None, hoverinfo= 'none')
    MAPA.update_layout(showlegend=False,
                       title_text="Modificar y centrar titulo",
                       margin={"r": 50, "t": 50, "l": 50, "b": 50})
    return (MAPA)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#>
def Puestos_Menu(Tabla):
    ''' '''
    labels = ['Puesto con Riesgo', 'Puesto sin Riesgo']
    TOTAL = Tabla.PUESTO_NOM.nunique()
    values = [Tabla[Tabla['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique(), 
              Tabla[Tabla['PTO_RIESGO'] == 'NO'].PUESTO_NOM.nunique()]

    PASTEL = go.Figure(data=[go.Pie(labels=labels, 
                                    values=values, 
                                    hole=0.5,
                                    textinfo='label+value+percent', 
                                    hoverinfo='label+value+percent',
                                    texttemplate='%{label}<br>%{value} (%{percent})',
                                    textposition='outside',
                                    marker=dict(colors=['rgb(153, 0, 51)','rgb(0, 102, 102)'],
                                                line = dict(color = '#FFFFFF', width = 0.5)))]
                      )

    PASTEL.update_layout(annotations=[dict(text=f'Total Puestos<br>{TOTAL}',
                                           x=0.5,
                                           y=0.5, 
                                           font_size=20, 
                                           showarrow=False, 
                                           font = dict( family = "Montserrat"))],
                         showlegend=False)
    
    PASTEL.update_layout(showlegend=False, title_text="Modificar y centrar titulo",
                         margin={"r": 50, "t": 50, "l": 50, "b": 50})
    
    PASTEL.update_traces(marker_line_width=0.5, 
                         hovertemplate=None, hoverinfo= 'none')
    
    PASTEL.update_layout(title_font_size = 15,
                         title_x = 0.5,
                         font = dict(family = "Montserrat",
                                     size = 13,
                                     color = '#000000'))
    return (PASTEL)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Riesgo_Puestos_Menu (Tabla):
    ''' '''
    Tabla['PUESTO_NOM_ORD'] = Tabla['PUESTO_NOM'].astype(str) + ' '
    
    unique_positions = Tabla['PUESTO_NOM_ORD'].unique()
    num_positions = len(unique_positions)
    
    cmap = mcolors.LinearSegmentedColormap.from_list("", ['#990033','#808080', '#006666'])

    if num_positions > 1:
        colors = [mcolors.to_hex(cmap(i/(num_positions -1))) for i in range(num_positions)]
    else:
        colors = [mcolors.to_hex(cmap(0))]

    #colors = [mcolors.to_hex(cmap(i / (num_positions - 1))) for i in range(num_positions)]

    color_map = dict(zip(unique_positions, colors))
    
    BARRAS = px.bar(Tabla,
                    y = 'EMPLEADO',
                    x = 'PUESTO_NOM_ORD',
                    orientation = 'v',
                    color = 'PUESTO_NOM_ORD',
                    color_discrete_map = color_map,
                    text = 'EMPLEADO')
    
    BARRAS.update_traces(marker_line_width = 0.5,
                         textposition = 'auto',
                         hovertemplate = None, 
                         hoverinfo = 'none')
    
    BARRAS.update_layout( plot_bgcolor = 'white', 
                         xaxis_title = "",
                         yaxis_title = "",
                         yaxis = dict(showticklabels = False), 
                         xaxis = dict(showticklabels = False,
                                      categoryorder = 'total descending'),
                         margin = {"r": 50, "t": 50, "l": 50, "b": 50}, 
                         legend_title_text = 'Puestos',
                         legend=dict(orientation = "h",
                                     yanchor = "top",
                                     y = -0.1,
                                     xanchor = "center",
                                     x = 0.5,
                                     title_font = dict(size = 12),
                                     font = dict(size = 10),
                                     traceorder = "normal")
                        )
    
    BARRAS.layout.legend.update(title = dict(text = 'Puestos',
                                             font = dict(size = 12),
                                             side = 'top')
                               )
    BARRAS.update_layout(title_font_size = 15,
                              title_x = 0.5,
                              font = dict(family = "Montserrat",
                                          size = 12,
                                          color = '#000000')
                        )
    return (BARRAS)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Quejas_Denuncias_Riesgos (Tabla): ### En esta sección la tabla se crea con query filter
    ''' '''
    TOTAL_PUESTOS = Tabla.PUESTO_NOM.nunique()
    
    TOTAL_PUESTOS_RIESGO = Tabla[Tabla['PTO_RIESGO'] == 'SI'].PUESTO_NOM.nunique()
    
    MAYOR_RIESGO = Tabla[Tabla['PTO_RIESGO'] == 'SI'].groupby('PUESTO_NOM')['EMPLEADO'].\
                                                     nunique().reset_index().sort_values(by = ['EMPLEADO'],
                                                                                         ascending = False)
    
    CONFIABILIDAD = Tabla.groupby('PREVE_OBS')['EMPLEADO'].nunique().reset_index().sort_values(by = ['EMPLEADO'],
                                                                                               ascending = True)
    
    NIVEL_RIESGO = Tabla.groupby('NIVEL_ATENCION')['EMPLEADO'].nunique().reset_index().sort_values(by = ['EMPLEADO'],
                                                                                                   ascending=False)

    QUEJA_DENUNCIA = Tabla.groupby(Tabla['ESTATUS'])['EMPLEADO'].nunique().reset_index().sort_values(by=['EMPLEADO'],
                                                                                                     ascending=False)
    
    NIVELES = ['CRITICO', 'ALTO', 'MEDIO']
    NIVEL = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby('PUESTO_NOM')['EMPLEADO'].nunique().\
                                                        reset_index().sort_values(by=['EMPLEADO'],
                                                                                  ascending=False)
    
    USUARIOS = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby('PUESTO_NOM')\
               .agg(C_C=('EMPLEADO', lambda x: x[Tabla['NIVEL_ATENCION'] == 'CRITICO'].nunique()),
                    A_M_C=('EMPLEADO', lambda x: x[Tabla['NIVEL_ATENCION'].isin(['ALTO', 'MEDIO'])].nunique())).reset_index()
    
    USUARIO_CRITICO = USUARIOS['C_C'].sum()
    USUARIO_ALTOMEDIO = USUARIOS['A_M_C'].sum()
    
    return (TOTAL_PUESTOS,TOTAL_PUESTOS_RIESGO,
            MAYOR_RIESGO, CONFIABILIDAD, NIVEL_RIESGO,
            QUEJA_DENUNCIA, USUARIOS, USUARIO_CRITICO,USUARIO_ALTOMEDIO )
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Cofiabilidad (Tabla):
    ''' '''
    cmap = mcolors.LinearSegmentedColormap.from_list("", ['#990033', '#808080', '#006666'])
    num_classes = len(Tabla['EMPLEADO'])


    if num_classes > 1:
        colors = [mcolors.to_hex(cmap(i/(num_classes -1))) for i in range(num_classes)]
    else:
        colors = [mcolors.to_hex(cmap(0))]

    #colors = [mcolors.to_hex(cmap(i / (num_classes - 1))) for i in range(num_classes)]

    text_info = [f'{Numero}<br>{Texto}' for Numero, Texto in zip(Tabla['EMPLEADO'], Tabla['PREVE_OBS'])]
    
    FUNNEL_CONFIABI = go.Figure(go.Funnel(y = Tabla['PREVE_OBS'],
                                          x = Tabla['EMPLEADO'],
                                          text = text_info,
                                          textposition = "auto",
                                          textinfo = "text",
                                          orientation = 'h',
                                          marker = {"color": colors},
                                          connector = {"line": {"color": "#000000", "dash": "solid", 
                                                                "width": 0.5}, "fillcolor": "#F1F1E8"})
                               )
    
    FUNNEL_CONFIABI.update_layout(title_font_size = 12, yaxis = dict(showticklabels = False),
                                  title_x = 0.5,
                                  font = dict( family = "Montserrat",
                                              size = 12,
                                              color = '#000000'),
                                  template = None, showlegend = False,
                                  margin = {"r": 50, "t": 50, "l": 50, "b": 50})
    
    FUNNEL_CONFIABI.update_traces(hovertemplate = None, hoverinfo = 'none')
    
    return (FUNNEL_CONFIABI)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Queja_Denuncia(Tabla):
    ''' '''
    cmap = mcolors.LinearSegmentedColormap.from_list("", ['#990033', '#808080', '#006666'])
    num_classes = len(Tabla['EMPLEADO'])
    colors = [mcolors.to_hex(cmap(i / (num_classes - 1))) for i in range(num_classes)]

    text_info = [f'{Numero}<br>{Texto}' for Numero, Texto in zip(Tabla['EMPLEADO'], Tabla['ESTATUS'])]

    FUNNEL_QD = go.Figure(go.Funnel(y = Tabla['ESTATUS'],
                                    x = Tabla['EMPLEADO'],
                                    text = text_info,
                                    textposition = "auto",
                                    textinfo = "text",
                                    orientation = 'h',
                                    marker = {"color": colors},
                                    connector = {"line": {"color": "#000000",
                                                          "dash": "solid", "width": 0.5},
                                                 "fillcolor": "#F1F1E8"}
                                   )
                         )

    FUNNEL_QD.update_layout(title_font_size = 12, yaxis = dict(showticklabels = False),
                            title_x = 0.5,
                            font = dict(family = "Montserrat",
                                        size = 12,
                                        color = '#000000'),
                            template = None, showlegend = False,
                            margin = {"r": 50, "t": 50, "l": 50, "b": 50}
                           )
    FUNNEL_QD.update_traces(hovertemplate = None, hoverinfo = 'none')
    
    return (FUNNEL_QD)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Nivel_Riesgos_Atencion (Tabla):
    ''' '''
    colors = ['#218a8a', '#006666', '#ffff00', '#f59600', '#ad0303']
    
    TREE_ATENCION = go.Figure(go.Treemap(labels = Tabla['NIVEL_ATENCION'],
                                         parents = [""] * len(Tabla['NIVEL_ATENCION']),
                                         values = Tabla['EMPLEADO'],
                                         marker = dict(colors=colors),
                                         textinfo = 'label+value',
                                         textposition = 'middle center')
                             )
    
    TREE_ATENCION.update_layout(title_font_size = 12, yaxis = dict(showticklabels = False),
                                title_x = 0.5,
                                font = dict( family = "Montserrat",
                                            size = 12,
                                            color = '#000000'),
                                template = None, showlegend = False,
                                margin = {"r": 50, "t": 50, "l": 50, "b": 50},
                                uniformtext=dict(minsize = 10, mode ='hide'))
    
    TREE_ATENCION.update_traces(hovertemplate = None, hoverinfo = 'none')
    
    return (TREE_ATENCION)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Detalle_Aplicativos(Tabla): #En esta seccion entra el segundo fitro, que anida al primero
    ''' '''
    NIVELES = ['CRITICO', 'ALTO', 'MEDIO']
    TABLA_DETALLE = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby(['RFC_CORTO','EMPLEADO', 'NOMBRE_EMP', 
                                                                          'PTO_RIESGO', 'PREVE_OBS', 'DENUNCIAS',
                                                                          'NIVEL_ATENCION'])['APLICATIVO'].nunique().reset_index()
    
    SISTEMA_INFORMATICO = Tabla[Tabla['NIVEL_ATENCION'].isin(NIVELES)].groupby(['NOMBRE_EMP','APLICATIVO'])['ROL_APP'].\
                          nunique().reset_index().sort_values(by=['ROL_APP'], ascending=False)
    
    return (TABLA_DETALLE, SISTEMA_INFORMATICO)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Tabla_Aplicativos (Tabla):
    ''' '''
    Tabla.rename(columns={'RFC_CORTO': 'RFC corto', 
                          'EMPLEADO': 'No. Empleado', 
                          'NOMBRE_EMP': 'Nombre Empleado',
                          'PTO_RIESGO':'Puesto Riesgo (ACAER)',
                          'PREVE_OBS':'Confiabilidad Estatus',
                          'DENUNCIAS':'No. Denuncias',
                          'NIVEL_ATENCION':'Nivel Riesgo',
                          'APLICATIVO':'No. Sistemas'}, inplace=True
                 )
    
    pto_riesgo_colors = ['#68000C' if val == 'SI' else '#FFFFFF' for val in Tabla['Puesto Riesgo (ACAER)']]
    
    nivel_atencion_colors = []
    for val in Tabla['Nivel Riesgo']:
        if val == 'MEDIO':
            nivel_atencion_colors.append('#ffff00')
        elif val == 'ALTO':
            nivel_atencion_colors.append('#f59600')
        elif val == 'CRITICO':
            nivel_atencion_colors.append('#ad0303')
        else:
            nivel_atencion_colors.append('#FFFFFF')

    pto_riesgo_text_colors = ['#FFFFFF' if val == 'SI' else '#000000' for val in Tabla['Puesto Riesgo (ACAER)']]
    
    TABLA = go.Figure(data = [go.Table(header = dict(values = list(Tabla.columns),
                                                     fill_color = '#B38E5D',
                                                     font = dict(color = '#FFFFFF'), 
                                                     align='center'),
                                       cells=dict(values = [Tabla[col] for col in Tabla.columns],
                                                  fill_color = [['#FFFFFF']*len(Tabla),
                                                                ['#FFFFFF']*len(Tabla),
                                                                ['#FFFFFF']*len(Tabla), 
                                                                pto_riesgo_colors, 
                                                                ['#FFFFFF']*len(Tabla), 
                                                                ['#FFFFFF']*len(Tabla),
                                                                nivel_atencion_colors,
                                                                ['#FFFFFF']*len(Tabla)],
                                                  font = dict(color = [['black']*len(Tabla),
                                                                       ['black']*len(Tabla),
                                                                       ['black']*len(Tabla),
                                                                       pto_riesgo_text_colors,
                                                                       ['black']*len(Tabla),
                                                                       ['black']*len(Tabla),
                                                                       ['black']*len(Tabla),
                                                                       ['black']*len(Tabla)]
                                                             ),
                                                  line_color='#000000',
                                                  align='center'))
                             ]
                     )
    
    TABLA.update_layout(title_font_size = 12,
                        title_x = 0.5,
                        font = dict( family = "Montserrat",
                                    size = 12,
                                    color = '#000000'),
                        template = None, showlegend = False,
                        margin = {"r": 50, "t": 50, "l": 50, "b": 50},
                        uniformtext=dict(minsize = 10, mode ='hide')
                       )
    
    return (TABLA)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 
def Accesos_Aplicaticos(Tabla):
    ''' '''
    cmap = mcolors.LinearSegmentedColormap.from_list("", ['#990033', '#808080', '#006666'])
    
    num_apps = len(Tabla)
    colors = [mcolors.to_hex(cmap(i / (num_apps - 1))) for i in range(num_apps)]
    
    max_value = Tabla['ROL_APP'].max()
    
    pull_values = [0.1 if val > 0.80 * max_value else 0 for val in Tabla['ROL_APP']]
    
    PASTEL = px.pie(Tabla,
                    names = 'APLICATIVO',
                    values = 'ROL_APP')
    
    PASTEL.update_traces(pull = pull_values,
                         marker = dict(colors = colors,
                                       line = dict(color = '#FFFFFF', width = 0.5)
                                      ),
                         textposition = 'outside',
                         textinfo = 'label+percent', 
                         insidetextorientation = 'radial',
                         hovertemplate = None,
                         hoverinfo =  'none')
    
    PASTEL.update_traces(pull = pull_values,
                         marker = dict(colors = colors), 
                         hole=0
                        )
    
    PASTEL.update_layout(title_font_size = 12,
                         title_x = 0.5,
                         font = dict( family = "Montserrat",
                                     size = 10,
                                     color = '#000000'),
                         template = None, showlegend = False,
                         margin = {"r": 0, "t": 0, "l": 0, "b": 30},
                         uniformtext = dict(minsize = 10, mode ='hide')
                        )
    return (PASTEL)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#> 