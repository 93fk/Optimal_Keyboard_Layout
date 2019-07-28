# coding: utf-8

# Introduction

"""
Web scraping book corpuses
"""

NAME = '1_unigrams_and_bigrams'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports  

import os, re, math, time
import pandas as pd

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

corpuses_df = pd.read_csv(os.path.join('empirical', '2_pipeline',
                                       '0_get_corpuses', 'out', 'corpuses.csv'), encoding="ISO-8859-1", error_bad_lines=False)

# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
