from tradingview_ta import TA_Handler, Interval, Exchange
import time
from datetime import datetime
import pandas as pd
from binance.client import Client
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail.content import Content
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)


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

def mail_csv(file):
    topsecret = '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'
    message = Mail(
    from_email='stijnvanleeuwen3@gmail.com',
    to_emails='stijnvanleeuwen3@gmail.com',
    subject='TradinView CSV',
    html_content='<p>weet ik veel</p>'
    )

    with open(file, 'rb') as f:
        data = f.read()
        f.close()

    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(file),
        FileType('application/csv'),
        Disposition('attachment')
    )
    message.attachment = attachedFile
    sg = SendGridAPIClient(topsecret)
    response = sg.send(message)
    bericht = 'Mail verstuurd! :)' if response.status_code==202 else 'Error met mail'
    print(bericht)


lol = {}
for i in range(1000000):
    start = time.time()
    date = get_date()
    lol[date] = get_main()
    print(date)
    main = pd.DataFrame(lol).transpose()
    took = time.time() - start
    main.to_csv('hoho.csv')
    time.sleep(2)
    if int(i) % 4 == 0:
        mail_csv('hoho.csv')
    
    #print(lol[date])
    time.sleep(20-took)
