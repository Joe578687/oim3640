import yfinance as yf

# stock = yf.Ticker("AAPL")
# info = stock.info
# print(type(info))

# print(info.keys())
# print(len(info))
# print(info['longName'])
# print(info['shortName'])
# print(info['currentPrice'])

# # print(info['longBusinessSummary'])

# print(info['longBusinessSummary'].split())
# print('iPhone' in info['longBusinessSummary'])

# print('iPhone' in info['longBusinessSummary'])

# print(info['city'])
# # info['city'][0] = 'c'
# info['city'] = 'Wellesley'
# print(info['city'])

# info['founder'] = 'Robert'
# print(info['founder'])


# for k, v in info.items():
#     print(k, v)

tickers = ["AAPL", "NVDA", "MSFT"]
prices = {}
for t in tickers:
    prices[t] = yf.Ticker(t).info['currentPrice']

    print(prices)

print(sorted(prices)) # create a new list of the keys in prices, sorted alphabetically
print(sorted(prices.values()))
print(sorted(prices.values(), reverse=True)) # sort the values in descending order

# how to sort sotkcs by values, but still to show k: v ?

#print(tickers)

# prices = {'AAPL':{152.53, 300}, 'NVDA':{174.33, 200}, 'MSFT':{372.845, 500}}
print(sum(prices.values()))

total = 0
for price in prices.values():
    total += price
print(total)

tickers.append('GOOG')
print(tickers)
tickers = {}
for t in tickers:
    prices[t] = yf.Ticker(t).info['currentPrice']
    print(prices)


tickers = ['AAPL', 'NVDA', 'MSFT', 'META']
stocks = {} # {'NVDA': [price, open, currentPrice, volume]}

for t in tickers:
    # stocks[t] = (yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume']) # create a tuple
    # stocks[t] = [yf.Ticker(t).info['open'], yf.Ticker(t).info['currentPrice'], yf.Ticker(t).info['volume']] # create a lsit
    info_list = {}
    for name in ['open', 'currentPrice', 'volume']:
        info_list[name] = yf.Ticker(t).info[name]
        stocks[t] = info_list


stocks['AAPL']['currentPrice'] = 260
print(stocks)
