# coding: utf-8

# Introduction

"""
Web scraping book corpuses
"""

NAME = '0_get_corpuses'
PROJECT = 'Optimal_Keyboard_Layout'
PYTHON_VERSION = '3.6.8'

## Imports

import os, re, random, requests, time
import pandas as pd
from bs4 import BeautifulSoup
from progress.bar import Bar

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
            

random.seed('books-corpuses')
corpuses_df = pd.DataFrame(columns=['url', 'corpus', 'page', 'book'])
num_corpuses = 100
bar = Bar('Processing', max=num_corpuses)

while corpuses_df.shape[0] < num_corpuses:
    bar.next()
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
        time.sleep(120)

corpuses_df.to_csv(os.path.join(pipeline, 'out', 'corpuses.csv'))

# ----------
# Leftovers
# ----------
"""
Here you leave any code snippets or temporary code that you don't need but don't want to delete just yet
"""

