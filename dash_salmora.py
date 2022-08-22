import os
import base64
from turtle import color
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable

def cal_incr_sal(dens_var_1, flowrate_var, dens, flow, incr10, incr25, incr50, incr75, incr100):
    #Cálculo do incremento de salinidade para uma condição de descarte

    x_d = dens.size
    x_fr = flow.size

    # dens_input= 1165       ############----INPUT - BRINE DENSITY
    pos_d = (dens_var_1-1054.99999)/((1199-1055)/90)
    dens_pos_down = math.floor(pos_d)
    dens_pos_up = math.ceil(pos_d)

    dens_up=dens[dens_pos_down]
    dens_down=dens[dens_pos_up]

    # flowrate_input = 1112  ############----INPUT - DISCHARGE FLOW RATE
    pos_fr = (flowrate_var-199.9999)/(1000/90)
    fr_pos_down = math.floor(pos_fr)
    fr_pos_up = math.ceil(pos_fr)

    fr_up=flow[fr_pos_up]
    fr_down=flow[fr_pos_down]

    # para 10m
    salinity_up10=incr10[dens_pos_up,fr_pos_up]
    salinity_down10=incr10[dens_pos_down,fr_pos_down]
    salinity_result10= salinity_down10-(salinity_down10-salinity_up10)*(fr_down-flowrate_var)/(fr_down-fr_up)

    # para 25 m
    salinity_up25=incr25[dens_pos_up,fr_pos_up]
    salinity_down25=incr25[dens_pos_down,fr_pos_down]
    salinity_result25= salinity_down25-(salinity_down25-salinity_up25)*(fr_down-flowrate_var)/(fr_down-fr_up)

    # para 50 m
    salinity_up50=incr50[dens_pos_up,fr_pos_up]
    salinity_down50=incr50[dens_pos_down,fr_pos_down]
    salinity_result50= salinity_down50-(salinity_down50-salinity_up50)*(fr_down-flowrate_var)/(fr_down-fr_up)

    # para 75 m
    salinity_up75=incr75[dens_pos_up,fr_pos_up]
    salinity_down75=incr75[dens_pos_down,fr_pos_down]
    salinity_result75= salinity_down75-(salinity_down75-salinity_up75)*(fr_down-flowrate_var)/(fr_down-fr_up)

    # para 100 m
    salinity_up100=incr100[dens_pos_up,fr_pos_up]
    salinity_down100=incr100[dens_pos_down,fr_pos_down]
    salinity_result100= salinity_down100-(salinity_down100-salinity_up100)*(fr_down-flowrate_var)/(fr_down-fr_up)

    return salinity_result10, salinity_result25, salinity_result50, salinity_result75, salinity_result100


