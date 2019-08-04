# coding: utf-8

# Introduction

"""
Building network of letters
"""

NAME = '3_letters_graph'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, math, time, itertools
import pickle
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

## Set working directory

workdir = re.sub("(?<={})[\w\W]*".format(PROJECT), "", os.getcwd())
os.chdir(workdir)

## Set  up pipeline folder if missing

if os.path.exists(os.path.join('empirical', '2_pipeline')):
    pipeline = os.path.join('empirical', '2_pipeline', NAME)
else:
    pipeline = os.path.join('2_pipeline', NAME)

if not os.path.exists(pipeline):
    os.makedirs(pipeline)
    for folder in ['out', 'store', 'tmp']:
        os.makedirs(os.path.join(pipeline, folder))

# ---------
# Main code
# ---------

unigrams = pd.read_csv(os.path.join('empirical', '2_pipeline',
                                    '1_unigrams_and_bigrams', 'out', 'unigrams.csv'), header=None)

bigrams = pd.read_csv(os.path.join('empirical', '2_pipeline',
                                    '1_unigrams_and_bigrams', 'out', 'bigrams.csv'), header=None)

unigrams[1] = unigrams[1]/max(unigrams[1])
bigrams[1] = bigrams[1]/max(bigrams[1])

Letters_net = nx.Graph()

for idx, val in zip(unigrams[0], unigrams[1]):
    Letters_net.add_node(idx, size=val)

for idx, val in zip(bigrams[0], bigrams[1]):
    Letters_net.add_edge(idx[0], idx[1], weight=val)

pickle.dump(Letters_net, open(os.path.join(pipeline, 'out', 'Letters_net.p'), 'wb'))

size = [np.sqrt(size)*1500 for size in nx.get_node_attributes(Letters_net,  'size').values()]
weigth = [(Letters_net[edge[0]][edge[1]]['weight']+0.6)**6 for edge in Letters_net.edges()]

fig = plt.figure(facecolor='w')
pos = nx.layout.shell_layout(Letters_net)
nx.draw_networkx_nodes(Letters_net, pos, node_size=size, edgecolors='black', alpha=0.80)
nx.draw_networkx_edges(Letters_net, pos, width=weigth, alpha=0.50, arrowstyle='simple')
nx.draw_networkx_labels(Letters_net, pos)
plt.axis('off')
plt.show()
fig.savefig(os.path.join(pipeline, 'out', 'letters_network.png'), facecolor='w')

# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
