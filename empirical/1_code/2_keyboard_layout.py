# coding: utf-8

# Introduction

"""
Create graph for typical keyboard layout
"""

NAME = '2_keyboard_layout'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, math, time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pickle
from matplotlib.patches import Rectangle
from scipy.stats import skewnorm

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

key_dict = dict()
top = 'QWERTYUIOP'
middle = 'ASDFGHJKL'
bottom = 'ZXCVBNM'

t = (t for t in np.linspace(-53, 37, 10))
for letter in top:
    key_dict[letter] = (next(t), 10)

m = (m for m in np.linspace(-50, 30, 9))
for letter in middle:
    key_dict[letter] = (next(m), 0)

b = (b for b in np.linspace(-45, 15, 7))
for letter in bottom:
    key_dict[letter] = (next(b), -10)

# Keyboard layout with weights
# The assumption is that certain keys are easier to reach. The higher the weight,
# the easier is a key to be pressed.
xxx = np.linspace(-55,55,100)
yyy = np.linspace(-15,20,100)
x,y = np.meshgrid(xxx, yyy)
z = skewnorm.pdf(y*0.1,0.45)*(skewnorm.pdf(x*0.035, 4)+skewnorm.pdf((x+10)*0.035, -4))
max_z = np.amax(z)

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, aspect='equal')
plt.xlim(-55,50)
plt.ylim(-10,20)
for k,v in key_dict.items():
    a = skewnorm.pdf(v[1]*0.1,0.45)*(skewnorm.pdf((v[0])*0.035, 4)+skewnorm.pdf((v[0]+10)*0.035, -4))/max_z
    new = v + (a,)
    key_dict[k] = new
    ax.add_patch(Rectangle(v, 8, 8, alpha=a, color='red'))
    plt.text(v[0]+2, v[1]+4, k, color='black')
plt.axis('off')
plt.show()
fig.savefig(os.path.join(pipeline, 'out', 'keyboard_layout.png'), facecolor='w')

# Create network of keyboard keys
Keyboard_net = nx.Graph()

for K, V in key_dict.items():
    Keyboard_net.add_node(K, size=V[2])
    for k, v in key_dict.items():
        if V[0] < v[0] and V[0] + 10 > v[0] and V[1] == 0: # 'V' Key to the left
            if V[1] - v[1] == 10: # 'V' Key above
                w = abs(V[0] + 10 - v[0])*0.04
                Keyboard_net.add_edge(K, k, weight=w)
            elif V[1] - v[1] == -10: # 'V' Key below
                w = abs(V[0] + 10 - v[0])*0.08
                Keyboard_net.add_edge(K, k, weight=w)
        elif V[0] < v[0] + 10 and V[0] + 10 > v[0] + 10 and V[1] == 0: # 'V' Key to the right
            if V[1] - v[1] == 10: # 'V' Key above
                w = abs(v[0] + 10 - V[0])*0.04
                Keyboard_net.add_edge(K, k, weight=w)
            elif V[1] - v[1] == -10: # 'V' Key below
                w = abs(v[0] + 10 - V[0])*0.08
                Keyboard_net.add_edge(K, k, weight=w)
        else:
            if V[1] == v[1] and V[0] - v[0] == -10: # same row, adjacent keys
                w = 1
                Keyboard_net.add_edge(K, k, weight=w)

pickle.dump(Keyboard_net, open(os.path.join(pipeline, 'out', 'Keyboard_net.p'), 'wb'))

# Delete unnecessary connections
Keyboard_net.remove_edge('T', 'Y')
Keyboard_net.remove_edge('G', 'H')
Keyboard_net.remove_edge('B', 'N')
Keyboard_net.remove_edge('Y', 'G')
Keyboard_net.remove_edge('H', 'B')

#vizualize network
fig = plt.figure(facecolor='w')
size = [(nx.degree_centrality(Keyboard_net)[node]+1.5)**12 for node in Keyboard_net.nodes()]
weigth = [Keyboard_net[edge[0]][edge[1]]['weight']*10 for edge in Keyboard_net.edges()]

pos = {}
for key, value in key_dict.items():
    pos[key] = np.array([value[0], value[1]/10])

nx.draw_networkx_nodes(Keyboard_net, pos, node_size=size, edgecolors='black', alpha=0.80)
nx.draw_networkx_edges(Keyboard_net, pos, width=weigth, alpha=0.50, arrowstyle='simple')
nx.draw_networkx_labels(Keyboard_net, pos, font_size=15, font_family='helvetica')
plt.axis('off')
plt.show()
fig.savefig(os.path.join(pipeline, 'out', 'keyboard_network.png'), facecolor='w')


# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