def cal_vaz_otm(dens_var_2, dens, flow, incr10, incr25, incr50, incr75, incr100):
    #Cálculo da vazão ótima de descarte

    # dens_input_2 = 1165     #################### INPUT - BRINE DISCHARGE DENSITY
    pos_d_2 = (dens_var_2-1054.9999)/((1199-1055)/90)
    dens_pos_down_2 = math.floor(pos_d_2)
    dens_pos_up_2 = math.ceil(pos_d_2)
    dens_up_2 = dens[dens_pos_down_2]
    dens_down_2 = dens[dens_pos_up_2]
    p=0
    output_salinity_100=10000.0
    output_salinity_75=10000.0
    output_salinity_50=10000.0
    output_salinity_25=10000.0
    output_salinity_10=10000.0

    while p < dens.size:
        #calculo de salinidade para cada vazão para 100m
        #pos_fr = (flowrate_input-500)/(700/90)
        fr_pos_fr_2 = flow[p]

        #Distância de 100.0 m
        salinity_up100_2 = incr100[dens_pos_up_2,p]
        salinity_down100_2 = incr100[dens_pos_down_2,p]
        salinity_result100_2 = salinity_down100_2+(salinity_up100_2-salinity_down100_2)*(dens_var_2-dens_down_2)/(dens_up_2-dens_down_2)

        if (salinity_result100_2 <= output_salinity_100):
            output_salinity_100 = salinity_result100_2
            minor_value_position100 = p
            minor_flow_rate100 = flow[p]

        #Distância de 75.0 m
        salinity_up75_2 = incr75[dens_pos_up_2,p]
        salinity_down75_2 = incr75[dens_pos_down_2,p]
        salinity_result75_2 = salinity_down75_2+(salinity_up75_2-salinity_down75_2)*(dens_var_2-dens_down_2)/(dens_up_2-dens_down_2)

        if (salinity_result75_2 <= output_salinity_75):
            output_salinity_75 = salinity_result100_2
            minor_value_position75 = p
            minor_flow_rate75 = flow[p]

        #Distância de 50.0 m
        salinity_up50_2 = incr50[dens_pos_up_2,p]
        salinity_down50_2 = incr50[dens_pos_down_2,p]
        salinity_result50_2 = salinity_down50_2+(salinity_up50_2-salinity_down50_2)*(dens_var_2-dens_down_2)/(dens_up_2-dens_down_2)

        if (salinity_result50_2 <= output_salinity_50):
            output_salinity_50 = salinity_result50_2
            minor_value_position50 = p
            minor_flow_rate50 = flow[p]

        #Distância de 25.0 m
        salinity_up25_2 = incr25[dens_pos_up_2,p]
        salinity_down25_2 = incr25[dens_pos_down_2,p]
        salinity_result25_2 = salinity_down25_2+(salinity_up25_2-salinity_down25_2)*(dens_var_2-dens_down_2)/(dens_up_2-dens_down_2)

        if (salinity_result25_2 <= output_salinity_25):
            output_salinity_25 = salinity_result25_2
            minor_value_position25 = p
            minor_flow_rate25 = flow[p]

        #Distância de 10.0 m 
        salinity_up10_2 = incr10[dens_pos_up_2,p]
        salinity_down10_2 = incr10[dens_pos_down_2,p]
        salinity_result10_2 = salinity_down10_2+(salinity_up10_2-salinity_down10_2)*(dens_var_2-dens_down_2)/(dens_up_2-dens_down_2)

        if (salinity_result10_2 <= output_salinity_10):
            output_salinity_10 = salinity_result10_2
            minor_value_position10 = p
            minor_flow_rate10 = flow[p] 
     
        p=p+1

    return output_salinity_100, minor_flow_rate100


def calc_MV_lmt(dens_var_3, salinity_limit_var_100, dens, flow, incr10, incr25, incr50, incr75, incr100):
    # Cálculo da maior vazão possível para um limite de incremento de salinidade
    # dens_input_3 = 1165
    # salinity_limit_input_100 = 2.0
    salinity_limit_var_50 = 7.0

    pos_d_3 = (dens_var_3-1054.9999)/((1199-1055)/90)
    dens_pos_down_3 = math.floor(pos_d_3)
    dens_pos_up_3 = math.ceil(pos_d_3)
    dens_up_3 = dens[dens_pos_down_3]
    dens_down_3 = dens[dens_pos_up_3]
    p=0
    flowrate_output100=0.0
    flowrate_output50=0.0

    while p < dens.size:
        #calculo de salinidade para cada vazão para 100m
        #pos_fr = (flowrate_input-500)/(700/90)
        fr_pos_fr_3 = flow[p]

        #Distância de 100.0 m
        salinity_up100_3 = incr100[dens_pos_up_3,p]
        salinity_down100_3 = incr100[dens_pos_down_3,p]
        salinity_result100_3 = salinity_down100_3+(salinity_up100_3-salinity_down100_3)*(dens_var_3-dens_down_3)/(dens_up_3-dens_down_3)

        if (salinity_result100_3 <= salinity_limit_var_100):
            
            if(flow[p]>=flowrate_output100):
                output_salinity_100 = salinity_result100_3
                minor_value_position100 = p
                opt_flowrate_100 = flow[p]


        #Distância de 50.0 m
        salinity_up50_3 = incr50[dens_pos_up_3,p]
        salinity_down50_3 = incr50[dens_pos_down_3,p]
        salinity_result50_3 = salinity_down50_3+(salinity_up50_3-salinity_down50_3)*(dens_var_3-dens_down_3)/(dens_up_3-dens_down_3)

        if (salinity_result50_3 <= salinity_limit_var_50):
            
            if(flow[p]>=flowrate_output50):
                output_salinity_50 = salinity_result50_3
                minor_value_position50 = p
                opt_flowrate_50 = flow[p]

            
        p=p+1
        
    return opt_flowrate_100, output_salinity_100

