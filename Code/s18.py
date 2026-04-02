import yfinance as yf
from pprint import pprint #todo: pprint will print a dictionary in a more readable format (after sorting?)

tickers = ['AAPL', 'NVDA', 'MSFT', 'META', 'GOOG']
stocks = {}

for t in tickers:
    stocks[t] = yf.Ticker(t).info['currentPrice'] # create a dictioanry with the current price of each stock
                 
pprint (stocks)

print ('After sorting...')

def sort_by_price(t):
    return t[1] # sort by the second element of the tuple (the price)


print(sorted(stocks.items(), key=lambda t: t[1], reverse=True)) # sort the items in the stocks dictionary by the price in descending order

