
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
from dash.dependencies import Input, Output, State

import pandas as pd

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
    # dataframe = pd.read_csv('./assets/data/romeo_and_juliet.csv')

    # proc_data = preprocess.summarize_lines(dataframe)
    # proc_data = preprocess.replace_others(proc_data)
    # proc_data = preprocess.clean_names(proc_data)

    # return proc_data
    return


def init_app_layout(figLineChartCompare,figLineChartToggle,figBarChartSeason,figBarChartDays, figLineChartHour):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Équipe 17'),
            html.H2('Consommation énergétique d’habitants de la province de Québec')
        ]),
        html.Main(children=[
            html.Div(className='text', children=[
                html.H2("Est-ce que le lieu de résidence affecte la consommation électrique des québécois ?"),
                html.H3("""Le graphique suivant montre la consommation d'hydroélectricité de juin 2022 à février 2023 d'un propriétaire habitant à Laval et d'un locataire habitant
                         à Montréal selon la date et l'heure de la journée. On voit alors ici que le propriétaire habitant à Laval semble consommer 
                         beaucoup plus d'énergie que le locataire habitant à Montréal. On peut donc dire que selon nos données, un locataire dépenses 
                         moins d'électricité qu'un propriétaire pendant presque toute l'année et un habitant de Laval dépenses plus en électricité 
                         qu'un habitant de Montréal au courant de l'année. Cependant, vu que l'on a seulement les données pour 2 individus, la fiabilité 
                         de nos réponses n'est pas certaine. La raison d'une telle différence de consommation électrique est probablement liée à des valeurs 
                         externes comme ce que le locataire paie et ne paie pas de sa facture électrique, la différence de grandeur ou le nombre de personnes 
                         qui vivent dans la résidence.
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
            html.Div(className='text', children=[
                html.H2("Comment la température affecte la consommation d'électricité des québécois?"),
                html.H3("""Cette visualisation nous montre la consommation moyenne d'hydroélectricité du propriétaire et du locataire selon la température. 
                            Comme on peut le constater dans le graphique en allant mettre le curseur sur les points, la plus grande moyenne d'énergie consommée 
                            du propriétaire se situe à -24 °C, alors que pour le locataire, sa plus grande moyenne de consommation énergétique se situe quand 
                            la température est à 31 °C. Normalement, en hiver on s'attend à voir une plus grande consommation d'électricité à cause du chauffage, 
                            alors il est normal que le propriétaire dépenses plus l'hiver, mais le fait que le locataire ne suit pas cette tendance nous force à se
                            demander la raison de cette inconsistance. Pour notre cas, le locataire ne payes pas son chauffage, alors une grande partie de la différence 
                            de consommation entre le propriétaire et le locataire est à cause de cela.
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
            html.Div(className='text', children=[
                html.H3(
                    """
                    Une autre façon de visualiser les données selon la température est d'utiliser les saisons,
                      chacune étant marqué par un climat particulier. Nous avonc donc calculer la consommation moyenne en 1h pour chaque saison. En regardant le diagramme à barre qui suit,
                        on constate sans surprise que l'hiver coûte beaucoup plus cher aux québecois en électricité, étant donné que c'est la saison la plus froide.
                        Suivant le même raisonnement, l'automne serait la prochaine saison en terme de consommation électrique. 
                        Par contre, ce qui est surprenant, nous consommons plus en été, bien que ce soit la saison la plus chaude. Une explication possible
                        serait l'utilisation de l'air climatisée, qui ne serait pas utiliser au printemps.
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
            html.Div(className='text', children=[
                html.H2("Quel est la consommation électrique d'une personne au cours de la journée?"),
                html.H3(
                    """Le graphique suivant nous renseigne sur la consomation moyenne d'un utilsateur dans sa semaine, 
                        afin de prendre en compte les données de nos 2 types d'utilisateurs, locataire et propriétaire. 
                        La première chose que nous constatons est que les jours de fin de semaine indiquent une plus grande consommation électrique,
                          ce qui n'est pas tant surprenant étant donnée que nous sommes plus souvent à la maison durant la fin de semaine. 
                          On constate aussi que bien que la consommation soit plus grande le jour, cette différence n'est pas aussi marqué qu'on pourrait le croire (à peine le double), probablement à cause du 
                          chauffage nécessaire pour chauffer l'habitat pendant la nuit. Finalement, on peut voir que la consommation durant la journée
                          est relativement stable d'une journée à l'autre, restant entre 12kWh et 14kWh."""
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

            html.Div(className='text', children=[
                html.H3(
                    """
                    Nous terminons cette page en plongeant davantage et en observant la consommation électrique moyenne d'un utilisateur
                      au cours d'une journée. On constate un énorme pic à minuit. En temps normal, on ne devrait pas consommer autant pendant la nuit.
                     Il est important de mentionner que nous n'avons pas beaucoup d'utilisateur, et que l'un d'entre eux travaille de nuit, 
                     cela pourrait donc expliquer les données. Sinon, on constate un autre pic en plein milieu de la journée,
                       à midi, qui semble beaucoup plus naturel.
                    """
                        )
            ],),
            html.Div(className='viz-container', children=[
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

@app.callback(
    Output('bar-chart-season', 'figure'),
    Input('bar-chart-season', 'hoverData'),
    State('bar-chart-season', 'figure'))
def changeOpacity(hoverData, figure):
    new_fig = figure
    if hoverData is not None:
        index = new_fig['data'][0]['x'].index(hoverData['points'][0]['x'])
        new_fig['data'][0]['marker']['opacity'] = [0.4] * 4
        new_fig['data'][0]['marker']['opacity'][index] = 1
    else:
        new_fig['data'][0]['marker']['opacity'] = [1] * 4
    
    return new_fig

@app.callback(
    Output('bar-chart-day', 'figure'),
    Input('bar-chart-day', 'hoverData'),
    State('bar-chart-day', 'figure'))
def changeOpacity(hoverData, figure):
    new_fig = figure
    if hoverData is not None:
        index = new_fig['data'][0]['x'].index(hoverData['points'][0]['x'])
        new_fig['data'][0]['marker']['opacity'] = [0.4] * 7
        new_fig['data'][0]['marker']['opacity'][index] = 1
        new_fig['data'][1]['marker']['opacity'] = [0.4] * 7
        new_fig['data'][1]['marker']['opacity'][index] = 1
    else:
        new_fig['data'][0]['marker']['opacity'] = [1] * 7
    
    return new_fig

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

