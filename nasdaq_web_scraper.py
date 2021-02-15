import time
import pandas as pd
from concurrent import futures

from parsers.financial_site_parsers import get_the_street, get_zacks, get_fool
from parsers.config import total_stocks


MARKETBEAT = 'https://www.marketbeat.com/stocks/'
NUMBER_OF_SITES = 3 #   Number going into the final analysis.  Excludes Marketbeat.

start_time = time.time()    # How long does this take.

#   Retrieve the initial set of symbols and company information.
tickers_dataframe = pd.read_csv('companylist.csv', header=0) # From https://www.nasdaq.com/screening/company-list.aspx

#   Retrieve all symbols
symbols = tickers_dataframe['Symbol'].tolist()


#   This maps the parser function with some variables such as columns returned, filename, URL.
#   Could be made simpler...buuuut what are you gonna do?

parsers_dictionary = {

    'Zacks':
        {'url':'zacks_url',
        'columns':['zacks_consensus','zacks_URL'],
        'out_file':'zacks.csv',
        'parser':get_zacks,
        'url_string_formatting':"https://www.zacks.com/stock/quote/" + tickers_dataframe['Symbol']
    },

    'Motley Fool':  {
        'url':'fool_url',
        'columns':['fool_rating', 'fool_url'],
        'out_file':'fool.csv',
        'parser':get_fool,
        'url_string_formatting':'https://www.fool.com/quote/' + tickers_dataframe['Symbol']
    }
}


# Add total to variable
number_of_sites = len(parsers_dictionary.keys())
total_stocks = len(symbols) * number_of_sites
print(len(symbols), " Stocks total...\n",number_of_sites," sites and ", total_stocks, " pages.")


for key in parsers_dictionary.keys():
    tickers_dataframe[parsers_dictionary[key]['url']] = parsers_dictionary[key]['url_string_formatting']


parse_all_sites = True

if parse_all_sites:
    with futures.ThreadPoolExecutor() as executor:
        for key in parsers_dictionary.keys():

            results = executor.map(parsers_dictionary[key]['parser'], tickers_dataframe[parsers_dictionary[key]['url']])
            results = pd.DataFrame(results)
            results.columns = parsers_dictionary[key]['columns']
            results.to_csv('results/' + parsers_dictionary[key]['out_file'])


stop_time = time.time()
elapsed = stop_time - start_time

print(f"Total: {round((elapsed)/60, 2)} Minutes")
