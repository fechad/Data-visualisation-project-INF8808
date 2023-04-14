
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
from constant import MODES
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


def init_app_layout(figLineChartCompare,figLineChartToggle,figBarChartSeason,figBarChartDays):
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
                html.H3("Description Line chart Compare"),
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
                html.H3("Description Line chart Toggle"),
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
                ])
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
            ]),
            
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
                )
            ])
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
    new_fig = line_chart.draw(new_fig, my_df, mode)
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

data = prep_data()
my_df = preprocess.read_data()
season_df = preprocess.group_by_season(my_df)
day_df = preprocess.group_days(my_df)
night_df = preprocess.group_nights(my_df)

create_template()
fig_Compare = line_chart.init_figure_Compare(my_df)
fig_Toggle = line_chart.init_figure_Toggle()
fig_Toggle = line_chart.draw(fig_Toggle, my_df, MODES['homeowner'])
fig_Season = bar_chart.init_figure_Season(season_df)
fig_Days = bar_chart.init_figure_Days(day_df, night_df)

app.layout = init_app_layout(fig_Compare,fig_Toggle,fig_Season,fig_Days)
preprocess.filter(my_df)

