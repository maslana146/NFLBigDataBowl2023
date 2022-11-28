import pandas as pd

weeks_data = []
for week in range(1, 9):
    weeks_data.append(pd.read_csv(f'../data/week{week}.csv'))

games_data = pd.read_csv(f'../data/games.csv')
pff_scouting_data = pd.read_csv(f'../data/pffScoutingData.csv')
players_data = pd.read_csv(f'../data/players.csv')
plays_data = pd.read_csv(f'../data/plays.csv')
