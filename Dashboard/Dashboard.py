from dash import Dash, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import flask
import dash_auth

from Dashboard.Navigation import tabs_navigator_offcanvas
from Dashboard.Calculations_p1 import choose_hospital_ASC
from Dashboard.Filters_p1 import sidebar
from Dashboard.Content_p1 import content


VALID_USERNAME_PASSWORD_PAIRS = {
    'user_42': '1234',
    'Sysoev_SA': '1234'
}

server = flask.Flask(__name__)
app = Dash(name=__name__, 
           server=server, 
           title='test_BI_app', 
           external_stylesheets=[dbc.themes.BOOTSTRAP])

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(
    #style={'backgroundColor': colors['background']},
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

# Development server
# if __name__ == '__main__':
#     app.run_server(host='0.0.0.0', debug=True, port=8050)
