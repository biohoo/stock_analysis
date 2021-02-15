import pandas as pd
import re
import requests
import sys
import urllib.request as urllib2
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from jonathan_utilities.pandas_better_formatting import set_pandas_options
set_pandas_options()

if __name__ != '__main__':
    from parsers.config import total_stocks


TEST_URL = 'https://finance.yahoo.com/quote/FB'


# Zacks works beautifully.

def get_zacks(site):
    '''
    Zacks consensus scores
    :param site:
    :return:
    '''
    global total_stocks
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        r = requests.get(site, headers=header)
        dfs = pd.read_html(r.text)

        consensus = ''



        for i in range(len(dfs)):
            if 'Definition' in dfs[i].columns:
                if 'Definition' in str(dfs[i]['Definition'].iloc[1]):

                    consensus = str(dfs[i]['Definition'].iloc[0])
                    break


        consensus = str(consensus).split(' ')[-1]

        if consensus in ['1','2','3','4','5']:
            rank = {'1':'Strong Buy',
                    '2':'Buy',
                    '3':'Neutral',
                    '4':'Sell',
                    '5':'Strong Sell'}
            consensus = rank[consensus]
            total_stocks -= 1
        else:
            total_stocks -= 1
            consensus = 'None'

        print(consensus, site, total_stocks)

        return consensus, site
    except Exception as e:
        print('exception')
        print(e)
        total_stocks -= 1
        return "None", site



# May as well skip this for now...

def get_the_street(site):
    pass


# Simple and works

def get_fool(site):
    '''
    site:arg
    '''


    global total_stocks


    try:
        html_doc = requests.get(site).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        rating = soup.find(class_='number-of-stars')['alt'][0]
        print(rating, site,total_stocks)

        total_stocks -= 1
        return rating, site

    except:

        total_stocks -= 1
        print('Nope.', site, total_stocks)
        return "None", site



def get_wall_street_journal(site):
    '''Fix this.'''
    global total_stocks
    try:
        r = requests.get(site)
        dfs = pd.read_html(r.content)
        number_buys = dfs[8].loc[0,'Current']
        consensus = dfs[8].loc[5, 'Current']
        print(number_buys, consensus, site)
        print(total_stocks)
        total_stocks -= 1
        return number_buys, consensus, site
    except:
        print('Nope: ', site, total_stocks)
        total_stocks -= 1
        return "None", "None", site

def get_yahoo(site):

    global total_stocks




    #except:
'''
        total_stocks -= 1
        print('Nope.', site)
        return "None", site
'''

if __name__ == '__main__':
    from config import total_stocks

    get_zacks('https://www.zacks.com/stock/quote/f')