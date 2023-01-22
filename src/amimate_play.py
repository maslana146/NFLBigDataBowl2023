import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

colors = {0: '#D50A0A',
          1: '#003594',
          2: '#CBB67C'
          }


def animate_play(tracking_df, play_df, players, pffScoutingData, gameId, playId, games_data):
    games_temp = games_data[games_data['gameId'] == gameId].values[0]
    selected_play_df = play_df[(play_df.playId == playId) & (play_df.gameId == gameId)].copy()

    tracking_players_df = pd.merge(tracking_df, players, how="left", on="nflId")
    tracking_players_df = pd.merge(tracking_players_df, pffScoutingData, how="left",
                                   on=["nflId", "playId", "gameId"])
    selected_tracking_df = tracking_players_df[
        (tracking_players_df.playId == playId) & (tracking_players_df.gameId == gameId)].copy()

    sorted_frame_list = selected_tracking_df.frameId.unique()
    sorted_frame_list.sort()

    # get play General information
    line_of_scrimmage = selected_play_df.absoluteYardlineNumber.values[0]
    first_down_marker = line_of_scrimmage + selected_play_df.yardsToGo.values[0]
    down = selected_play_df.down.values[0]
    quarter = selected_play_df.quarter.values[0]
    gameClock = selected_play_df.gameClock.values[0]
    playDescription = selected_play_df.playDescription.values[0]
    # Handle case where we have a really long Play Description and want to split it into two lines
    if len(playDescription.split(" ")) > 15 and len(playDescription) > 115:
        playDescription = " ".join(playDescription.split(" ")[0:16]) + "<br>" + " ".join(
            playDescription.split(" ")[16:])

    # initialize plotly start and stop buttons for animation
    updatemenus_dict = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 0}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    # initialize plotly slider to show frame position in animation
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Frame:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    frames = []
    for frameId in sorted_frame_list:
        data = []
        # Add Numbers to Field
        data.append(
            go.Scatter(
                x=np.arange(20, 110, 10),
                y=[5] * len(np.arange(20, 110, 10)),
                mode='text',
                text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
                textfont_size=30,
                textfont_family="Courier New, monospace",
                textfont_color="#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        data.append(
            go.Scatter(
                x=np.arange(20, 110, 10),
                y=[53.5 - 5] * len(np.arange(20, 110, 10)),
                mode='text',
                text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
                textfont_size=30,
                textfont_family="Courier New, monospace",
                textfont_color="#ffffff",
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add line of scrimage
        data.append(
            go.Scatter(
                x=[line_of_scrimmage, line_of_scrimmage],
                y=[0, 53.5],
                line_dash='dash',
                line_color='blue',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Add First down line
        data.append(
            go.Scatter(
                x=[first_down_marker, first_down_marker],
                y=[0, 53.5],
                line_dash='dash',
                line_color='yellow',
                showlegend=False,
                hoverinfo='none'
            )
        )
        # Plot Players
        for color_id, team in enumerate(selected_tracking_df.team.unique()):
            plot_df = selected_tracking_df[(selected_tracking_df.team == team) & (
                    selected_tracking_df.frameId == frameId)].copy()
            if team != "football":
                hover_text_array = []
                for nflId in plot_df.nflId:
                    selected_player_df = plot_df[plot_df.nflId == nflId]
                    p_info = {
                        #
                        'Name': f"""{selected_player_df["displayName"].values[0]}""",
                        'nflId': selected_player_df["nflId"].values[0],
                        # 'Position':selected_player_df["pff_positionLinedUp"].values[0],
                        # 'Role':selected_player_df["pff_role"].values[0],
                    }
                    hover_text_array.append(p_info)
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"], mode='markers',
                                       marker_color=colors[color_id], name=team,
                                       hovertext=hover_text_array, hoverinfo="text"))
            else:
                data.append(go.Scatter(x=plot_df["x"], y=plot_df["y"], mode='markers',
                                       marker_color=colors[color_id], name=team, hoverinfo='none'))
        # add frame to slider
        slider_step = {"args": [
            [frameId],
            {"frame": {"duration": 100, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 0}}
        ],
            "label": str(frameId),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
        frames.append(go.Frame(data=data, name=str(frameId)))

    scale = 10
    layout = go.Layout(
        autosize=False,
        width=120 * scale,
        height=60 * scale,
        xaxis=dict(range=[0, 120], autorange=False, tickmode='array',
                   tickvals=np.arange(10, 111, 5).tolist(), showticklabels=False),
        yaxis=dict(range=[0, 53.3], autorange=False, showgrid=False, showticklabels=False),

        plot_bgcolor='#00B140',
        title=f"{games_temp[-2]} vs {games_temp[-1]}<br>{gameClock} {quarter}Q",
        updatemenus=updatemenus_dict,
        sliders=[sliders_dict]
    )

    fig = go.Figure(
        data=frames[0]["data"],
        layout=layout,
        frames=frames[1:]
    )
    # Create First Down Markers
    for y_val in [0, 53]:
        fig.add_annotation(
            x=first_down_marker,
            y=y_val,
            text=str(down),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="black"
            ),
            align="center",
            bordercolor="black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=1
        )
    fig_speed_line = px.line(selected_tracking_df[selected_tracking_df['pff_role'].isin(
        ['Pass Block', 'Pass Rush'])].dropna(subset=['frameId', 's', 'nflId']),
                             x='frameId',
                             y='s',
                             color='displayName',
                             line_dash='team')

    fig.update_layout(paper_bgcolor="#282828",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="white"
                      ))
    return fig, fig_speed_line, playDescription