card_1 = dbc.Spinner(dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col([html.H5(id='titulo_card_1', children='Incrementos de salinidade para condições operacionais específicas', style={"textAlign": "center",})], md=10),
                dbc.Col([html.Button(id="button_1", children="Calcular!")], md=2),
            ]),
        dbc.Row(
            [
            dbc.Col([
                 html.Div(id='text_dens_1', children='Densidade [kg/m³]:'),
                 dcc.Input(id='dens_input_1', type='number', value=1100), 
                    ], md=6),
            dbc.Col([
                 html.Div(id='text_flowrate', children='Vazão [barris/h]:'),
                 dcc.Input(id='flowrate_input', type='number', value=1000),
                    ], md=6),    
            ]),
        html.Br(),
        html.Div(
                [
                html.Div(id="salinity_result10",),
                html.Div(id="salinity_result25",),
                html.Div(id="salinity_result50",),
                html.Div(id="salinity_result75",),
                html.Div(id="salinity_result100",),
                ],
                )
        # html.Div(
        #         [
        #         html.Div(f"Incremento de salninidade - 10,0 m: 10 g/kg",),
        #         html.Div(f"Incremento de salninidade - 25,0 m: 10 g/kg",),
        #         html.Div(f"Incremento de salninidade - 50,0 m: 10 g/kg",),
        #         html.Div(f"Incremento de salninidade - 75,0 m: 10 g/kg",),
        #         html.Div(f"Incremento de salninidade - 100,0 m: 10 g/kg",),
        #         ],
        #         )
    ],
    body=True,
    color = "PowderBlue",
    outline=False,
))

card_2 = dbc.Spinner(dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col([html.H5(id='titulo_card_2', children='Vazão ótima de descarte', style={"textAlign": "center",})], md=10),
                dbc.Col([html.Button(id="button_2", children="Calcular!")], md=2),
            ]),
        dbc.Row(
            [
            dbc.Col([
                html.Div(id='text_dens_2', children='Densidade [kg/m³]:'),
                dcc.Input(id='dens_input_2', type='number', value=1100), 
                ], md=6),
            ]),
        html.Br(),
        html.Div(
                [
                html.Div(f"Distância - 100,0 m",),
                html.Div(id="output_salinity_100_2",),
                html.Div(id="minor_flow_rate100",),
                # html.Div(f"Incremento de salninidade: 10 g/kg",),
                # html.Div(f"Vazão ótima: 10 barris/h",),
                ],
                )
#                 print('   Distância - 100,0 m')
# print('   Incremento de salinidade - ',output_salinity_100)
# print('   Vazão ótima - ',minor_flow_rate100)
    ],
    body=True,
    color = "PowderBlue",
    outline=False,
))

card_3 = dbc.Spinner(dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col([html.H5(id='titulo_card_3', children='Incrementos de salinidade para condições operacionais específicas', style={"textAlign": "center",})], md=10),
                dbc.Col([html.Button(id="button_3", children="Calcular!")], md=2),
            ]),
        html.Br(),
        dbc.Row(
            [
            dbc.Col([
                 html.Div(id='text_dens_3', children='Densidade [kg/m³]:'),
                 dcc.Input(id='dens_input_3', type='number', value=1100),], md=6),
            dbc.Col([
                 html.Div(id='text_salinity_limit_100', children='Incremento de salinidade a 100 m:'),
                 dcc.Input(id='salinity_limit_input_100', type='number', value=5),], md=6),   
            ]),
        html.Br(),
        html.Div(
                [
                html.Div(f"Distância - 100,0 m",),
                html.Div(id="opt_flowrate_100",),
                html.Div(id="output_salinity_100_3"),
                # html.Div(f"Vazão permitida: 10 barris/h",),
                # html.Div(f"Incremento de salinidade: 10 g/kg",),
                ],
                )
    ],
    body=True,
    color = "PowderBlue",
    outline=False,
))

