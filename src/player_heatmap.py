import pandas as pd

from src.load_data import weeks_data
import plotly.express as px


def get_player_season_info(player_nfl_id):
    player_df = None
    for week in weeks_data:
        player_data = week[week['nflId'] == int(player_nfl_id)]
        if player_data is not None:
            player_df = pd.concat([player_df, player_data])
        else:
            player_df = player_data
    fig = px.density_heatmap(player_df,
                             x="x",
                             y="y",
                             marginal_x="violin",
                             marginal_y="violin",
                             nbinsx=240,
                             nbinsy=106,
                             range_x=[0, 120],
                             range_y=[0, 53.3],
                             title='Heatmap of player during the season',
                             width=1200, height=530
                             )
    info = f'''
    Avg. Speed: {round(player_df['s'].mean(),3)} y/s \n
    Avg. Acceleration: {round(player_df['a'].mean(),3)} y/s2, \n
    Total Distance: {round(player_df['dis'].sum(),3)} yards \n
    '''
    return fig, [info]