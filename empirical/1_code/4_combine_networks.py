# coding: utf-8

# Introduction

"""
Broadcasting one networ onto the other to find an optimal keyboard layout
"""

NAME = '4_combine_networks'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, math, time
import pickle
import random
import pandas as pd
import networkx as nx

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

Keyboard_net = pickle.load(open(os.path.join('empirical', '2_pipeline', '2_keyboard_layout',
                                            'out', 'Keyboard_net.p'), 'rb'))

Letters_net = pickle.load(open(os.path.join('empirical', '2_pipeline', '3_letters_graph',
                                            'out', 'Letters_net.p'), 'rb'))

Keyboard_dict = {key:size['size'] for key, size in Keyboard_net._node.items()}
Keyboard_Series = pd.Series(Keyboard_dict).sort_values(ascending=False).index
letters_list = list(Keyboard_Series)

mapping_dict = {}
full_keyboard = list('qwertyuiopasdfghjklzxcvbnm')

for key in Keyboard_Series:
    letters_list.remove(key)
    Modified_net = Keyboard_net.copy()
    for letter in letters_list:
        Modified_net.remove_node(letter)
    if mapping_dict:
        Modified_net = nx.relabel_nodes(Modified_net, mapping_dict)
    letters_Series = pd.Series()
    for letter in full_keyboard:
        weight_sum = sum(Modified_net[key][edge]['weight'] * Letters_net[letter][edge[0]]['weight']\
                        for edge in Modified_net[key].keys()\
                        if edge[0] in Letters_net[letter])
        size = Modified_net._node[key]['size'] * Letters_net._node[letter]['size']
        letters_Series = letters_Series.append(pd.Series(weight_sum + 3*size, index=[letter]))
    best_letter = letters_Series.sort_values(ascending=False).index[0]
    mapping_dict[key] = best_letter+'_new'
    full_keyboard.remove(best_letter)

for k, v in mapping_dict.items():
    mapping_dict[k] = v[0]

pd.Series(mapping_dict).to_csv(os.path.join(pipeline, 'out', 'pairs.csv'))

# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet

Letters_net['b'][edge.lower()]['weight'] * Keyboard_net['A'][edge]['weight']
 if edge in Letters_net['b']
sum(Letters_net['b'][edge.lower()]['weight'] * Keyboard_net['A'][edge]['weight'] for edge in Keyboard_net['A'].keys() if edge.lower() in Letters_net['b'])




random.seed('network')

best_score = 0
best_pairs = {}
alphabet = list('qwertyuiopasdfghjklzxcvbnm') # Keyboard nodes
bar = Bar('Processing', max=10000000)

for i in range(10000000):
    bar.next()
    shuffled_alphabet = random.sample(alphabet, len(alphabet)) # Letters nodes
    pairs = dict(zip(alphabet, shuffled_alphabet)) # Broadcast letters onto keyboard network

    Relabeled_layout = nx.relabel_nodes(Keyboard_net, pairs)

    scores_dict = {}

    for k, l in pairs.items():
        s = sum(Letters_net[l][edge]['weight'] * Relabeled_layout[k][edge]['weight'] \
            for edge in Relabeled_layout[k].keys() \
            if edge in Letters_net[l])
        scores_dict[k+l] = s + (Letters_net._node[l]['size']*Relabeled_layout._node[k]['size'])*5
    scores_Series = pd.Series(scores_dict)
    if scores_Series.sum() > best_score:
        best_score = scores_Series.sum()
        best_pairs = pd.Series(pairs)

best_pairs.to_csv(os.path.join(pipeline, 'out', 'pairs.csv'))
"""