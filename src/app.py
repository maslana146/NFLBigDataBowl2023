from dash import Dash, Input, Output, html, dcc
import plotly.express as px
from load_data import (
    weeks_data, pff_scouting_data, players_data,plays_data
)
import pandas as pd

from src.amimate_play import animate_play

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='NFL Big Data Bowl 2023'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Input(id='game_id_input', value=2021090900, type='number',placeholder="Game id input ..."),
    dcc.Input(id='player_id_input', value=349, type='number',placeholder="Player id input "
                                                                              "..."),
    dcc.Graph(
        id='animate-graph',
    )
])


@app.callback(
    Output('animate-graph', 'figure'),
    Input('game_id_input', 'value'),
    Input('player_id_input', 'value'))
def update_figure(game_id, player_id):
    fig_anime, fig_speed_line = animate_play(weeks_data[0], plays_data, players_data,
                                             pff_scouting_data, game_id, player_id)
    return fig_anime


if __name__ == '__main__':
    app.run_server(debug=True)
