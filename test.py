import requests
from enum import Enum
from bs4 import BeautifulSoup
import pprint

def getBalanceSheet(ticker):
    ticker = ticker.lower()

    # Pull the web page
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=balance-sheet".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extract the table with Balance Sheet data
    table = soup.find_all('table')[2]
    
    # Extract the time period
    headings = table.find_all('th')
    for i in range(len(headings)):
        headings[i] = headings[i].text.strip()
    period = headings[2:6]

    # Slice list cutting off the first category
    headings = headings[7:]

    # Separate the table into its categories
    currentAssets = {}
    longTermAssets = {}
    currentLiabilities = {}
    stockHoldersEquity = {}

    balanceSheet = {
        'Current Assets' : currentAssets,
        'Long-Term Assets' : longTermAssets,
        'Current Liabilities' : currentLiabilities,
        'Stock Holders Equity' : stockHoldersEquity
    }

    for item in balanceSheet:
        for i in range(len(headings)):
            if(headings[i] in balanceSheet):
                headings = headings[i + 1:]
                break
            amounts = []
            raw = soup.find(text=headings[i]).find_parent('tr')
            raw_children = raw.find_children('td')
            for r in raw:
                print(r)
            balanceSheet[item][headings[i]] = 0



    # rows = soup.find_all('tr')
    # for r in rows:
    #     items = r.find_all('td')
    #     for i in items:
    #         if(i.text != "" and i.text != None):
    #             print(i.text.strip())

    pprint.pprint(balanceSheet)


if __name__ == "__main__":
    getBalanceSheet('fb')