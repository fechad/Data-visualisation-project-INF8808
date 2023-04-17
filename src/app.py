
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
            html.Div(className='viz-container', children=[
                html.H3("Le graphique suivant montre la consommation d'hydroélectricité en 2022 d'un propriétaire habitant à Laval et d'un locataire habitant à Montréal selon la date et l'heure de la journée. Le line chart nous permet ici de comparer la consommation en kWh des 2 individus pour une date et heure donnée, ce qui nous permet directement de répondre aux questions suivantes:"),
                html.H3("- Est-ce qu’il existe une grande différence entre un propriétaire et un locataire sur la consommation électrique au cours d’une année?"),
                html.H3("- Y-a-t-il une différence de consommation entre les gens habitant en banlieue et ceux à Montréal au cours d’une année?"),
                html.H3("On voit alors ici que le propriétaire habitant à Laval semble consommer beaucoup plus d'énergie que le locataire habitant à Montréal. On peut donc dire que selon nos données, un locataire dépenses moins d'électricité qu'un propriétaire pendant presque toute l'année et un habitant de Laval dépenses plus en électricité qu'un habitant de Montréal au courant de l'année. Cependant, pour être certain de ses réponses, plus de données venant d'autres personnes seraient nécessaires."),
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
            
            html.Div(className='viz-container', children=[
                html.H3("En premier temps, cette visualisation nous montre la consommation moyenne d'hydroélectricité du propriétaire et du locataire selon la température. le line chart nous permet de facilement répondre à la question suivante: "),
                html.H3("- À quelle température atteint-on un pic de consommation électrique?"),
                html.H3("Comme on peut le constater dans le graphique en allant mettre le curseur sur les points, la plus grande moyenne d'énergie consommée du propriétaire se situe à -24 °C, alors que pour le locataire, sa plus grande moyenne de consommation énergétique se situe quand la température est à 31 °C. Plusieurs raisons peuvent influence ces résultats, alors il nous faudrais plus d'information pour savoir la raison de cette différence entre les 2 individus."),
                html.H3("Dans un deuxième temps, le graphique nous permet de changer l'axe vertical pour l'heure de la journée plutôt que la température. Ce line chart nous permet alors de répondre à la question suivante: "),
                html.H3("- À quelle température atteint-on un pic de consommation électrique?"),
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
            
            html.Div(className='viz-container', children=[
                html.H3("Description Bar chart Season"),
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
                html.H1("Quel est la consommation électrique d'une personne au cours de la journée?"),
                html.H1(
        "Le graphique suivant nous renseigne sur la consomation moyenne d'un utilsateur dans sa semaine, afin d'atténuer les effets des données extrêmes et de montrer une utilisation "
        )
            ],),
            
            html.Div(className='viz-container', children=[
                html.H3("Description Bar chart Days"),
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
            html.Div(className='viz-container', children=[
                html.H3("Description"),
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

