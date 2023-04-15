import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import preprocess
from hover_template import get_hover_template
import hover_template as hover

def init_figure_Compare(df):
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = px.line(df, x='Date et heure', y='kWh', color='Contrat', custom_data=['Contrat', 'Date et heure', 'kWh'])

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
    fig.update_traces(hovertemplate=hover.get_compare_template())
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
    #fig.update_traces(hovertemplate=hover.get_toggle_template())

    return fig

def draw(fig, data, mode, mode_unit):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    print(mode_unit)
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode
    tenant_data, homeowner_data = preprocess.get_separate_data(data)
    tenant_avg_temp, homeowner_avg_temp = preprocess.avg_consumption_per_temp(tenant_data, homeowner_data)
    tenant_avg_hour, homeowner_avg_hour = preprocess.avg_consumption_per_hour(tenant_data, homeowner_data)
    
    fig.data = []
    if mode_unit == 'Température':
        fig.update_layout(
        title="Consommation moyenne d'hydroélectricité selon la température",
        xaxis_title="Température",
        yaxis_title="Quantité moyenne (kWh)",
        xaxis_range=[-29, 32],
        )
        if mode == 'Locataire':
            data = tenant_avg_temp
        else:
            data = homeowner_avg_temp
    else: 
        fig.update_layout(
        title="Consommation moyenne d'hydroélectricité selon l'heure",
        xaxis_title="Heure",
        yaxis_title="Quantité moyenne (kWh)",
        xaxis_range=['00', '23'],
        )
        if mode == 'Locataire':
            data = tenant_avg_hour
        else:
            data = homeowner_avg_hour
    
    #print(fig.layout)
        
    columns = data.columns
    print(columns)
    print(data)
    fig.add_trace(go.Scatter(
        x=data[columns[0]], 
        y=data[columns[1]],
       ))
    fig.update_traces(hovertemplate = hover.get_toggle_template(mode_unit))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e1dfde')
    #fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e1dfde')
    #print(fig.data[0])
        
    return fig
