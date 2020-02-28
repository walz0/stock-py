import stock_pull as pull
import util

"""
    Takes a list of tickers and calculates ROIC / Earnings Yield
    for all of them.
    Returns a ranked ascending list of stocks based upon 
    ROIC / Earnings Yield. 
"""
def btm (tickers):
    stats = []

    for ticker in tickers:
        roic = pull.getROIC(ticker)
        if(roic != None):
            roic = str(round(pull.getROIC(ticker), 4) * 100)[0:5]
        else:
            roic = str(roic)
        pe = pull.getPE(ticker)
        if(pe != 0):
            earningsYield = 1 / pe
        else:
            earningsYield = 0
        stats.append([ticker, roic, earningsYield])
        print("{}% Complete...".format(len(stats) / len(tickers)))

    roic_stats = util.sortList(stats, 1, util.Order.descending)
    ey_stats = util.sortList(stats, 2, util.Order.descending) 

    rank = []
    for i, s in enumerate(roic_stats):
        rank.append([roic_stats[i][0], str(roic_stats[i][1]) + '%', roic_stats[i][2], ey_stats.index(roic_stats[i]) + i])

    rank = util.sortList(rank, 3, util.Order.ascending)

    for i in range(len(rank)):
        r[len(r) - i] = i + 1
    
    return rank

if __name__ == "__main__":
    btm(['FB', 'MCD', 'HD'])
