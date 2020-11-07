import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from os import path

ABS_PATH = path.dirname(path.realpath(__file__))

rnd_data = []
food_eaten = []
scores = []
energy = []

#DrawHist- Draws a Histogram that includes more labels along the x-axis such as the values at the edge of each bar, the percentage of buddies in the bar
#and the value at the center of each bar
#The bars will also be coloured depending upon the side of the graph 
#data_set is the data the graph will use *****Buddies are currently always on the Y axis****** The Ylabel is the label for the Y axis

def DrawHist(data_set, title, yLabel):	
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(data_set, facecolor='yellow', edgecolor='gray')
    plt.title(title)
    plt.ylabel(yLabel)
    # Set the ticks to be at the edges of the bins. 
    ax.set_xticks(bins)
    # Set the xaxis's tick labels to be formatted with 1 decimal place...
    ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

    # Change the colors of bars at the edges...
    twentyfifth, seventyfifth = np.percentile(data_set, [25, 75])
    for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
        if rightside < twentyfifth:
            patch.set_facecolor('green')
        elif leftside > seventyfifth:
            patch.set_facecolor('red')

    # Label the raw counts and the percentages below the x-axis...
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        # Label the raw counts
        ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
            xytext=(0, -18), textcoords='offset points', va='top', ha='center')

        # Label the percentages
        percent = '%0.0f%%' % (100 * float(count) / counts.sum())
        ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
        xytext=(0, -32), textcoords='offset points', va='top', ha='center')


    # Give ourselves some more room at the bottom of the plot
    plt.subplots_adjust(bottom=0.15)
    plt.show()



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

    DrawHist(food_eaten, "Food Eaten by Buddies", "Number of Buddies")
    DrawHist(scores, "Buddy Scores", "Number of Buddies")
    DrawHist(energy, "Remaining Buddy Energy", "Number of Buddies")
