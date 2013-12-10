#coding: utf-8
from datetime import datetime, timedelta
import time

import api

access_key="f6322647-43a3-461f-a2f8-85fcfa1881ac"
secret_key="6b0d21c3-bf2f-4e6f-86cc-a7f66c4cd451"
btc_balance = {}
cny_balance = {} 
bc = api.BTCChina(access_key,secret_key)

def log(txt, level='info'):
    f = file('log.txt', 'a+')
    content = '%s:%s' % (str(datetime.now()), txt)
    if level != 'info':
        print content
    f.write(content + "\n")
    f.close()

def get_price_from_depth(infos):
    total = 0
    amount = 0
    for info in infos:
        total += info['price'] * info['amount']
        amount += info['amount']
    price =  total / amount
    log(price)
    return price

def get_balance():
    global btc_balance, cny_balance
    try:
        account_info = bc.get_account_info()
    except:
        account_info = None
    if account_info:
        btc_balance = account_info['balance']['btc']
        btc_balance['amount'] = float(btc_balance['amount'])
        cny_balance = account_info['balance']['cny']
        cny_balance['amount'] = float(cny_balance['amount'])

def legal_number(num):
    return "%.4f" % num

def sell(price):
    btc_amount = btc_balance['amount']
    log("[sell]%f,%f" % (btc_amount, price), 'warning')
    if btc_amount:
        try:
            bc.sell(legal_number(price), legal_number(btc_amount))
        except:
            pass



if __name__ == "__main__":
	get_balance()
	sell(300)
