# coding: utf-8

# Introduction

"""
Extracting unigrams (letters) and bigrams (adjacent letters)
"""

NAME = '1_unigrams_and_bigrams'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, math, time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from itertools import product

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
                                       '0_get_corpuses', 'out', 'corpuses.csv'))

uni_vectorizer = CountVectorizer(analyzer='char', ngram_range=(1,1))
uni_transformed = uni_vectorizer.fit_transform(corpuses_df['corpus'])
unigrams = pd.DataFrame(uni_transformed.toarray(), columns=uni_vectorizer.get_feature_names()).sum(axis=0)

bi_vectorizer = CountVectorizer(analyzer='char', ngram_range=(2,2))
bi_transformed = bi_vectorizer.fit_transform(corpuses_df['corpus'])
bigrams = pd.DataFrame(bi_transformed.toarray(), columns=bi_vectorizer.get_feature_names()).sum(axis=0)

repetitive = [r for r in bigrams.index if r[0] == r[1]]
alphabet = ''.join(l[0] for l in repetitive)

# getting rid of indexes such as 'ba', when 'ab' is already present
duped = []
for index, letter in enumerate(alphabet):
    tuples = list(product(letter, alphabet[:index]))
    duped +=  [''.join(i) for i in tuples if ''.join(i) in bigrams.index]

# summing observations
for i in bigrams.index:
    if i[::-1] in bigrams.index:
        bigrams[i] += bigrams[i[::-1]]

bigrams = bigrams.drop(repetitive+duped)

# save to file
unigrams.to_csv(os.path.join(pipeline, 'out', 'unigrams.csv'))
bigrams.to_csv(os.path.join(pipeline, 'out', 'bigrams.csv'))

# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""
#    print(letter, alphabet[:index])