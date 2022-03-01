from enum import Enum
import requests
import json
from bs4 import BeautifulSoup
import dash_bootstrap_components as dbc
from dash import html

class SiteStatus(Enum):
    OK = 1
    LENTO = 2
    INDISPONIVEL = 3


def check_site(site):
    try:
        site_response = requests.get(site.get('url'), timeout=site.get('timeout',3))

        soup = BeautifulSoup(site_response.text, 'html.parser')

        if (not site['title'].upper() in soup.title.text.upper()):
            raise Exception('Titulo da pagina não encontrado')

        status = SiteStatus.OK
        if (site_response.elapsed.total_seconds() > 3):
            status = SiteStatus.LENTO

        return {
            'site': site,
            'status': status,
        }

    except Exception as e:
        return {
            'site': site,
            'status': SiteStatus.INDISPONIVEL,
            'msg': str(e),
        }


def card_result(result):

    badget_status = dbc.Badge("Erro/Timeout", color="danger", className="me-1")

    if result['status'] == SiteStatus.OK:
        badget_status = dbc.Badge("Disponivel", color="success", className="me-1")
    elif result['status'] == SiteStatus.LENTO:
        badget_status = dbc.Badge("Lento", color="warning", className="me-1")

    return dbc.Col(
        dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(result['site']['nome'], className="card-title"),
                    badget_status,
                    html.Hr(className="my-2"),
                    dbc.CardLink("Visitar Site", href=result['site']['url']),
                ]
            ),
        ]
    ), md=2)


if __name__ == '__main__':
    site = {}
    with open('sites.json', 'r') as file:
        sites = json.loads(file.read())
        for site in sites:
            print(check_site(site))

