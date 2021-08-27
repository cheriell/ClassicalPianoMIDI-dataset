import pandas as pd
import numpy as np
import pretty_midi as pm
import math
from collections import Counter
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")

metadata = pd.read_csv('metadata.csv')

# durations
for i, row in metadata.iterrows():
    if not math.isnan(row['year']):
        metadata.loc[i, 'year'] = str(int(row['year']))
    if math.isnan(row['duration']):
        midi_data = pm.PrettyMIDI(row['midi'])
        duration = midi_data.get_end_time()
        metadata.loc[i, 'duration'] = duration
metadata.to_csv('metadata.csv', index=False)
print('Total duration: {:.2f} hours.'.format(metadata.sum()['duration'] / 3600))

# count composer
count_composer = Counter(metadata.loc[:,'composer'])
count_composer = [(composer, count) for composer, count in count_composer.items()]
count_composer.sort(key=lambda x: x[1])
x = [item[0] for item in count_composer]
y = [item[1] for item in count_composer]

fig, ax = plt.subplots(figsize=(10,10))    
width = 0.7 # the width of the bars 
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color='royalblue')
for i, v in enumerate(y):
    ax.text(v+0.5, i-0.2, str(v), color='purple', fontweight='bold')
ax.set_yticks(ind)
ax.set_yticklabels(x, minor=False)
plt.title('Music pieces by composer')
plt.xlabel('number of pieces')
plt.savefig('statistics.svg')