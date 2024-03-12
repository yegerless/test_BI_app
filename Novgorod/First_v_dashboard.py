# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import dash
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

months_dict = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
               7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

df = pd.read_excel(r'\\dfs-02\DKH_2\Gbmu\Новгород\Мониторинг_Новгород.xlsx')
# df.info()

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



'Dashboard'
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {'background': '#FFFFFF', 'text': '#000000'}

app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'width': 1820, 'height': 720},
    children=[

        # Заголовок дашборда
        html.H1(children='Мониторинг ОКС Новгородская область',
                style={'textAlign': 'center', 'position': 'relative', 'width': 1820, 'top': 10}
                ),

        # Фильтр выбор года
        html.Div(children=[year_choice_card], style={'display': 'inline-block', 'vertical-align': 'top'}),

        # Фильтр по больнице
        html.Div(children=[hospital_choice_card], style={'display': 'inline-block', 'vertical-align': 'top'}),

        # Фильтр с выбором месяцев
        html.Div(
            children=[
                dcc.RangeSlider(min=1, max=12, step=1, marks=months_dict,
                                value=[1, 12], allowCross=False, id='month_choice')
            ],
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'}
            #style={'display': 'inline-block', 'vertical-align': 'right'}
        ),

        # Горизонтальная линия между блоками дашборда
        html.Hr(),

        # Блок карточек с цифрами по кол-ву ОКС
        html.Div(
            children=[total_ACS_card, ACS_with_elevation_ST_card, ACS_without_elevation_ST_card],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '15%', 'left': 0}
        ),

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



])


