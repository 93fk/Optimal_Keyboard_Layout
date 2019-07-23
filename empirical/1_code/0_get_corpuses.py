# coding: utf-8

# Introduction

"""
Web scraping book corpuses
"""

NAME = '0_get_corpuses'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports  

import os, re
import pandas as pd
import requests
from bs4 import BeautifulSoup

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
""" 
-- Save data to pipeline folder --
 
    auto_df['log_weight'] = np.log(auto_df['weight'])  
    auto_df.to_excel(os.path.join(pipeline, 'out', 'auto.xls'))
"""



# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
