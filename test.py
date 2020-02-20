import requests
import stock_pull as pull
from enum import Enum
from bs4 import BeautifulSoup
import pprint


if __name__ == "__main__":
    # tickers = pull.getTickersByIndustry('Technology', 10)
    while(True):
        tickers = []
        tickers.append(input('Enter a ticker:'))
        for t in tickers:
            print(t)
            pprint.pprint(pull.getBalanceSheet(t))