import stock_pull as pull
import json_test as store 

version = 1.0
stdin = ''

keywords = [
    'pull',
]

tags = [
    '-a' # Analysis
]

analysis = [
    'btm'
]

def parseInput(stdin):
    def parseTags():
        pass

    sel_keys = ['']
    sel_tags = ['']
    for k in keywords:
        if(k in stdin):
            sel_keys.append(k) 

    if(sel_keys[0] == 'pull'):
        if(len(sel_tags) > 0):
    pass

    # for t in tags:
    #     if(t in stdin):
    #         sel_tags.append(t) 
    # pass


if __name__ == '__main__':
    print("--- stock-py v{} ---".format(version))
    stdin = input("> ")
    print(parseInput(stdin))
