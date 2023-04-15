'''
    Provides the template for the hover tooltips.
'''
import constant as modes


def get_hover_template(name, mode):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * A title stating player name with:
                - Font family: Grenze Gotish
                - Font size: 24px
                - Font color: Black
            * The number of lines spoken by the player, formatted as:
                - The number of lines if the mode is 'Count ("X lines").
                - The percent of lines fomatted with two
                    decimal points followed by a '%' symbol
                    if the mode is 'Percent' ("Y% of lines").

        Args:
            name: The hovered element's player's name
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''
    # TODO: Generate and return the hover template
 
    return "<b style='font-family: Grenze Gotisch;font-size: 24px; color: black'> {name} </b> <br><br> " + "{mode} <extra></extra>"

def get_season_template():
    return "<b style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Saison : %{x}</b>" \
            "<br style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Consommation moyenne par heure : %{y} kWh" \
            " <extra></extra>"

def get_week_template(time):
    return " " + time + "<br> <b>%{x}</b> <br> " + "%{y:.2f} kWh <extra></extra>"

def get_compare_template():
    return "<b style='font-family: Grenze Gotisch;font-size: 24px; color: black'> %{customdata[0]} </b>" + \
        "<br style='font-family: Grenze Gotisch;font-size: 24px; color: black'> %{customdata[1]}" \
        "<br style='font-family: Grenze Gotisch;font-size: 24px; color: black'> %{customdata[2]} kWh" \
        " <extra></extra>"

def get_toggle_template(mode_unit):
    if(mode_unit == 'Température'):
        return "<b style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Température :  %{x} °C</b>" \
            "<br style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Consommation moyenne : %{y} kWh" \
            " <extra></extra>"
    else:
        return "<b style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Heure :  %{x}h</b>" \
            "<br style='font-family: Grenze Gotisch;font-size: 24px; color: black'> Consommation moyenne : %{y} kWh" \
            " <extra></extra>" 
