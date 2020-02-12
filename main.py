import stock_pull as pull
import json_test as store 

version = 1.0
stdin = ''

# All core functions
keywords = [
    'pull',
]

# All additional functions 
tags = [
    '-a' # Analysis
]

# All forms of analysis
analysis = [
    'btm'
]

def parseInput(stdin):
    sel_keys = []
    sel_tags = []
    obj = []

    # Parse Keywords
    for k in keywords:
        if(k in stdin):
            sel_keys.append(k) 

    # Remove all spaces from string

    # Parse Input Object
    for sk in sel_keys:
        index = stdin.index(sk) + len(sk)
        obj_index = index + 1
        # User has provided a list
        if(stdin[obj_index] == '['):
            sentinel = ']'
            for i, c in enumerate(stdin[obj_index:]):
                if(c == ']'):
                    raw = stdin[obj_index:obj_index + (i + 1)]
                    delimiters = ["'", " ", "[", "]"]
                    for d in delimiters:
                        raw = raw.replace(d, '') 
                    obj = raw.split(',')
                    return obj
        #User has provided a single ticker 
        else: 
           print("fish") 

    # Parse Tags
    for t in tags:
        if(t in stdin):
            sel_tags.append(t) 



    # if(sel_keys[0] == 'pull'):
    #     if(len(sel_tags) > 0):


if __name__ == '__main__':
    print("--- stock-py v{} ---".format(version))
    stdin = input("> ")
    print(parseInput(stdin))
