import requests
from enum import Enum
from bs4 import BeautifulSoup

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
    data = {
        "price": float(priceText),
        "change$": float(dollarChangeText),
        "change%": percentChangeText
    }
    return data


def getPE(ticker):
    ticker = ticker.lower()
    page = requests.get(
        "https://old.nasdaq.com/symbol/{}/stock-report".format(ticker))
    soup = BeautifulSoup(page.content, 'html.parser')

    tag = soup.find(id='pe_ratio')
    try:
        tag = tag.find_parent('th')
        tag = tag.find_parent('tr')

        parsedAmount = str(tag.td)
        delimiters = ['<td>', '</td>', '$', ',']
        for d in delimiters:
            parsedAmount = parsedAmount.replace(d, '')
        return float(parsedAmount)
    except:
        return 0 


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


class Order(Enum):
    descending = 0
    ascending = 1

def sortList(list, element, order):
    output = list.copy()
    if(order == Order.ascending):
        for i in range(0, len(output)):
            for j in range(0, len(output)):
                if output[i][element] < output[j][element]:
                    temp = output[i]
                    output[i] = output[j]
                    output[j] = temp
    elif(order == Order.descending):
        for i in range(0, len(output)):
            for j in range(0, len(output)):
                if output[i][element] > output[j][element]:
                    temp = output[i]
                    output[i] = output[j]
                    output[j] = temp   
    return output


if __name__ == '__main__':
    print(getCompanyName('FB'))


    # tickers = [
    #     'FB',
    #     'MU',
    #     'AMZN',
    #     'MCD',
    #     'PAGS',
    #     'GLOB',
    #     'MSFT',
    #     'TSLA',
    #     'AAPL',
    #     'REAL',
    #     'NVDA',
    #     'AMD'
    # ]
    # stats = []

    # for ticker in tickers:
    #     data = getStock(ticker)
    #     print("Ticker: {}".format(ticker))
    #     print("Price: ${}".format(data["price"]))
    #     print("Change: ${}".format(data["change$"]))
    #     print("Change: {}%".format(data["change%"]))
    #     print("---------------------------------")

    # for ticker in tickers:
    #     roic = getROIC(ticker)
    #     if(roic != None):
    #         roic = str(round(getROIC(ticker), 4) * 100)[0:5]
    #     else:
    #         roic = str(roic)
    #     pe = getPE(ticker)
    #     if(pe != 0):
    #         earningsYield = 1 / pe
    #     else:
    #         earningsYield = 0
    #     stats.append([ticker, roic, earningsYield])
    #     print(ticker, 'ROIC:', roic + '%', 'Earnings Yield:', str(earningsYield)[0:5])
    
    # roic_stats = sortList(stats, 1, Order.descending)
    # ey_stats = sortList(stats, 2, Order.descending) 

    # print("\nROIC:")
    # for s in roic_stats:
    #     print(s)

    # print("Earnings Yield:")
    # for s in ey_stats:
    #     print(s)

    # rank = []

    # for i, s in enumerate(roic_stats):
    #     rank.append([roic_stats[i][0], str(roic_stats[i][1]) + '%', roic_stats[i][2], ey_stats.index(roic_stats[i]) + i])
    
    # rank = sortList(rank, 3, Order.ascending)

    # print("-----------------------")
    # for i, r in enumerate(rank):
    #     r[len(r) - 1] = i + 1
    #     print(r)