import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from os import path

ABS_PATH = path.dirname(path.realpath(__file__))

def read_data():
    frame = None
    read_path = path.join(ABS_PATH, 'stat_data', 'agent_data.csv')
    if path.exists(read_path):
        frame = pd.read_csv(read_path)
    return frame

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

def population_time(frame):
    x = np.zeros(frame['ticks'][0])
    y_tot = np.zeros(frame['ticks'][0])
    y_evil = np.zeros(frame['ticks'][0])
    y_neutral = np.zeros(frame['ticks'][0])
    for i in range(x.size):
        x[i] = i
        for j in range(len(frame.index)):
            age = frame['age'][j]
            birth = frame['birth_tick'][j]
            # If alive at time tick
            if birth <= i and age + birth+1 >= i: 
                y_tot[i] += 1
                if frame['type'][j] == 'ObjectType.NEUTRAL':
                    y_neutral[i] += 1
                else:
                    y_evil[i] += 1
    fig, ax = plt.subplots()
    ax.plot(x, y_tot, label='Total')
    ax.plot(x, y_evil, label='Evil')
    ax.plot(x, y_neutral, label='Neutral')
    ax.grid()
    ax.set(xlabel='Time Ticks', ylabel='Population', title='Population/Time')
    ax.legend()
    plt.show()

def stats_time(frame):
    x = np.zeros(frame['ticks'][0])
    speed = np.zeros(frame['ticks'][0])
    agility = np.zeros(frame['ticks'][0])
    intelligence = np.zeros(frame['ticks'][0])
    endurance = np.zeros(frame['ticks'][0])
    strength = np.zeros(frame['ticks'][0])
    fertility = np.zeros(frame['ticks'][0])
    bite_size = np.zeros(frame['ticks'][0])

    for i in range(x.size):
        x[i] = i
        for j in range(len(frame.index)):
            age = frame['age'][j]
            birth = frame['birth_tick'][j]
            # If alive at time tick
            if birth <= i and age + birth+1 >= i:
                speed[i] += frame['speed'][j]
                agility[i] += frame['agility'][j]
                intelligence[i] += frame['intelligence'][j]
                endurance[i] += frame['endurance'][j]
                strength[i] += frame['strength'][j]
                fertility[i] += frame['fertility'][j]
                bite_size[i] += frame['bite_size'][j]
    
    fig, ax = plt.subplots()
    ax.plot(x, speed, label='Speed')
    ax.plot(x, agility, label='Agility')
    ax.plot(x, intelligence, label='Intelligence')
    ax.plot(x, endurance, label='Endurance')
    ax.plot(x, strength, label='Strength')
    ax.plot(x, fertility, label='Fertility')
    ax.plot(x, bite_size, label='Bite Size')
    ax.grid()
    ax.set(xlabel='Time Ticks', ylabel='Stat Totals', title='Stats/Time')
    ax.legend()
    plt.show()

def run_analysis():
    frame = read_data()
    population_time(frame)
    stats_time(frame)
    
    if frame is not None:
        DrawHist(frame.loc[:, 'health'], "Health of Buddies", "Number of Buddies")
        DrawHist(frame.loc[:, 'score'], "Buddy Scores", "Number of Buddies")
        DrawHist(frame.loc[:, 'energy'], "Remaining Buddy Energy", "Number of Buddies")
        DrawHist(frame.loc[:, 'age'], "Buddy Age", "Number of Buddies")
        DrawHist(frame.loc[:, 'children'], "Number of Children", "Number of Buddies")
        DrawHist(frame.loc[:, 'speed'], "Buddy Speed", "Number of Buddies")
        DrawHist(frame.loc[:, 'agility'], "Buddy Agility", "Number of Buddies")
        DrawHist(frame.loc[:, 'intelligence'], "Buddy Intelligence", "Number of Buddies")
        DrawHist(frame.loc[:, 'strength'], "Buddy Strength", "Number of Buddies")
        DrawHist(frame.loc[:, 'fertility'], "Buddy Fetility", "Number of Buddies")

run_analysis()
