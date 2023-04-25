
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
            edit and adapted by Team 17 for Final Project
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL

import pandas as pd
from dash.exceptions import PreventUpdate

import preprocess
import bar_chart
import line_chart

from template import create_template
from constant import MODES, MODES_UNITS
from datetime import date


app = dash.Dash(__name__)
server = app.server
app.title = 'Projet | INF8808'


def prep_data():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    return


def init_app_layout(figLineChartCompare,figLineChartToggle,figBarChartSeason,figBarChartDays, figLineChartHour):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    navBarSection = [
        {'key': 'Accueil', 'id': '#home'},
        {'key': 'Lieux de résidence', 'id': '#residence'},
        {'key': 'Température', 'id': '#temperature'},
        {'key': 'Saisons', 'id': '#season'},
        {'key': 'Jour de la semaine', 'id': '#day'},
        {'key': 'Heure de la journée', 'id': '#time'}
    ]
    return html.Div(className='content', children=[
        html.Nav([
            html.A(section['key'], href=section['id'], className='navigation-button')
            for section in navBarSection
        ], className='navbar ', id='navbar'),
        html.Main(children=[
        html.Header(id='home', children=[
            html.H1('Consommation énergétique d’habitants de la province de Québec')
        ]),
            html.Div(className='welcome', children=[
                html.P(
                    """
                    La province du Québec est l’un des plus grands producteurs d’électricité au Canada avec un tiers 
                    de la totalité de la génération d’électricité produite par celle-ci. En effet, le Québec dispose de 
                    nombreuses sources d'hydroélectricité, avec 130 000 rivières et ruisseaux entourant la région et contenant 
                    environ 40% de l'eau du Canada. Il n’est donc pas étonnant de constater les taux peu élevés que propose Hydro-Québec : 
                    6,319 sous pour les premiers 40 kilowattheures d’une journée pour les habitants de la catégorie “Rate D”, soit le tarif 
                    pour les consommateurs résidentiels ou agricoles. Il est connu que les tarifs d'Hydro-Québec sont bas, mais il serait intéressant 
                    d’observer s’il y a de grandes variations en termes de consommation électrique lorsqu'on est locataire de son appartement ou propriétaire 
                    d'un condo pour différents étudiants universitaires de la région de Montréal. Surtout depuis la pandémie, plusieurs travaillent à distance ou 
                    ont des cours en ligne. Il serait donc intéressant de voir s'il y a des différences de consommation électrique.
                    """
                ),
                html.Img(src='/assets/manic.jpg', width='70%')

            ]),
            html.Div(className='text section', id='residence', children=[
                html.H2("Est-ce que le lieu de résidence affecte la consommation électrique des québécois?"),
                html.P(
                """
                        Le graphique ci-dessous représente la consommation d'hydroélectricité de juin 2022 à février 2023 d'un propriétaire
                        habitant à Laval et d'un locataire habitant à Montréal en fonction de la date et de l'heure de la journée. D'après ce graphique, 
                        il semble que le propriétaire habitant à Laval consomme beaucoup plus d'énergie que le locataire habitant à Montréal. Ces données 
                        suggèrent donc que, en moyenne, un locataire dépense moins d'électricité qu'un propriétaire tout au long de l'année et qu'un habitant
                        de Laval dépense plus en électricité qu'un habitant de Montréal. Cependant, il est important de noter que ces conclusions sont basées
                        sur les données de seulement deux individus, donc elles ne sont pas nécessairement représentatives de l'ensemble de la population. La 
                        différence de consommation électrique entre les deux personnes pourrait être influencée par des facteurs externes, tels que le coût de 
                        l'électricité dans leur région, la taille de leur domicile et le nombre de personnes qui y vivent, ainsi que leur comportement de consommation d'énergie.
                """),

            ],),
            html.Div(className='viz-container', children=[
                dcc.DatePickerRange(
                    id='dates',
                    min_date_allowed=date(2022, 6, 7),
                    max_date_allowed=date(2023, 2, 21),
                    initial_visible_month=date(2022, 7, 1),
                    start_date=date(2022, 7, 1),
                    end_date=date(2022, 8, 1)
                    ),
                dcc.Graph(
                    figure=figLineChartCompare,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='line-chart-compare'
                )
            ]),
            html.Div(className='text section', id='temperature', children=[
                html.H2("Comment la température affecte la consommation d'électricité des québécois?"),
                html.P("""Cette visualisation nous montre la consommation moyenne d'hydroélectricité du propriétaire et du locataire selon la température. 
                           Comme on peut le constater dans le graphique en allant mettre le curseur sur les points, la plus grande moyenne d'énergie 
                           consommée par le propriétaire se situe à -24 °C, alors que pour le locataire, sa plus grande moyenne de consommation énergétique 
                           se situe la température est à 31 °C. Normalement, en hiver, on s'attend à voir une plus grande consommation d'électricité à cause 
                           du chauffage, il est normal que le propriétaire dépenses plus l'hiver, mais le fait que le locataire ne suit pas cette tendance nous
                            force à demander la raison de cette inconsistance. Pour notre cas, le locataire ne paye pas son chauffage, alors une grande partie
                            de la différence  consommation entre le propriétaire et le locataire de cela.
                """),
            ],),
            html.Div(className='viz-container', children=[
                
                dcc.Graph(
                    figure=figLineChartToggle,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='line-chart-toggle'
                ),
                 html.Div(children=[
                    dcc.RadioItems(
                        id='radio-items',
                        options=[
                             dict(
                                label=MODES['homeowner'],
                                value=MODES['homeowner']),
                            dict(
                                label=MODES['tenant'],
                                value=MODES['tenant']),
                        ],
                        value=MODES['homeowner']
                    )
                ]),
            ]),
            html.Div(className='text section', id='season', children=[
                html.P(
                    """
                    Une autre façon de visualiser les données selon la température est d'utiliser les saisons, chacune étant marquée par un 
                    climat particulier. Nous avons donc calculé la consommation moyenne en 1 h pour chaque saison. En regardant le diagramme 
                    à barre qui suit, on constate sans surprise que l'hiver coûte beaucoup plus cher aux Québécois en électricité, étant donné 
                    que c'est la saison la plus froide. Suivant le même raisonnement, l'automne serait la prochaine saison en termes de consommation
                      électrique. Par contre, ce qui est surprenant, nous consommons plus en été, bien que ce soit la saison la plus chaude. Une explication 
                      possible serait l'utilisation de l'air climatisé, qui ne serait pas utilisé au printemps.
                    """
                        )
            ],),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figBarChartSeason,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='bar-chart-season'
                )
            ], id='main'),
            html.Div(className='text section', id='day', children=[
                html.H2("Quelle est la consommation électrique d'une personne au cours de la journée?"),
                html.P(
                    """Le graphique suivant nous renseigne sur la consomation moyenne d'un utilsateur dans sa semaine, afin de prendre en compte les données de nos 2 types 
                    d'utilisateurs, locataire et propriétaire. La première chose que nous constatons est que les jours de fin de semaine indiquent une plus grande consommation
                      électrique, ce qui n'est pas tant surprenant étant donnée que nous sommes plus souvent à la maison durant la fin de semaine. On constate aussi que bien 
                      que la consommation soit plus grande le jour, cette différence n'est pas aussi marqué qu'on pourrait le croire (à peine le double), probablement à cause 
                      du chauffage nécessaire pour chauffer l'habitat pendant la nuit. Finalement, on peut voir que la consommation durant la journéeest relativement stable
                        d'une journée à l'autre, restant entre 12kWh et 14kWh."""
                        )
            ],),
            
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figBarChartDays,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='bar-chart-day'
                ),
            ]),
            html.Div(className='text section', id='time', children=[
                html.P(
                    """
                    Nous terminons cette page en plongeant davantage et en observant la consommation électrique moyenne d'un propriétaire au cours 
                    d'une journée. On constate un énorme pic à minuit. En temps normal, on ne devrait pas consommer autant pendant la nuit. Il est 
                    important de mentionner que nous n'avons qu'un seul propriétaire, et qu'il travaille de nuit, cela pourrait donc expliquer les 
                    données. Sinon, on constate un autre pic en plein milieu de la journée, à midi, qui semble beaucoup plus naturel. Pour ce qui est du
                      locataire, il est tout aussi actif la nuit. Considérant que nous sommes en classe la journée et qu'il étudie très tard le soir, il 
                      n'y a rien de surprenant.
                    """
                        ),
            ],),
            html.Div(className='viz-container', id='padding', children=[
                dcc.Graph(
                    figure=figLineChartHour,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='line-chart-hour'
                ),
                html.Div(children=[
                    dcc.RadioItems(
                        id='radio-items2',
                        options=[
                             dict(
                                label=MODES['homeowner'],
                                value=MODES['homeowner']),
                            dict(
                                label=MODES['tenant'],
                                value=MODES['tenant']),
                        ],
                        value=MODES['homeowner']
                    )
                ]),
            ]),
            html.Div(className="end")
        ]),
    ])

