import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import preprocess
from hover_template import get_hover_template

def init_figure_Compare(df):
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = px.line(df, x='Date et heure', y='kWh', color='Contrat')

    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['simple_white+Compare'],
        dragmode=False,
        barmode='relative',
        title="Consommation d'hydroélectricité en 2022",
        xaxis_title="Date",
        yaxis_title="Quantité (kWh)",
        xaxis_range=['2022-07-01', '2022-08-01'],
        legend_title=''
    )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e1dfde')
    return fig

def change_range(start, end, figure): 
    figure = go.Figure(figure)
    figure.update_layout(
        xaxis_range=[start, end]
    )
    return figure
    

def init_figure_Toggle():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = px.line([])

    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['simple_white+Toggle'],
        dragmode=False,
        title="Consommation moyenne d'hydroélectricité selon la température",
        xaxis_title="Température",
        yaxis_title="Quantité moyenne (kWh)"
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e1dfde')

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
    tenant_data, homeowner_data = preprocess.get_separate_data(data)
    tenant_avg, homeowner_avg = preprocess.avg_consumption_per_temp(tenant_data, homeowner_data)
    
    if mode == 'Locataire':
        data = tenant_avg
        hover_text = "%{y:.2f}"
    else: 
        data = homeowner_avg
        hover_text = "%{y:.2f}"
    
    fig.data = []
        
    fig.add_trace(go.Scatter(
        x=data['Température moyenne (°C)'], 
        y=data['kWh'],
       #hovertemplate = get_hover_template(data['Contrat'],mode).format(name=data['Contrat'], mode=hover_text)
       ))
        
    return fig