# ------------------------------------------------------------------#### main ####------------------------------------------------------------------------- #

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [
        html.Br(),
        html.Div([
            dbc.Row([   
                dbc.Col(html.H2("Impacto ambiental de operações offshore - Descarte de Salmoura", style={"textAlign":"left", "font-family":"Verdana"}), md=11),
                dbc.Col(html.Img(src="https://media-exp2.licdn.com/dms/image/C4E0BAQFqC_QE_7r1Ww/company-logo_200_200/0/1540009367728?e=1663804800&v=beta&t=JARdgH9BSxToupHq9g64c6d-6Bl9JSqBelRPi6ZEPlM", style={'display':'inline-block', 'width': '60%'}) ,md=1),
            ])
        ]),

        html.Hr(),

        dbc.Row(dbc.Col([card_1],md=6)),

        html.Br(),
        
        dbc.Row(dbc.Col([card_2],md=6)),

        html.Br(),
        
        dbc.Row(dbc.Col([card_3],md=6)),
    
    ],
    fluid=True,
)


@app.callback(
    [       
        Output("salinity_result10", "children"),
        Output("salinity_result25", "children"),
        Output("salinity_result50", "children"),
        Output("salinity_result75", "children"),
        Output("salinity_result100", "children"),
        Output("output_salinity_100_2", "children"),
        Output("minor_flow_rate100", "children"),
        Output("opt_flowrate_100", "children"),
        Output("output_salinity_100_3", "children"),
    ],
    [  
        Input("dens_input_1", "value"),
        Input("dens_input_2", "value"),
        Input("dens_input_3", "value"),
        Input("flowrate_input", "value"),
        Input("salinity_limit_input_100", "value"),
        Input('button_1', 'n_clicks'),
        Input('button_2', 'n_clicks'),
        Input('button_3', 'n_clicks'),
    ],
)
    
def update_output(dens_var_1, dens_var_2, dens_var_3, flowrate_var, salinity_limit_var_100, nclik_bt_1, nclik_bt_2, nclik_bt_3):
    
    #To determine if n_clicks is changed. 
    changed_ids = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    button_pressed = ('button_1' or 'button_2' or 'button_3') in changed_ids

    dens=np.loadtxt('dens.txt')
    flow=np.loadtxt('flow.txt')
    incr10=np.loadtxt('salmouraincr_10.txt')
    incr25=np.loadtxt('salmouraincr_25.txt')
    incr50=np.loadtxt('salmouraincr_50.txt')
    incr75=np.loadtxt('salmouraincr_75.txt')
    incr100=np.loadtxt('salmouraincr_100.txt')

    if 'button_1' in changed_ids:
        salinity_result10, salinity_result25, salinity_result50, salinity_result75, salinity_result100 = cal_incr_sal(dens_var_1, flowrate_var, dens, flow, incr10, incr25, incr50, incr75, incr100)
        sr_10 = f"Incremento de salninidade - 10,0 m: {np.round(salinity_result10, 2)} g/kg"
        sr_25 = f"Incremento de salninidade - 25,0 m: {np.round(salinity_result25, 2)} g/kg"
        sr_50 = f"Incremento de salninidade - 50,0 m: {np.round(salinity_result50, 2)} g/kg"
        sr_75 = f"Incremento de salninidade - 75,0 m: {np.round(salinity_result75, 2)} g/kg"
        sr_100 = f"Incremento de salninidade - 100,0 m: {np.round(salinity_result100, 2)} g/kg"
        return sr_10, sr_25, sr_50, sr_75, sr_100, [], [], [] ,[]

    elif 'button_2' in changed_ids:
        output_salinity_100_2, minor_flow_rate100 = cal_vaz_otm(dens_var_2, dens, flow, incr10, incr25, incr50, incr75, incr100)
        os_100_2 = f"Incremento de salninidade: {np.round(output_salinity_100_2, 2)} g/kg"
        mf_100 = f"Vazão ótima: {np.round(minor_flow_rate100, 2)} barris/h"
        return [], [], [], [], [], os_100_2, mf_100, [], []
    
    elif 'button_3' in changed_ids:
        opt_flowrate_100, output_salinity_100_3 = calc_MV_lmt(dens_var_3, salinity_limit_var_100, dens, flow, incr10, incr25, incr50, incr75, incr100)
        of_100 = f"Vazão permitida: {np.round(opt_flowrate_100, 2)} barris/h"
        os_100_3 = f"Incremento de salinidade: {np.round(output_salinity_100_3, 2)} g/kg"
        return [], [], [], [] ,[] , [] ,[], of_100, os_100_3

    else:
        return dash.no_update

    
# def callback(n_clicks):
#     n_clicks=None
#     return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run_server(debug=True)