@app.callback(
    [Output('line-chart-toggle', 'figure')],
    [Input('radio-items', 'value')],
    [State('line-chart-toggle', 'figure')]
)
def radio_updated(mode, figure):
    '''
        Updates the application after the radio input is modified.

        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            new_fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    # TODO : Update the figure's data and y axis, as well as the informational
    # text indicating the mode
    new_fig = figure
    new_fig = line_chart.draw(new_fig, my_df, mode, MODES_UNITS['temp'])
    return [new_fig]

@app.callback(
    [Output('line-chart-hour', 'figure')],
    [Input('radio-items2', 'value')],
    [State('line-chart-hour', 'figure')]
)
def radio_updated2(mode, figure):
    '''
        Updates the application after the radio input is modified.

        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            new_fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    # TODO : Update the figure's data and y axis, as well as the informational
    # text indicating the mode
    new_fig = figure
    new_fig = line_chart.draw(new_fig, my_df, mode, MODES_UNITS['hour'])
    return [new_fig]

@app.callback(
    Output('line-chart-compare', 'figure'),
    Input('dates', 'start_date'),
    Input('dates', 'end_date'),
    State('line-chart-compare', 'figure')
    )
def update_dates(start_date, end_date, figure):
    new_fig = figure
    if start_date is not None and end_date is not None:
       return line_chart.change_range(start_date, end_date, new_fig)
    
    return new_fig

