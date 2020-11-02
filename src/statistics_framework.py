import pandas as pd
import matplotlib.pyplot as plt
from os import path

ABS_PATH = path.dirname(path.realpath(__file__))

rnd_data = []
food_eaten = []
scores = []
energy = []

i = 1
while path.exists(path.join(ABS_PATH, 'stat_data', f'agent_stats_round{i}.csv')):
    rnd_data.append(pd.read_csv(path.join(ABS_PATH, 'stat_data', f'agent_stats_round{i}.csv')))    
    i += 1

if i == 1:
    print('No data.')
else:
    for data in rnd_data:
        food_eaten.extend(data.loc[:, 'Food Eaten'])
        scores.extend(data.loc[:, 'Score'])
        energy.extend(data.loc[:, 'Energy'])

    plt.hist(food_eaten)
    #plt.hist(scores)
    #plt.hist(energy)
    plt.show()

