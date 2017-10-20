from urllib2 import Request, urlopen
import json
import time
import pandas as pd
from datetime import datetime

pd.options.display.float_format = '{:,.8f}'.format # 

ETH = """
  {
        "exchange_code": "BITS",
        "exchange_market": "ETH/BTC"
    }
"""

LTC = """
  {
        "exchange_code": "BITS",
        "exchange_market": "LTC/BTC"
    }
"""

DASH = """
  {
        "exchange_code": "BTRX",
        "exchange_market": "DASH/BTC"
    }
"""

ZEC = """
  {
        "exchange_code": "BTRX",
        "exchange_market": "ZEC/BTC"
    }
"""
headers = {
  'Content-Type': 'application/json',
  'X-API-KEY': 'f4d54af4b45105f9ddd4d0c6447c160e',
  'X-API-SECRET': 'd0a13966bb8f9661d8795b551301f4ad'
}


def send(coin):
    request = Request('https://api.coinigy.com/api/v1/ticker', data = ETH, headers=headers)
    req = urlopen(request)
    date = datetime.strptime(req.info().getheader('date')[5:25], '%d %b %Y %H:%M:%S')
    response_body = req.read()
    a = json.loads(response_body)
    return pd.DataFrame({'bids':[float(a["data"][0]["bid"])], 'asks':[float(a["data"][0]["ask"])]}, index = [date]) 

print 2

pricesETH = pd.DataFrame({'asks':[], 'bids':[]})
pricesLTC = pd.DataFrame({'asks':[], 'bids':[]})
pricesDASH = pd.DataFrame({'asks':[], 'bids':[]})
pricesZEC = pd.DataFrame({'asks':[], 'bids':[]})

# print prices
sec = 0

while sec < 10*60:
    pricesETH = pricesETH.append(send(ETH))
    pricesLTC = pricesLTC.append(send(LTC))
    pricesDASH = pricesDASH.append(send(DASH))
    pricesZEC = pricesZEC.append(send(ZEC))
    
    time.sleep(2) # 2 second
    sec += 2
    print sec


pricesETH = pricesETH.resample('20S').mean() # prices.resample('20S').mean()
pricesLTC = pricesLTC.resample('20S').mean() # prices.resample('20S').mean()
pricesDASH = pricesDASH.resample('10S').mean() # prices.resample('20S').mean()
pricesZEC = pricesZEC.resample('10S').mean() # prices.resample('20S').mean()
    
    
Asks = pd.concat([pricesETH['asks'], pricesLTC['asks'],pricesDASH['asks'], pricesZEC['asks']], axis=1, keys=['ETH', 'LTC', 'DASH', 'ZEC'])    
Bids = pd.concat([pricesETH['bids'], pricesLTC['bids'],pricesDASH['bids'], pricesZEC['bids']], axis=1, keys=['ETH', 'LTC', 'DASH', 'ZEC'])    

print Asks.corr()
print Bids.corr()
