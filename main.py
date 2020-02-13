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
        return obj

    # if(sel_keys[0] == 'pull'):
    #     if(len(sel_tags) > 0):

    # # Parse Tags
    # for t in tags:
    #     if(t in stdin):
    #         sel_tags.append(t) 



if __name__ == '__main__':
    print("--- stock-py v{} ---".format(version))
    while(True):
        stdin = input("> ")
        print(parseInput(stdin))
