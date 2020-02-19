import requests
from enum import Enum
from bs4 import BeautifulSoup

def getBalanceSheet(ticker):
    ticker = ticker.lower()

    # Pull data from the balance sheet
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=balance-sheet".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    raw = soup.find('table')
    print(raw.tr)

if __name__ == "__main__":
    getBalanceSheet('fb')