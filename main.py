#coding: utf-8
from datetime import datetime, timedelta
import time

import api

access_key="YOUR_ACCESS_KEY"
secret_key="YOUR_SECRET_KEY"
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

def buy(price):
    btc_amount = cny_balance['amount'] / price
    log("[buy]%f,%f" % (btc_amount, price), 'warning')
    try:
        bc.buy(legal_number(price), legal_number(btc_amount))
    except:
        pass
    return


def sell(price):
    btc_amount = btc_balance['amount']
    log("[sell]%f,%f" % (btc_amount, price), 'warning')
    if btc_amount:
        try:
            bc.sell(legal_number(price), legal_number(btc_amount))
        except:
            pass

def trading_analysis():
	old_buy_price = 0
	old_sell_price = 0
	up_count = 0
	down_count = 0
	while True:
		bids = []
		asks = []
		try:
			markets = bc.get_market_depth()
			bids = markets['market_depth']['bid']
			asks = markets['market_depth']['ask']
		except:
			markets = {'market_depth':[]}
		new_buy_price = get_price_from_depth(bids)
		new_sell_price = get_price_from_depth(asks)
		
		sum_bid_amount = 0
		sum_ask_amount = 0
		for bid in bids:
			sum_bid_amount = sum_bid_amount + bid['amount']
		for ask in asks:
			sum_ask_amount = sum_ask_amount + ask['amount']
		
		if old_buy_price > 0  and old_sell_price > 0:
			buy_price_rate = new_buy_price / old_buy_price
			sell_price_rate = new_sell_price / old_sell_price
			print 'buy_price_rate: ',float(buy_price_rate),' sell_price_rate: ',float(sell_price_rate)
			print 'new_buy_price: ',float(new_buy_price),' new_sell_price: ',float(new_sell_price)
			if sum_bid_amount > sum_ask_amount * 4 and buy_price_rate > 1 and sell_price_rate > 1:
				up_count = up_count + 1
				down_count = 0
			if sum_ask_amount > sum_bid_amount * 4 and buy_price_rate < 1 and sell_price_rate < 1:
				down_count = down_count + 1
				up_count = 0
		print 'up_count: ',float(up_count),' down_count',float(down_count)

		buy_price = 0
		if up_count > 3 and down_count > 100:
			up_count = 0
			down_count = 0
			buy_price = new_buy_price + 50 
			buy(new_buy_price)
		sell_price = 0
		if down_count > 3 and up_count > 100:
			up_count = 0
			down_count = 0
			sell_price = new_sell_price - 50 
			sell(sell_price)
		print 'buy: ',float(sum_bid_amount),' sell: ',float(sum_ask_amount)
		old_buy_price = new_buy_price
		old_sell_price = new_sell_price
		time.sleep(5)

if __name__ == "__main__":
	get_balance()
	trading_analysis()
