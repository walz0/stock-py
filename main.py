import stock_pull as pull
import json_test as store 
import pprint

version = 1.0
stdin = ''

# All accessor functions
keywords = [
    'pull',
    'analysis'
]

# All forms of analysis
analysis = [
    'btm'
]

# All core functions
functions = {
    'bal-sheet' : pull.getBalanceSheet,
    'income' : pull.getIncomeStatement,
    'cash-flow' : pull.getCashFlow,
    'ratios' : pull.getFinancialRatios,
    'roic' : pull.getROIC,
    'by-industry' : pull.getTickersByIndustry,
    'earnings-yield' : pull.getEarningsYield,
    'price' : pull.getStockPrice,
    'dollar-chng' : pull.getDollarChange,
    'percent-chng' : pull.getPercentChange,
    'name' : pull.getCompanyName,
    'stock' : pull.getStock,
    'pe' : pull.getPE,
    'industries' : pull.getIndustryNames
}

def parseInput(stdin):
    stdin = stdin.lower()
    sel_keys = []
    sel_tags = []
    obj = []

    if(stdin == 'help'):
        print('FUNCTIONS:')
        print('Syntax : [keyword] [tickers] [function]')
        print('Example : pull [FB,MCD,HD, ...] bal_sheet')
        for f in functions:
            print(f)
        return 

    # Parse Keywords
    for k in keywords:
        if(k in stdin):
            sel_keys.append(k) 

    # Parse Input Object
    for sk in sel_keys:
        index = stdin.index(sk) + len(sk)
        obj_index = index + 1
        # User has provided a list
        if(stdin[obj_index] == '['):
            sentinel = ']'
            for i, c in enumerate(stdin[obj_index:]):
                if(c == sentinel):
                    # Grab raw string of list object
                    raw = stdin[obj_index:obj_index + (i + 1)]
                    # Parse raw string with delimiters
                    delimiters = ["'", " ", "[", "]"]
                    for d in delimiters:
                        raw = raw.replace(d, '') 
                    # Create list
                    obj = raw.split(',')
                    break
        #User has provided a single ticker 
        else: 
            sentinel = ' '
            for i, c in enumerate(stdin[obj_index:]):
                # String contains tags after object
                if(c == sentinel):
                    obj.append(stdin[obj_index:obj_index + (i + 1)])
                    break
                # String only contains keyword and object
                else:
                    obj.append(stdin[obj_index:])
                    break
    
    for k in sel_keys:
        if(k == 'pull'):
            for f in functions:
                if(f in stdin):
                    if(len(obj) > 1):
                        output = []
                        for o in obj:
                            output += [functions[f](o)]
                        return output
                    else:
                        return functions[f](obj)
                    


if __name__ == '__main__':
    print("--- stock-py v{} ---".format(version))
    while(True):
        stdin = input("> ")
        output = parseInput(stdin)
        if isinstance(output, list):
            pprint.pprint(output)
        elif output != None: 
            print(output)
        print('')