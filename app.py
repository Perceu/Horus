from ctypes import cast
import json
import dash_bootstrap_components as dbc
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from monitor import check_site, card_result
from decouple import config

app = Dash('Monitoramento dos sites', external_stylesheets=[dbc.themes.BOOTSTRAP])

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Dash de monitoramento", className="display-3"),
            html.P(
                "Use o json do projeto para registrar cada site a ser monitorado!",
                className="lead",
            ),
            html.Hr(className="my-2"),
            dbc.Badge("Disponivel", color="success", className="me-1"),
            dbc.Badge("Lento", color="warning", className="me-1"),
            dbc.Badge("Erro/Timeout", color="danger", className="me-1"),
            html.Hr(className="my-2"),
            dbc.Button('Verificar Sites', id='refresh'),
            dcc.Interval(
                id='interval-component',
                interval=60*1000, # in milliseconds
                n_intervals=0
            )
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 mb-3 bg-light rounded-3",
)


@app.callback(
    Output('sites', 'children'),
    Input('refresh', 'n_clicks'),
    Input('interval-component', 'n_intervals')
)
def update_output(n_clicks, n_intervals):

    site = {}
    with open('sites.json', 'r') as file:
        sites = json.loads(file.read())
        
    results = []
    for site in sites['sites']:
        card = card_result(check_site(site))
        results.append(card)

    return results

app.layout = dbc.Container(
    [
        jumbotron,
        dbc.Row(id='sites')
    ]
)

app.run_server(debug=config('DEBUG', default=False, cast=bool))