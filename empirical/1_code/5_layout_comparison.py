# coding: utf-8

# Introduction

"""
Vizuelize two keyboard layouts: standard (QWERTY) vs optimized, using sample text
"""

NAME = '5_layout_comparison' ## Name of the notebook goes here (without the file extension!)
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, math, time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
from sklearn.feature_extraction.text import CountVectorizer

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

mapping = pd.read_csv(os.path.join('empirical', '2_pipeline', '4_combine_networks',
                                    'out', 'pairs.csv'), header=None)

mapping_dict = dict(zip(mapping[0], mapping[1]))

key_dict = dict()
top = 'qwertyuiop'
middle = 'asdfghjkl'
bottom = 'zxcvbnm'

# remapped keys
m_key_dict = dict()
m_top = ''.join(list(map(lambda l: mapping_dict[l], top)))
m_middle = ''.join(list(map(lambda l: mapping_dict[l], middle)))
m_bottom = ''.join(list(map(lambda l: mapping_dict[l], bottom)))

t = np.linspace(-53, 37, 10)
for idx, letter in enumerate(zip(top, m_top)):
    key_dict[letter[0]] = (t[idx], 10)
    m_key_dict[letter[1]] = (t[idx], 10)

m = np.linspace(-50, 30, 9)
for idx, letter in enumerate(zip(middle, m_middle)):
    key_dict[letter[0]] = (m[idx], 0)
    m_key_dict[letter[1]] = (m[idx], 0)

b = np.linspace(-45, 15, 7)
for idx, letter in enumerate(zip(bottom, m_bottom)):
    key_dict[letter[0]] = (b[idx], -10)
    m_key_dict[letter[1]] = (b[idx], -10)

# sample text for plotting purposes
sample = pd.read_csv(os.path.join('empirical', '2_pipeline',
                                       '0_get_corpuses', 'out', 'corpuses.csv'), nrows=50)
uni_vectorizer = CountVectorizer(analyzer='char', ngram_range=(1,1))
uni_transformed = uni_vectorizer.fit_transform(pd.Series(sample.iloc[40]['corpus']))
unigrams = pd.DataFrame(uni_transformed.toarray(), columns=uni_vectorizer.get_feature_names()).sum(axis=0)
unigrams = unigrams/max(unigrams)


fig = plt.figure(facecolor='w')

ax1 = fig.add_subplot(211)
plt.xlim(-55,50)
plt.ylim(-10,20)
for k,v in key_dict.items():
    a = unigrams[k]
    ax1.add_patch(Rectangle(v, 8, 8, alpha=a, color='red'))
    plt.text(v[0]+2, v[1]+4, k, color='black')
plt.axis('off')
ax1.set_title('QWERTY Layout')

ax2 = fig.add_subplot(212)
plt.xlim(-55,50)
plt.ylim(-10,20)
for k,v in m_key_dict.items():
    a = unigrams[k]
    ax2.add_patch(Rectangle(v, 8, 8, alpha=a, color='red'))
    plt.text(v[0]+2, v[1]+4, k, color='black')
plt.axis('off')
ax2.set_title('Optimized Layout')
plt.show()


# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
