import requests
from enum import Enum
from bs4 import BeautifulSoup
import pprint
import util
import sys

def getStockPrice(ticker):
    page = requests.get("https://finance.yahoo.com/quote/{}".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find(id='quote-header-info').find_all("span")
    priceText = elements[1].text.replace(',', '')
    return float(priceText)


def getDollarChange(ticker):
    page = requests.get("https://finance.yahoo.com/quote/{}".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find(id='quote-header-info').find_all("span")
    changeText = elements[2].text.split(" ")[0]
    return float(changeText)


def getPercentChange(ticker):
    page = requests.get("https://finance.yahoo.com/quote/{}".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        elements = soup.find(id='quote-header-info').find_all("div")
        changeText = elements[2].text.split(" ")[1].replace(
            '(', '').replace(')', '').replace('%', '')
        return float(changeText) / 100
    except:
        return 0


def getCompanyName(ticker):
    page = requests.get("https://finance.yahoo.com/quote/{}".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find(id='quote-header-info').find_all("h1")
    return elements[0].text


def getStock(ticker):
    page = requests.get("https://finance.yahoo.com/quote/{}".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.find(id='quote-header-info').find_all("span")
    priceText = elements[1].text.replace(',', '')
    dollarChangeText = elements[2].text.split(" ")[0]
    try:
        elements = soup.find(id='quote-header-info').find_all("span")
        percentChangeText = elements[2].text.split(" ")[1].replace(
            '(', '').replace(')', '').replace('%', '')
        percentChangeText = float(percentChangeText) / 100
    except:
        percentChangeText = None
    elements = soup.find(id='quote-header-info').find_all("h1")
    data = {
        "price": float(priceText),
        "change$": float(dollarChangeText),
        "change%": percentChangeText,
        "ticker" : ticker,
        "name" : elements[0].text
    }
    return data


def getPE(ticker):
    ticker = ticker.lower()
    page = requests.get("https://finance.yahoo.com/quote/{}/key-statistics".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')

    tag = soup.find(string='Trailing P/E')
    try:
        tag = tag.find_parent('td')
        tag = tag.find_parent('tr')

        parsedAmount = str(tag.text)
        delimiters = ['<td>', '</td>', '$', ',', 'Trailing P/E']
        for d in delimiters:
            parsedAmount = parsedAmount.replace(d, '')
        return float(parsedAmount)
    except:
        return 0 


def getEarningsYield(ticker):
    return 1 / getPE()


def getIndustryNames():
    page = requests.get("https://old.nasdaq.com/screening/companies-by-industry.aspx")
    soup = BeautifulSoup(page.content, 'html.parser')
    industries_raw = soup.find(id='industryshowall').find_all('a')
    industries = []

    for i in industries_raw:
        industries.append(i.text)

    return industries


def getTickersByIndustry(industry, total):
    # Get Industry links
    page = requests.get("https://old.nasdaq.com/screening/companies-by-industry.aspx")
    soup = BeautifulSoup(page.content, 'html.parser')
    industries_raw = soup.find(id='industryshowall').find_all('a')
    links = []

    for i in industries_raw:
        links.append("https://old.nasdaq.com" + i.get('href'))
    
    pages = 0
    tickers = []
    
    for l in links:
        if(industry in l):
            page = requests.get(l)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Get Total Pages
            results_raw = soup.find(id='resultsDisplay').find_all('b')
            results = int(str(results_raw[1]).replace('<b>', '').replace('</b>', ''))
            pages = round(results / 50)
            itemsPerPage = int(total / pages)
            if(itemsPerPage < 1):
                itemsPerPage = 1

            tickers = []
            for currentPage in range(pages):
                page = requests.get(l + '&page={}'.format(currentPage))
                soup = BeautifulSoup(page.content, 'html.parser')
                
                companyTable = soup.find(id='CompanylistResults').find_all("a")
                allTickers = []
                for i in range(len(companyTable)):
                    raw = companyTable[i].text.strip()
                    if(len(raw) <= 5 and 'Name' not in raw):
                        parsedTicker = raw
                        allTickers.append(parsedTicker)
                for t in range(itemsPerPage):
                    tickers.append(allTickers[t])
    return tickers


def getROIC(ticker):
    ticker = ticker.lower()
    def parseData(items):
        output = []
        for item in items:
            tag = soup.find(string=item)
            if(tag != None):
                parent = tag.find_parent('tr')
                amounts = parent.findChildren('td')
                dollars = []
                for a in amounts:
                    parsedAmount = str(a.text)
                    delimiters = ['<td>', '</td>', '$', ',', '(', ')']
                    if('$' in parsedAmount):
                        for d in delimiters:
                            parsedAmount = parsedAmount.replace(d, '')
                        dollars.append(parsedAmount)
                output.append(dollars)
            else:
                output.append(None)
        return output

    # Pull data from the balance sheet
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=balance-sheet".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    items = [
        'Total Liabilities',
        'Total Assets',
        'Long-Term Debt'
    ]

    output = parseData(items)
    if output[0] != None:
        totalLiabilities = output[0][0]
        totalAssets = output[1][0]
        longTermDebt = output[2][0]

        shareHolderEquity = float(totalAssets) - float(totalLiabilities)
        investedCapital = float(shareHolderEquity) + float(longTermDebt)

        # Pull data from income statement
        page = requests.get(
            "https://old.nasdaq.com/symbol/{}/financials?query=income-statement".format(ticker))
        soup = BeautifulSoup(page.content, 'html.parser')
        items = ['Net Income']
        output = parseData(items)

        netIncome = float(output[0][0])
        roic = netIncome / investedCapital

        return roic
    else:
        return 0


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
            # Create a space for dollar amounts
            amounts = []
            # Find a parse all rows with dollar amounts
            raw = soup.find(text=headings[i]).find_parent('tr')
            raw_children = raw.findChildren('td')
            for r in raw_children:
                if(r.text != ""):
                    amounts.append(r.text)

            balanceSheet[item][headings[i]] = amounts

    return balanceSheet


def getIncomeStatement (ticker):
    ticker = ticker.lower()

    # Pull the web page
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=income-statement".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extract the table with Balance Sheet data
    table = soup.find_all('table')[2]
    
    # Extract the time period
    headings = table.find_all('th')
    for i in range(len(headings)):
        headings[i] = headings[i].text.strip()
    period = headings[2:6]

    # Slice list cutting off the period
    headings = headings[6:]

    # Separate the table into its categories
    operatingExpenses = {}
    other = {}

    incomeStatement = {
        'Other:' : other,
        'Operating Expenses' : operatingExpenses,
    }

    for item in incomeStatement:
        for i in range(len(headings)):
            if(headings[i] in incomeStatement):
                headings = headings[i + 1:]
                break
            # Create a space for dollar amounts
            amounts = []
            # Find a parse all rows with dollar amounts
            raw = soup.find(text=headings[i]).find_parent('tr')
            raw_children = raw.findChildren('td')
            for r in raw_children:
                if(r.text != ""):
                    amounts.append(r.text)

            incomeStatement[item][headings[i]] = amounts

    return incomeStatement


def getCashFlow(ticker):
    ticker = ticker.lower()

    # Pull the web page
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=cash-flow".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extract the table with Balance Sheet data
    table = soup.find_all('table')[2]
    
    # Extract the time period
    headings = table.find_all('th')
    for i in range(len(headings)):
        headings[i] = headings[i].text.strip()
    period = headings[2:6]

    # Slice list cutting off the period
    headings = headings[6:]

    # Separate the table into its categories
    other = {}
    changesInOperating = {}
    cashFlowsOperating = {}
    cashFlowsInvesting = {}
    cashFlowsFinancing = {}

    incomeStatement = {
        'Other:' : other,
        'Cash Flows-Operating Activities' : cashFlowsOperating,
        'Changes in Operating Activities': changesInOperating,
        'Cash Flows-Investing Activities' : cashFlowsInvesting,
        'Cash Flows-Financing Activities' : cashFlowsFinancing 
    }

    for item in incomeStatement:
        for i in range(len(headings)):
            if(headings[i] in incomeStatement):
                headings = headings[i + 1:]
                break
            # Create a space for dollar amounts
            amounts = []
            # Find a parse all rows with dollar amounts
            raw = soup.find(text=headings[i]).find_parent('tr')
            raw_children = raw.findChildren('td')
            for r in raw_children:
                if(r.text != ""):
                    amounts.append(r.text)

            incomeStatement[item][headings[i]] = amounts

    incomeStatement[ticker] = "ticker"
    return incomeStatement


def getFinancialRatios(ticker):
    ticker = ticker.lower()

    # Pull the web page
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/financials?query=ratios".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extract the table with Balance Sheet data
    table = soup.find_all('table')[2]
    
    # Extract the time period
    headings = table.find_all('th')
    for i in range(len(headings)):
        headings[i] = headings[i].text.strip()
    period = headings[2:6]

    # Slice list cutting off the period
    headings = headings[7:]

    # Separate the table into its categories
    other = {}
    liquidityRatios = {}
    profitabilityRatios = {}

    financialRatios = {
        'Liquidity Ratios' : liquidityRatios,
        'Profitability Ratios': profitabilityRatios,
    }

    for item in financialRatios:
        for i in range(len(headings)):
            if(headings[i] in financialRatios):
                headings = headings[i + 1:]
                break
            # Create a space for dollar amounts
            amounts = []
            # Find a parse all rows with dollar amounts
            raw = soup.find(text=headings[i]).find_parent('tr')
            raw_children = raw.findChildren('td')
            for r in raw_children:
                if(r.text != ""):
                    amounts.append(r.text)

            financialRatios[item][headings[i]] = amounts

    financialRatios[ticker] = "ticker"
    return financialRatios 




if __name__ == "__main__":
    pprint.pprint(getFinancialRatios('fb'))