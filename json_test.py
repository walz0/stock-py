import json
import stock_pull as pull 
import pprint

data = {}
data['stocks'] = []

def recordTicker(ticker):
    stockData = pull.getStock(ticker)
    close = stockData['price']
    dollarChange = stockData['change$']
    percentChange = stockData['change%']
    peRatio = pull.getPE(ticker)
    roic = pull.getROIC(ticker)
    if(peRatio != 0):
        earningsYield = 1 / peRatio 
    else:
        earningsYield = None 

    data['stocks'].append({
        'ticker': str(ticker),
        'close': str(close),
        'dollarChange': str(dollarChange), 
        'percentChange': str(percentChange),
        'roic': str(roic), 
        'peRatio': str(peRatio),
        'earningsYield' : str(earningsYield)   
    })

if __name__ == '__main__':
    tickers = [
        'FB',
        'MU',
        'AMZN',
        'MCD',
        'PAGS',
        'GLOB',
        'MSFT',
        'TSLA',
        'AAPL',
        'REAL',
        'NVDA',
        'AMD'
    ]

    # print("Downloading data...")
    
    # for ticker in tickers:
    #     recordTicker(ticker)

    # with open('data.json', 'w') as outfile:
    #     json.dump(data, outfile)        

    # pprint.pprint(data)

    query = input('Enter a ticker: ').upper()

    stocks = []
    with open('data.json') as json_file:
        data = json.load(json_file)
        for s in data['stocks']:
            stocks.append(s)

    def queryJSONfile(ticker, json_file):
        ticker = ticker.upper()
        with open('data.json') as json_file:
            data = json.load(json_file)
            for s in data['stocks']:
                if(s['ticker'] == ticker):
                    return s


    pprint.pprint(queryJSONfile(query, json_file))