from bs4 import BeautifulSoup
from enum import Enum

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