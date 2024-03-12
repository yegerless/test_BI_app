import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#'SteelBlue', 'PaleTurquoise'

'Cards with numbers'
# Всего ОКС
total_ACS_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("Всего ОКС", className="card-title"), #style={'background-color': 'CornflowerBlue'},
                       className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='total_ASC'))
    ],
    #color="AliceBlue", outline=True, style={},
    className='information_card_1')

# Кол-во ОКС с подъемом ST
ACS_with_elevation_ST_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("ОКС с подъемом ST", className="card-title"), #style={'background-color': 'CornflowerBlue'},
                       className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='cnt_ACS_with_elevation_ST'))
    ],
    #color="AliceBlue", outline=True, style={},
    className='information_card_1')

# Кол-во ОКС без подъема ST
ACS_without_elevation_ST_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("ОКС без подъема ST", className="card-title"), #style={'background-color': 'CornflowerBlue'},
                       className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='cnt_ACS_without_elevation_ST'))
    ],
    #color="AliceBlue", outline=True, style={},
    className='information_card_1')

# Охват ЧКВ
PCI_coverage_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Охват ЧКВ', className="card-title"), className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='PCI_coverage'))
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# Летальность при ОКС
ACS_mortality_rate_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Летальность ОКС', className="card-title"), className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='ACS_mortality_rate'))
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# Летальность при ИМ
MI_mortality_rate_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Летальность ИМ', className="card-title"), className='information_card_header_1'),
        dbc.CardBody(html.P(className="card-text", id='MI_mortality_rate'))
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# ОКСпST
ACS_with_elevation_ST_information_card = dbc.Card(
    children=[
        dbc.CardBody(id='count_deaths_ACS_with_eST'),
        dbc.CardBody(id='mortality_rate_ACS_with_eST'),
        dbc.CardBody(id='mortality_rate_ACS_with_eST_ideal_path'),
        dbc.CardBody(id='part_deaths_ACS_with_eST_without_revasc')
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# ОКСбпST высокого риска
ACS_without_elevation_ST_high_risk_information_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('ОКСбпST высокого риска'), className='information_card_header_1'),
        dbc.CardBody(id='PTCA_coverage_ACS_without_eST_high_risk'),
        dbc.CardBody(id='mortality_rate_ACS_without_eST_high_risk')
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# ОКСбпST низкого риска
ACS_without_elevation_ST_low_risk_information_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('ОКСбпST низкого риска'), className='information_card_header_1'),
        dbc.CardBody(id='PTCA_coverage_ACS_without_eST_low_risk'),
        dbc.CardBody(id='mortality_rate_ACS_without_eST_low_risk')
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')

# Шок
Shock_information_card = dbc.Card(
    children=[
        dbc.CardBody(id='count_shock'),
        dbc.CardBody(id='PTCA_coverage_for_shock'),
        dbc.CardBody(id='mortality_rate_shock'),
        dbc.CardBody(id='part_shock_for_deaths')
    ],
    #color='primary', outline=True, style={},
    className='information_card_1')


content = html.Div(
    style={"margin-left": "18rem", "margin-right": "2rem"}, #, #"padding": "2rem 1rem"},
    children=[
        #Заголовок дашборда
        html.Div(children='Мониторинг ОКС Новгородская область', className='header_1'),

        # Блок карточек с цифрами по кол-ву ОКС
        html.Div(
            children=[total_ACS_card, ACS_with_elevation_ST_card, ACS_without_elevation_ST_card],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '15%', 'left': 0}),

        # График динамика кол-ва и летальности ОКС по месяцам
        html.Div(
            children=[dcc.Graph(id='ACS_bar')],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '85%', 'right': 0}
        ),

        # Горизонтальная линия между блоками дашборда
        html.Hr(),

        # Блок карточек с цифрами по охвату ЧКВ и летальности при ОКС и ИМ
        html.Div(
            children=[PCI_coverage_card, ACS_mortality_rate_card, MI_mortality_rate_card],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '15%', 'left': 0}
        ),

        # График динамика кол-ва выбывших и летальности при ИМ по месяцам
        html.Div(
            children=[dcc.Graph(id='MI_bar')],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '85%', 'right': 0}
        ),

        # Горизонтальная линия между блоками дашборда
        html.Hr(),

        # Блок с дополнительной информацией по ОКСпST (график-воронка + карточка с показателями летальности)
        html.Div(
            children=[
                html.H5(children='ОКСпST',
                        style={'textAlign': 'center'}
                        # 'position': 'relative', 'width': 1820, 'top': 10}
                        ),
                dcc.Graph(id='ACS_path_funnel'),
                ACS_with_elevation_ST_information_card
            ],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '33%', 'left': 0}
        ),

        # Блок с дополнительной информацией по ОКСбпST (гистограмма с кол-вом по риску и карточки с ЧКВ и летальностью)
        html.Div(
            children=[
                html.H5(children='ОКСбпST', style={'textAlign': 'center'}),
                dcc.Graph(id='ACS_without_eST_risk'),
                ACS_without_elevation_ST_high_risk_information_card,
                ACS_without_elevation_ST_low_risk_information_card
            ],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '33%', 'left': 0}
        ),

        # Блок с дополнительной информацией по шоку при ОКС (график + карточка)
        html.Div(
            children=[
                html.H5(children='Шок', style={'textAlign': 'center'}),
                dcc.Graph(id='Shock_bar'),
                Shock_information_card
            ],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '33%', 'left': 0}
        )





    ]
)
