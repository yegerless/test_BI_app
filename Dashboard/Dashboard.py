from dash import Dash, html, callback, Output, Input, State
import dash_bootstrap_components as dbc

from Calculations_p1 import choose_hospital_ASC
from Filters_p1 import sidebar
from Content_p1 import content



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



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {'background': '#FFFFFF', 'text': '#000000'}

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, #'width': 1820, 'height': 720},
    children=[
        sidebar,
        tabs_navigator_offcanvas,
        content
    ]
)


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
def intermediate_function(*args, **kwargs):
    return choose_hospital_ASC(*args, **kwargs)


@callback(
    Output(component_id='Tabs_navigator', component_property='is_open'),
    Input(component_id='Tabs_navigator_open_button', component_property='n_clicks'),
    [State("Tabs_navigator", "is_open")],
)
def open_tabs_navigator(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
