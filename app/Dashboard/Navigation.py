from dash import html
import dash_bootstrap_components as dbc


tabs_navigator_offcanvas = html.Div(
    children=[
        dbc.Button(
            children=['Навигация по приложению'],
            id='Tabs_navigator_open_button',
            n_clicks=0,
            className='nav_button_1',
            style={'margin-top': '20px', 'margin-left': '30px'},
        ),
        dbc.Offcanvas(
            children=[
                html.P(
                    '''Здесь будут кнопки со ссылками на все страницы приложения.
                    
                    Сейчас вы можете видеть пример как будут выглядеть эти кнопки (на данный момент они не работают).'''
                ),
                dbc.ListGroup(
                    children=[
                        dbc.ListGroupItem('Домашняя страница'),
                        dbc.ListGroupItem('Мониторинг ОКС'),
                        dbc.ListGroupItem('Какая-то страница №1'),
                        dbc.ListGroupItem('Какая-то страница №2'),
                        dbc.ListGroupItem('Какая-то страница №3'),
                        dbc.ListGroupItem('Какая-то страница №4'),
                        dbc.ListGroupItem('Какая-то страница №5'),
                        dbc.ListGroupItem('Какая-то страница №6'),
                        dbc.ListGroupItem('Какая-то страница №7'),
                        dbc.ListGroupItem('Какая-то страница №8'),
                        dbc.ListGroupItem('Какая-то страница №9'),
                        dbc.ListGroupItem('Какая-то страница №10'),
                        dbc.ListGroupItem('Контакты для обратной связи')
                    ]
                )
            ],
            id='Tabs_navigator',
            title='Вкладки аналитической панели',
            placement='start',
            backdrop=False,
            scrollable=True,
            is_open=False,
            style={'width': '15%', 'background-color': 'Azure'}
        )
    ],
    style={'position': 'fixed', 'width': '15%'}
)