# @app.callback(
#     Output('bar-chart-season', 'figure'),
#     Input('bar-chart-season', 'hoverData'),
#     State('bar-chart-season', 'figure'))
# def changeOpacity(hoverData, figure):
#     new_fig = figure
#     if hoverData is not None:
#         index = new_fig['data'][0]['x'].index(hoverData['points'][0]['x'])
#         new_fig['data'][0]['marker']['opacity'] = [0.4] * 4
#         new_fig['data'][0]['marker']['opacity'][index] = 1
#     else:
#         new_fig['data'][0]['marker']['opacity'] = [1] * 4
    
#     return new_fig

# @app.callback(
#     Output('bar-chart-day', 'figure'),
#     Input('bar-chart-day', 'hoverData'),
#     State('bar-chart-day', 'figure'))
# def changeOpacity(hoverData, figure):
#     new_fig = figure
#     if hoverData is not None:
#         index = new_fig['data'][0]['x'].index(hoverData['points'][0]['x'])
#         new_fig['data'][0]['marker']['opacity'] = [0.4] * 7
#         new_fig['data'][0]['marker']['opacity'][index] = 1
#         new_fig['data'][1]['marker']['opacity'] = [0.4] * 7
#         new_fig['data'][1]['marker']['opacity'][index] = 1
#     else:
#         new_fig['data'][0]['marker']['opacity'] = [1] * 7
    
#     return new_fig

data = prep_data()
my_df = preprocess.read_data()
season_df = preprocess.group_by_season(my_df)
day_df = preprocess.group_days(my_df)
night_df = preprocess.group_nights(my_df)

create_template()
fig_Compare = line_chart.init_figure_Compare(my_df)
fig_Toggle = line_chart.init_figure_Toggle()
fig_Toggle = line_chart.draw(fig_Toggle, my_df, MODES['homeowner'], MODES_UNITS['temp'])
fig_Season = bar_chart.init_figure_Season(season_df)
fig_Days = bar_chart.init_figure_Days(day_df, night_df)
fig_hour = line_chart.init_figure_Toggle()
fig_hour = line_chart.draw(fig_hour, my_df, MODES['homeowner'], MODES_UNITS['hour'])

app.layout = init_app_layout(fig_Compare,fig_Toggle,fig_Season,fig_Days, fig_hour)
preprocess.filter(my_df)

