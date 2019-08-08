# coding: utf-8

# Introduction

"""
Vizuelize two keyboard layouts: standard (QWERTY) vs optimized, using sample text
"""

NAME = '5_layout_comparison' ## Name of the notebook goes here (without the file extension!)
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, time, requests, random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
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
def get_soup(page_address):
    url = 'http://www.fullbooks.com/' + page_address
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_text(soup):
    regex = re.compile(r'[\n\r\t]')
    #when a book has multiple sub pages
    if len(soup.find_all('a')) > 1:
        whole_corpus = []
        for part_soup in soup.find_all('a')[:-1]:
            text_soup = get_soup(part_soup['href'])
            for script in text_soup(["script", "style"]):
                script.extract()
            corpus = regex.sub(' ', text_soup.get_text()).lower()
            corpus = ''.join(re.findall(r'[a-z]+', corpus))
            whole_corpus.append(corpus)
            del corpus, text_soup
        return ''.join(whole_corpus)
    #when book has no sub pages
    else:
        for script in soup(["script", "style"]):
            script.extract()
        corpus = regex.sub(' ', soup.get_text()).lower()
        corpus = ''.join(re.findall(r'[a-z]+', corpus))
        return corpus

random.seed('sample-text')
corpuses_df = pd.DataFrame(columns=['url', 'corpus', 'page', 'book'])
num_corpuses = 3

while corpuses_df.shape[0] < num_corpuses:
    page_index = random.randint(1, 54)
    #get random index
    page_soup = get_soup(f'idx{page_index}.html')

    book_index = random.randint(0, len(page_soup.find_all('a'))-1)

    #check if a book is already in the DataFrame
    b1 = corpuses_df['page'] == page_index
    b2 = corpuses_df['book'] == book_index
    if any(b1 & b2):
        continue

    #get random book
    book_soup = get_soup(page_soup.find_all('a')[book_index]['href'])
    corpuses_df = corpuses_df.append(
        {'url': page_soup.find_all('a')[book_index]['href'],
         'corpus': get_text(book_soup),
         'page':page_index,
         'book':book_index},
        ignore_index=True
        )
    if corpuses_df.shape[0] % 30 == 0:
        time.sleep(5)

uni_vectorizer = CountVectorizer(analyzer='char', ngram_range=(1,1))
uni_transformed = uni_vectorizer.fit_transform(corpuses_df['corpus'])
unigrams = pd.DataFrame(uni_transformed.toarray(), columns=uni_vectorizer.get_feature_names())
unigrams = unigrams.apply(lambda x: x/max(x), axis=1)

for i in range(3):
    uni = unigrams.iloc[i]
    fig = plt.figure(facecolor='w')
    
    ax1 = fig.add_subplot(211)
    plt.xlim(-55,50)
    plt.ylim(-10,20)
    for k,v in key_dict.items():
        a = uni[k]
        ax1.add_patch(Rectangle(v, 8, 8, alpha=a, color='red'))
        plt.text(v[0]+2, v[1]+4, k, color='black')
    plt.axis('off')
    ax1.set_title('QWERTY Layout', color='black', weight='bold')
        
    ax2 = fig.add_subplot(212) 
    plt.xlim(-55,50)
    plt.ylim(-10,20)
    for k,v in m_key_dict.items():
        a = uni[k]
        ax2.add_patch(Rectangle(v, 8, 8, alpha=a, color='red'))
        plt.text(v[0]+2, v[1]+4, k, color='black')
    plt.axis('off')
    ax2.set_title('Optimized Layout', color='black', weight='bold')
    plt.show()
    fig.savefig(os.path.join(pipeline, 'out', corpuses_df.iloc[i]['url'][:-5]+'.png'), facecolor='w')


# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet

sample = pd.read_csv(os.path.join('empirical', '2_pipeline',
                                       '0_get_corpuses', 'out', 'corpuses.csv'), nrows=50)
uni_vectorizer = CountVectorizer(analyzer='char', ngram_range=(1,1))
uni_transformed = uni_vectorizer.fit_transform(pd.Series(sample.iloc[40]['corpus']))
unigrams = pd.DataFrame(uni_transformed.toarray(), columns=uni_vectorizer.get_feature_names()).sum(axis=0)
unigrams = unigrams/max(unigrams)
"""
