# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_excel(r'\\dfs-02\DKH_2\Gbmu\Новгород\Мониторинг_Новгород.xlsx')

'Cards with filters'
# Фильр с выбором года
year_choice_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Выберите год отчета')),
        dbc.CardBody(dcc.RadioItems(options=['2022', '2023', '2024'], value='2023', id='year_choice'))
    ],
    color="primary", outline=True, style={})

# Фильтр по больнице
hospital_choice_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Выберите стационар')),
        dbc.CardBody(dcc.Checklist(options=df.Hospital.unique(), value=df.Hospital.unique(), id='hospital_choice'))
    ],
    color="primary", outline=True, style={})


'Cards with numbers'
# Всего ОКС
total_ACS_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("Всего ОКС", className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='total_ASC'))
    ],
    color="primary", outline=True, style={})

# Кол-во ОКС с подъемом ST
ACS_with_elevation_ST_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("ОКС с подъемом ST", className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='cnt_ACS_with_elevation_ST'))
    ],
    color="primary", outline=True, style={})

# Кол-во ОКС без подъема ST
ACS_without_elevation_ST_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5("ОКС без подъема ST", className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='cnt_ACS_without_elevation_ST'))
    ],
    color="primary", outline=True, style={})

# Охват ЧКВ
PCI_coverage_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Охват ЧКВ', className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='PCI_coverage'))
    ],
    color='primary', outline=True, style={})

# Летальность при ОКС
ACS_mortality_rate_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Летальность ОКС', className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='ACS_mortality_rate'))
    ],
    color='primary', outline=True, style={})

# Летальность при ИМ
MI_mortality_rate_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('Летальность ИМ', className="card-title")),
        dbc.CardBody(html.P(className="card-text", id='MI_mortality_rate'))
    ],
    color='primary', outline=True, style={})

# ОКСпST
ACS_with_elevation_ST_information_card = dbc.Card(
    children=[
        dbc.CardBody(id='count_deaths_ACS_with_eST'),
        dbc.CardBody(id='mortality_rate_ACS_with_eST'),
        dbc.CardBody(id='mortality_rate_ACS_with_eST_ideal_path'),
        dbc.CardBody(id='part_deaths_ACS_with_eST_without_revasc')
    ],
    color='primary', outline=True, style={})

# ОКСбпST высокого риска
ACS_without_elevation_ST_high_risk_information_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('ОКСбпST высокого риска')),
        dbc.CardBody(id='PTCA_coverage_ACS_without_eST_high_risk'),
        dbc.CardBody(id='mortality_rate_ACS_without_eST_high_risk')
    ],
    color='primary', outline=True, style={})

# ОКСбпST низкого риска
ACS_without_elevation_ST_low_risk_information_card = dbc.Card(
    children=[
        dbc.CardHeader(html.H5('ОКСбпST низкого риска')),
        dbc.CardBody(id='PTCA_coverage_ACS_without_eST_low_risk'),
        dbc.CardBody(id='mortality_rate_ACS_without_eST_low_risk')
    ],
    color='primary', outline=True, style={})

# Шок
Shock_information_card = dbc.Card(
    children=[
        dbc.CardBody(id='count_shock'),
        dbc.CardBody(id='PTCA_coverage_for_shock'),
        dbc.CardBody(id='mortality_rate_shock'),
        dbc.CardBody(id='part_shock_for_deaths')
    ],
    color='primary', outline=True, style={})

'Sidebar'
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 10,
    "left": 0,
    "bottom": 0,
    "width": "15%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'display': 'inline-block',
    'vertical-align': 'top'
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)