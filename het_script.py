from tradingview_ta import TA_Handler, Interval, Exchange
import time
from datetime import datetime
import pandas as pd
from binance.client import Client

def get_binary_ratings(timeframe):
    
    tradingview_data = TA_Handler(
            symbol='BTCUSDT',
            screener='crypto',
            exchange="binance",
            interval=timeframe)

    oscillators = tradingview_data.get_analysis().oscillators['COMPUTE']
    moving_averages = tradingview_data.get_analysis().moving_averages['COMPUTE']
    all_ratings = {**oscillators, **moving_averages}
    all_ratings.keys()

    all_binary_ratings = {}
    for key in all_ratings.keys():
        all_binary_ratings[key+'_BUY'] = int(1 if all_ratings[key]=='BUY' else 0)
        all_binary_ratings[key+'_SELL'] = int(1 if all_ratings[key]=='SELL' else 0)

    return all_binary_ratings


def get_crypto_price(pair):
    api_key = "cjMxAEpqddjxWN8XWmfeBPGM0SO9GEX3Xi15OPkXUOnwttbH7hFw1XLjrZaipvdK"
    api_secret = "XFTvGHHInkTmqp9uJKFMAFR2Xh1b540tItpSpHpat5n33hbk6dXATgPPPhkHExsJ"
    client = Client(api_key, api_secret)  
    return round(float(client.get_orderbook_ticker(symbol=pair)['bidPrice']),1)

def get_main():
    main = {}

    for tf in ['5m','15m','1h','4h','1d']:
        temp = get_binary_ratings(tf)
        emp = {}
        
        for key in temp.keys():
            emp[key+"_"+tf] = temp[key]
        
        main.update(emp)

    main['price'] = get_crypto_price('BTCUSDT')
    return main

def get_date():
    unix = time.time()
    return datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M')

lol = {}
for i in range(1000000):
    start = time.time()
    date = get_date()
    lol[date] = get_main()
    print(date)
    main = pd.DataFrame(lol).transpose()
    took = time.time() - start
    main.to_csv('hoho.csv')
    #print(lol[date])
    time.sleep(60-took)
    