'''Dashboard's components interactions'''
@callback(
    Output(component_id='total_ASC', component_property='children'),
    Output(component_id='cnt_ACS_with_elevation_ST', component_property='children'),
    Output(component_id='cnt_ACS_without_elevation_ST', component_property='children'),
    Output(component_id='ACS_bar', component_property='figure'),
    Output(component_id='PCI_coverage', component_property='children'),
    Output(component_id='ACS_mortality_rate', component_property='children'),
    Output(component_id='MI_mortality_rate', component_property='children'),
    Output(component_id='MI_bar', component_property='figure'),
    Output(component_id='ACS_path_funnel', component_property='figure'),
    Output(component_id='count_deaths_ACS_with_eST', component_property='children'),
    Output(component_id='mortality_rate_ACS_with_eST', component_property='children'),
    Output(component_id='mortality_rate_ACS_with_eST_ideal_path', component_property='children'),
    Output(component_id='part_deaths_ACS_with_eST_without_revasc', component_property='children'),
    Output(component_id='ACS_without_eST_risk', component_property='figure'),
    Output(component_id='PTCA_coverage_ACS_without_eST_high_risk', component_property='children'),
    Output(component_id='mortality_rate_ACS_without_eST_high_risk', component_property='children'),
    Output(component_id='PTCA_coverage_ACS_without_eST_low_risk', component_property='children'),
    Output(component_id='mortality_rate_ACS_without_eST_low_risk', component_property='children'),
    Output(component_id='Shock_bar', component_property='figure'),
    Output(component_id='count_shock', component_property='children'),
    Output(component_id='PTCA_coverage_for_shock', component_property='children'),
    Output(component_id='mortality_rate_shock', component_property='children'),
    Output(component_id='part_shock_for_deaths', component_property='children'),
    Input(component_id='year_choice', component_property='value'),
    Input(component_id='month_choice', component_property='value'),
    Input(component_id='hospital_choice', component_property='value')
)
def choose_hospital_ASC(year, month, input_hospital):
    month_range = range(month[0], month[1])
    # Всего ОКС
    total_ACS = df.loc[(df['№ п/п'] == 47) &
                       (df['Date'].dt.to_period('Y') == year) &
                       (df['Date'].dt.month.isin(month_range)) &
                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Кол-во ОКС с подъемом ST
    ACS_with_elevation_ST = df.loc[(df['№ п/п'] == '47.1') &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Кол-во ОКС без подъема ST
    ACS_without_elevation_ST = df.loc[(df['№ п/п'] == '47.2') &
                                      (df['Date'].dt.to_period('Y') == year) &
                                      (df['Date'].dt.month.isin(month_range)) &
                                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # График ОКС
    months_ACS_with_eST = df.loc[(df['№ п/п'] == '47.1') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_ACS_with_eST = df.loc[(df['№ п/п'] == '47.1') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index(). \
                            sort_values(by='Month_number', axis='index').replace(months_dict)
    months_ACS_without_eST = df.loc[(df['№ п/п'] == '47.2') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_ACS_without_eST = df.loc[(df['№ п/п'] == '47.2') &
                                 (df['Date'].dt.to_period('Y') == year) &
                                 (df['Date'].dt.month.isin(month_range)) &
                                 (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index(). \
                            sort_values(by='Month_number', axis='index').replace(months_dict)
    cnt_all_ACS = df.loc[(df['№ п/п'] == 47) &
                         (df['Date'].dt.to_period('Y') == year) &
                         (df['Date'].dt.month.isin(month_range)) &
                         (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                        groupby('Month_number')['Value'].sum().reset_index()
    cnt_all_ACS_mortality = df.loc[(df['№ п/п'] == 44) &
                               (df['Date'].dt.to_period('Y') == year) &
                               (df['Date'].dt.month.isin(month_range)) &
                               (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                        groupby('Month_number')['Value'].sum().reset_index()
    df_ACS_mortality_rate = cnt_all_ACS.merge(cnt_all_ACS_mortality, how='inner', on=['Month_number'])
    df_ACS_mortality_rate['Value'] = round(df_ACS_mortality_rate['Value_y'] / df_ACS_mortality_rate['Value_x'] * 100, 2)
    df_ACS_mortality_rate = df_ACS_mortality_rate.sort_values(by='Month_number', axis='index')
    df_ACS_mortality_rate['Month'] = df_ACS_mortality_rate['Month_number'].replace(months_dict)
    ACS_fig = make_subplots(specs=[[{'secondary_y': True}]])
    ACS_fig.add_trace(go.Bar(name='ОКС с подъемом ST', x=months_ACS_with_eST, y=cnt_ACS_with_eST['Value'], text=cnt_ACS_with_eST['Value'],
                          textposition='auto', marker_color='SteelBlue'), secondary_y=False)
    ACS_fig.add_trace(go.Bar(name='ОКС без подъема ST', x=months_ACS_without_eST, y=cnt_ACS_without_eST['Value'], text=cnt_ACS_without_eST['Value'],
                          textposition='auto',  marker_color='PaleTurquoise'), secondary_y=False)
    ACS_fig.update_layout(barmode='stack')
    ACS_fig.add_trace(go.Scatter(x=df_ACS_mortality_rate['Month'], y=df_ACS_mortality_rate['Value'], mode='lines',
                                 name='Летальность ОКС', marker_color='red', text=df_ACS_mortality_rate['Value'],
                                 textposition='top center'),
                      secondary_y=True)
    ACS_fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, yaxis2={'visible': False, 'showticklabels': False})

    # Охват ЧКВ
    PTCA_cnt = df.loc[(df['№ п/п'] == '39.1') &
                      (df['Date'].dt.to_period('Y') == year) &
                      (df['Date'].dt.month.isin(month_range)) &
                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    PCI_coverage = round(PTCA_cnt / total_ACS, 3) if total_ACS > 0 else 0

    # Летальность при ОКС
    ACS_mortality_abs = df.loc[(df['№ п/п'] == 44) &
                               (df['Date'].dt.to_period('Y') == year) &
                               (df['Date'].dt.month.isin(month_range)) &
                               (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_mortality_rate = round(ACS_mortality_abs / total_ACS, 3) if total_ACS > 0 else 0

    # Летальность при ИМ
    MI_mortality_abs = df.loc[(df['№ п/п'] == 48) &
                              (df['Date'].dt.to_period('Y') == year) &
                              (df['Date'].dt.month.isin(month_range)) &
                              (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    total_MI = df.loc[(df['№ п/п'] == 49) &
                      (df['Date'].dt.to_period('Y') == year) &
                      (df['Date'].dt.month.isin(month_range)) &
                      (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    MI_mortality_rate = round(MI_mortality_abs / total_MI, 3) if total_MI > 0 else 0

    # График динамики выбывших и летальности при ИМ
    months_MI = df.loc[(df['№ п/п'] == 49) &
                    (df['Date'].dt.to_period('Y') == year) &
                    (df['Date'].dt.month.isin(month_range)) &
                    (df['Hospital'].isin(input_hospital)), 'Month_number'].replace(months_dict).unique()
    cnt_MI = df.loc[(df['№ п/п'] == 49) &
                    (df['Date'].dt.to_period('Y') == year) &
                    (df['Date'].dt.month.isin(month_range)) &
                    (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index()
    cnt_MI_mortality = df.loc[(df['№ п/п'] == 48) &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), ['Month_number', 'Value']]. \
                            groupby('Month_number')['Value'].sum().reset_index()
    df_MI_mortality_rate = cnt_MI.merge(cnt_MI_mortality, how='inner', on=['Month_number'])
    df_MI_mortality_rate['Value'] = round(df_MI_mortality_rate['Value_y'] / df_MI_mortality_rate['Value_x'] * 100, 2)
    df_MI_mortality_rate = df_MI_mortality_rate.sort_values(by='Month_number', axis='index')
    df_MI_mortality_rate['Month'] = df_MI_mortality_rate['Month_number'].replace(months_dict)
    MI_fig = make_subplots(specs=[[{'secondary_y': True}]])
    MI_fig.add_trace(go.Bar(name='Кол-во выбывших при ИМ', x=months_MI, y=cnt_MI['Value'], text=cnt_MI['Value'],
                          textposition='auto', marker_color='Khaki'), secondary_y=False)
    MI_fig.add_trace(go.Scatter(x=df_MI_mortality_rate['Month'], y=df_MI_mortality_rate['Value'], mode='lines',
                                 name='Летальность ОКС', marker_color='red', text=df_MI_mortality_rate['Value'],
                                 textposition='top center'),
                      secondary_y=True)
    MI_fig.update_layout(yaxis={'visible': False, 'showticklabels': False},
                         yaxis2={'visible': False, 'showticklabels': False})

    # График путь больного ОКС с подъемом ST
    ACS_with_elevation_ST_12_h_delivery = df.loc[(df['№ п/п'] == 34) &
                                                 (df['Date'].dt.to_period('Y') == year) &
                                                 (df['Date'].dt.month.isin(month_range)) &
                                                 (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_elevation_ST_12_h_PCI = df.loc[(df['№ п/п'] == '39.1.2.1') &
                                            (df['Date'].dt.to_period('Y') == year) &
                                            (df['Date'].dt.month.isin(month_range)) &
                                            (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_path_data = {'number': [ACS_with_elevation_ST, ACS_with_elevation_ST_12_h_delivery,
                                ACS_with_elevation_ST_12_h_PCI],
                     'stage': ['Всего', 'Доставлено за 12 часов', 'ЧКВ за 12 часов']}
    ACS_path_funnel_fig = px.funnel(ACS_path_data, x='number', y='stage', title='Путь больного с ОКСпST')

    # Кол-во умерших при ОКСпST
    cnt_deaths_ACS_with_eST = df.loc[(df['№ п/п'] == '44.1') &
                                     (df['Date'].dt.to_period('Y') == year) &
                                     (df['Date'].dt.month.isin(month_range)) &
                                     (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # Летальность при ОКСпST
    ACS_with_eST_mortality_rate = round(cnt_deaths_ACS_with_eST / ACS_with_elevation_ST, 3) if ACS_with_elevation_ST > 0 else 0

    # Летальность пациентов идеального пути при ОКСпST
    cnt_deaths_ACS_with_eST_ideal_path = df.loc[(df['№ п/п'] == '42.1.2.1') &
                                         (df['Date'].dt.to_period('Y') == year) &
                                         (df['Date'].dt.month.isin(month_range)) &
                                         (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_eST_ideal_path_mortality_rate = round(cnt_deaths_ACS_with_eST_ideal_path / ACS_with_elevation_ST, 3) if ACS_with_elevation_ST > 0 else 0

    # Доля умерших без реваскуляризации от всех пациентов с ОКСпST
    cnt_deaths_ACS_with_eST_CABG = df.loc[(df['№ п/п'] == '43.1.1') &
                                   (df['Date'].dt.to_period('Y') == year) &
                                   (df['Date'].dt.month.isin(month_range)) &
                                   (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_PCI = df.loc[(df['№ п/п'] == '42.1.2') &
                                  (df['Date'].dt.to_period('Y') == year) &
                                  (df['Date'].dt.month.isin(month_range)) &
                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_Thrombolysis = df.loc[(df['№ п/п'] == '42.1.4') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_deaths_ACS_with_eST_without_revasc = cnt_deaths_ACS_with_eST - cnt_deaths_ACS_with_eST_CABG - \
                                      cnt_deaths_ACS_with_eST_PCI - cnt_deaths_ACS_with_eST_Thrombolysis
    ACS_with_eST_without_revasc_deaths_part = \
        round(cnt_deaths_ACS_with_eST_without_revasc / cnt_deaths_ACS_with_eST, 3) if cnt_deaths_ACS_with_eST > 0 else 0

    # График ОКСбпST высокого и низкого риска
    cnt_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '47.2.1') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '47.2.2') &
                                           (df['Date'].dt.to_period('Y') == year) &
                                           (df['Date'].dt.month.isin(month_range)) &
                                           (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_with_eST_risk_fig = go.Figure(
        data=[
            go.Bar(x=['Высокий риск', 'Низкий риск'], y=[cnt_ACS_without_eST_high_risk, cnt_ACS_without_eST_low_risk],
                   text=[cnt_ACS_without_eST_high_risk, cnt_ACS_without_eST_low_risk],
                   textfont=dict(size=18, color="black"), marker_color=['#FFBAA0', '#8BDDB8']
                   )
        ])
    ACS_with_eST_risk_fig.update_layout(yaxis={'visible': False, 'showticklabels': False})

    # Охват ЧКВ при ОКСбпST высокого риска
    cnt_PTCA_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '39.1.1.1') &
                                                (df['Date'].dt.to_period('Y') == year) &
                                                (df['Date'].dt.month.isin(month_range)) &
                                                (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_PTCA_coverage = \
        round(cnt_PTCA_ACS_without_eST_high_risk / cnt_ACS_without_eST_high_risk, 3) \
            if cnt_ACS_without_eST_high_risk > 0 else 0

    # Летальность при ОКСбпST высокого риска
    cnt_deaths_ACS_without_eST_high_risk = df.loc[(df['№ п/п'] == '44.2.1') &
                                                  (df['Date'].dt.to_period('Y') == year) &
                                                  (df['Date'].dt.month.isin(month_range)) &
                                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_mortality_rate = \
        round(cnt_deaths_ACS_without_eST_high_risk / cnt_ACS_without_eST_high_risk, 3) \
            if cnt_ACS_without_eST_high_risk > 0 else 0

    # Охват ЧКВ при ОКСбпST низкого риска
    cnt_PTCA_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '39.1.1.2') &
                                                  (df['Date'].dt.to_period('Y') == year) &
                                                  (df['Date'].dt.month.isin(month_range)) &
                                                  (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_low_risk_PTCA_coverage = \
        round(cnt_PTCA_ACS_without_eST_low_risk / cnt_ACS_without_eST_low_risk, 3) \
            if cnt_ACS_without_eST_low_risk > 0 else 0


    # Летальность при ОКСбпST низкого риска
    cnt_deaths_ACS_without_eST_low_risk = df.loc[(df['№ п/п'] == '44.2.1') &
                                                 (df['Date'].dt.to_period('Y') == year) &
                                                 (df['Date'].dt.month.isin(month_range)) &
                                                 (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    ACS_without_eST_high_risk_mortality_rate = \
        round(cnt_deaths_ACS_without_eST_low_risk / cnt_ACS_without_eST_low_risk, 3) \
            if cnt_ACS_without_eST_low_risk > 0 else 0

    # Кол-во ОКС с шоком
    cnt_shock = df.loc[(df['№ п/п'] == '47.3') &
                       (df['Date'].dt.to_period('Y') == year) &
                       (df['Date'].dt.month.isin(month_range)) &
                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    # График шок
    cnt_shock_ACS_with_eST = df.loc[(df['№ п/п'] == '47.3.1') &
                                    (df['Date'].dt.to_period('Y') == year) &
                                    (df['Date'].dt.month.isin(month_range)) &
                                    (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    cnt_shock_ACS_without_eST = df.loc[(df['№ п/п'] == '47.3.2') &
                                       (df['Date'].dt.to_period('Y') == year) &
                                       (df['Date'].dt.month.isin(month_range)) &
                                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    part_shock_ACS_with_eST = round(cnt_shock_ACS_with_eST / cnt_shock, 3) if cnt_shock > 0 else 0
    part_shock_ACS_without_eST = round(cnt_shock_ACS_without_eST / cnt_shock, 3) if cnt_shock > 0 else 0
    Shock_fig = go.Figure(
        data=[
            go.Bar(name='Шок ОКСпST', y=[part_shock_ACS_with_eST], text=f'{part_shock_ACS_with_eST:.1%}',
                   marker_color='SteelBlue', textposition='inside'),
            go.Bar(name='Шок ОКСбпST', y=[part_shock_ACS_without_eST], text=f'{part_shock_ACS_without_eST:.1%}',
                   marker_color='PaleTurquoise', textposition='inside')
        ])
    Shock_fig.update_layout(barmode='stack', xaxis={'visible': False, 'showticklabels': False},
                            yaxis={'visible': False, 'showticklabels': False})
    '''
    textfont=dict(size=18, color="black"))
    '''

    # Охват ЧКВ у пациентов с шоком
    cnt_PTCA_for_shock = df.loc[(df['№ п/п'] == '39.1.3') &
                                (df['Date'].dt.to_period('Y') == year) &
                                (df['Date'].dt.month.isin(month_range)) &
                                (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    shock_PTCA_coverage = round(cnt_PTCA_for_shock / cnt_shock, 3) if cnt_shock > 0 else 0

    # Летальность при ОКС с шоком
    cnt_deaths_shock = df.loc[(df['№ п/п'] == '44.3') &
                              (df['Date'].dt.to_period('Y') == year) &
                              (df['Date'].dt.month.isin(month_range)) &
                              (df['Hospital'].isin(input_hospital)), 'Value'].sum()
    shock_mortality_rate = round(cnt_deaths_shock / cnt_shock, 3) if cnt_shock > 0 else 0

    # Доля пациентов с шоком от всех умерших при ОКС
    part_shock_for_deaths = round(cnt_deaths_shock / ACS_mortality_abs, 3) if ACS_mortality_abs > 0 else 0



    return total_ACS, ACS_with_elevation_ST, ACS_without_elevation_ST, ACS_fig, f'{PCI_coverage:.1%}', \
           f'{ACS_mortality_rate:.1%}', f'{MI_mortality_rate:.1%}', MI_fig, ACS_path_funnel_fig, \
           f'Умерших: {int(cnt_deaths_ACS_with_eST)}', f'Общая летальность при ОКСпST: {ACS_with_eST_mortality_rate:.1%}', \
           f'Летальность идеального пути: {ACS_with_eST_ideal_path_mortality_rate:.1%}', \
           f'Доля умерших без ЧКВ, АКШ и ТЛТ: {ACS_with_eST_without_revasc_deaths_part:.1%}', ACS_with_eST_risk_fig, \
           f'Охват ЧКВ: {ACS_without_eST_high_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', \
           f'Охват ЧКВ: {ACS_without_eST_low_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', Shock_fig, \
           f'Кол-во ОКС с шоком: {int(cnt_shock)}', f'Охват ЧКВ: {shock_PTCA_coverage:.1%}', \
           f'Летальность при шоке: {shock_mortality_rate:.1%}', \
           f'Доля пациентов с шоком среди всех умерших при ОКС {part_shock_for_deaths:.1%}'


if __name__ == '__main__':
    app.run_server(debug=True)
    print(dash.__version__)






'''
    Пример настройки дизайна графика
    ACS_fig.update_layout(bargap=0.2, yaxis={'visible': False, 'showticklabels': False}, template='plotly_white',
                          legend_title=None, legend={'font': {'size': 16, 'color': 'black'}, 'traceorder':'reversed'},
                          title={'font': {'size': 20, 'color': 'black'}})
'''

