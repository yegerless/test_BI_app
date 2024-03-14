import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc

from Novgorod.Parsing_data import df

months_dict = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
               7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}


'Visual elements with filters'
# Карточка-фильтр с выбором года
year_choice_card = dbc.Card(
    children=[
        dbc.CardHeader('Выберите год отчета', className='card-filter_header_1'),
        dbc.CardBody(dcc.RadioItems(options=['2022', '2023', '2024'], value='2023', id='year_choice'))
    ],
    className='card-filter_1')

# Карточка-фильтр с выбором стационара
hospital_choice_card = dbc.Card(
    children=[
        dbc.CardHeader('Выберите стационар', className='card-filter_header_1'),
        dbc.CardBody(dcc.Checklist(options=df.Hospital.unique(), value=df.Hospital.unique(), id='hospital_choice',
                                   style={'font-size': 15}))
    ],
    className='card-filter_1')

# Слайдер с фильтром по месяцам
months_slider = html.Div(
    children=[
        dcc.RangeSlider(min=1, max=12, step=1, marks=months_dict, value=[1, 12], allowCross=False, id='month_choice',
                        vertical=True)
    ],
    #className='month_slider_1',
    style={'width': '25%',
           'justify-content': 'center', 'margin': '0 auto', 'align-items': 'center', 'vertical-align': 'center'
           #'padding': '100'
           }
)



'Sidebar'
sidebar = html.Div(
    className='sidebar_1',
    children=[
        # Горизонтальная линия, которая отделяет кнопку навигации
        html.Hr(),

        # Заголовок блока с фильтрами
        html.Div(children=['Фильтрация данных'], className='header_2'),

        # Горизонтальная линия, которая отделяет блок с фильтрами от заголовка
        html.Hr(),

        # Фильтр по году
        year_choice_card,
        #html.Div(children=[year_choice_card]), #, style={'display': 'inline-block', 'vertical-align': 'top'}),

        # Фильтр по стационару
        hospital_choice_card,

        # Фильтр с выбором месяцев
        months_slider
    ]
)