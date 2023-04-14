'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

from hover_template import get_hover_template

def init_figure_Season(df):
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = px.bar(df, x='Saison', y='kWh')


    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['simple_white+Season'],
        dragmode=False,
        barmode='relative',
        title="Consommation d'hydroélectricité à travers les saisons",
        xaxis_title="Saison",
        yaxis_title="Quantité moyenne (kWh)"
    )

    return fig

def init_figure_Days():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = px.bar([])


    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['simple_white+Days'],
        dragmode=False,
        barmode='relative',
        title="Consommation moyenne d'hydroélectricité dans une semaine",
        xaxis_title="Jour de la semaine",
        yaxis_title="Quantité (Kwh)"
    )

    return fig

def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode

    if mode == 'Count':
        mode_chosen = 'PlayerLine'
        hover_text = "%{y} lines"
    else: 
        mode_chosen = 'PlayerPercent'
        hover_text = "%{y:.2f} % of lines"
    
    fig.data = []
    players = data.groupby("Player")
    
    for player in players:
        playerdf = player[1] # Get the dataframe 0 is index of group and 1 is Dataframe
        acts = playerdf['Act']
        xLabel = acts.transform(lambda x: 'Act '+ str(int(x)))
        
        fig.add_trace(go.Bar(
            x=xLabel, 
            y=playerdf[mode_chosen],
            name=player[0],
            hovertemplate = get_hover_template(player[0],mode).format(name=player[0], mode=hover_text)))
        
    return fig
