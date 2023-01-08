from dash import Dash, Input, Output, html, dcc
import plotly.express as px
from load_data import (
    weeks_data, pff_scouting_data, players_data, plays_data
)
import pandas as pd

from src.amimate_play import animate_play
from src.player_heatmap import get_player_season_info


def get_players_option():
    data = players_data
    options = {player[1][0]: player[1][6] for player in data.iterrows()}
    return options


app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='NFL Big Data Bowl 2023'),
    html.H3("Week of the game ..."),
    dcc.Dropdown(placeholder="Week of the game ...", options=[i for i in range(1, 9)],
                 id='week_number_input', value=1,clearable=False),
    html.H3("Game id input ..."),
    dcc.Dropdown(placeholder="Game id input ...", multi=False, id='game_id_input',
                 value=2021090900,clearable=False),
    html.H3("Play id input ..."),
    dcc.Dropdown(id='play_id_input', value=349, placeholder="Play id input ...",clearable=False),
    dcc.Loading(
        id="loading-1",
        type="graph",
        children=dcc.Graph(
            id='animate-graph',
        )
    ),
    html.H3("Player season info"),
    dcc.Dropdown(id='player_id_input', value=25511, options=get_players_option(),
                 placeholder="Play id input ...",clearable=False),
    dcc.Loading(
        id="loading-2",
        type="graph",
        children=[html.H4(id='player_info'), dcc.Graph(
            id='player-graph',
        )]
    ),

])


@app.callback(
    Output("game_id_input", "options"),
    Output("game_id_input", "value"),
    Input("week_number_input", "value")
)
def update_game_id_options(week_id):
    week_data = weeks_data[week_id - 1]
    options = list(week_data['gameId'].unique())
    return options, options[0]


@app.callback(
    Output("play_id_input", "options"),
    Output("play_id_input", "value"),
    Input("week_number_input", "value"),
    Input("game_id_input", "value")
)
def update_play_id_options(week_id, game_id):
    week_data = weeks_data[week_id - 1]
    # list(weeks_data[0][weeks_data[0]['gameId'] == 2021090900]['playId'].unique())
    options = list(week_data[week_data['gameId'] == game_id]['playId'].unique())
    return options, options[0]


@app.callback(
    Output('animate-graph', 'figure'),
    Input('week_number_input', 'value'),
    Input('game_id_input', 'value'),
    Input('play_id_input', 'value'))
def update_figure(week_number, game_id, player_id):
    fig_anime, fig_speed_line = animate_play(weeks_data[week_number - 1], plays_data, players_data,
                                             pff_scouting_data, game_id, player_id)
    return fig_anime


@app.callback(
    Output('player-graph', 'figure'),
    Output('player_info', 'children'),
    Input('player_id_input', 'value'))
def update_figure(player_id):
    print(player_id)
    return get_player_season_info(player_id)


if __name__ == '__main__':
    app.run_server(debug=True)
