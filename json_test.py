import json

data = {}
data['people'] = []
data['stocks'] = []

data['stocks'].append({
    'ticker': 'FB',
    'close': '257.34',
    'roic': '18.03',
    'peRatio': '28.02',
    'earningsYield' : '0.033123'
})

data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})

data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)


with open('data.txt') as json_file:
    data = json.load(json_file)
    for p in data['people']:
        print('Name: ' + p['name'])
        print('Website: ' + p['website'])
        print('From: ' + p['from'])
        print('')
    for s in data['stocks']:
        print('Ticker: ' + s['ticker'])
        print('Close: ' + s['close'])
        print('ROIC: ' + s['roic'])
        print('P/E Ratio: ' + s['peRatio'])
        print('Earnings Yield: ' + s['earningsYield'])