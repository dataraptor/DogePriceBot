#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import json
import urllib2
from urllib2 import urlopen
import datetime
import cookielib
from cookielib import CookieJar
import CryptoCoinChartsApi
from CryptoCoinChartsApi import API

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]


class DogePriceStreamer:
	#Global variables
	cryptsy, bter, cup, vrex, usdbtc, avg_dogeusd = 0, 0, 0, 0, 0, 0

	def __init__(self):
		self.update_prices()

	#def get_btcdoge_prices(self):
		#RETURN prices in list [bter, cup, cryptsy, average, usdbtc]
		#return [self.bter, self.cup, self.cryptsy, self.avg_dogebtc, self.usdbtc]

	def update_prices(self):
		self.cryptsy = self.btcdoge_cryptsy()
		self.bter = self.btcdoge_bter()
		self.cup = self.btcdoge_coinedup()
		self.vrex = self.btcdoge_vircurex()
		self.usdbtc = self.btc_to('USD')
		self.avg_dogebtc = self.avg_btcdoge()

#BTC:DOGE Exchange prices

	def btcdoge_cryptsy(self):
		#GET DOGE/BTC prices from cryptsy using JSON
		cryptsy_dogePrices = opener.open('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132')
		cryptsy_dogejson = json.load(cryptsy_dogePrices)
		cryptsy_dogelastP = cryptsy_dogejson['return']['markets']['DOGE']['lasttradeprice']
		cryptsy_dogelastT = cryptsy_dogejson['return']['markets']['DOGE']['lasttradetime']
		return cryptsy_dogelastP

	def btcdoge_bter(self):
		#GET DOGE prices from Bter using JSON
		bter_dogePrices = opener.open('http://data.bter.com/api/1/trade/doge_btc')
		bter_dogejson = json.load(bter_dogePrices)
		bter_dogelastP = bter_dogejson['data'][0]['price']
		bter_dogelastT = bter_dogejson['data'][0]['date']
		bter_dogelastT = datetime.datetime.fromtimestamp(int(bter_dogelastT)).strftime('%Y-%m-%d %H:%M:%S')
		return bter_dogelastP

	def btcdoge_coinedup(self):
		#GET DOGE prices from CoinedUp using wrapper API
		coinedup_api = API()
		pair = 'doge_btc'
		coinedup_dogelastP = coinedup_api.tradingpair(pair).price
		return coinedup_dogelastP

	def btcdoge_vircurex(self):
		vrex_dogejson = json.load(opener.open('https://api.vircurex.com/api/get_info_for_1_currency.json?base=DOGE&alt=BTC'))
		vrex_dogelastP = vrex_dogejson['last_trade']
		return vrex_dogelastP

	def avg_btcdoge(self):
		btcdogeprices = []
		btcdogeprices.extend([self.btcdoge_bter(), self.btcdoge_coinedup(), self.btcdoge_cryptsy(), self.btcdoge_vircurex()])
		average = reduce(lambda x, y: float(x) + float(y), btcdogeprices)/len(btcdogeprices)
		return average

#BTC Exchange prices
#Refactored to work with Bitcoin Average website
	
	def btc_to(self, ticker):
		currency_codes = ['AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'EUR', 'GBP', 'HKD', \
						  'ILS', 'JPY', 'NOK', 'NZD', 'PLN', 'RUB', 'SEK', 'SGD', \
						  'TRY', 'USD', 'ZAR']
		if len(ticker) > 3 or len(ticker) < 3:
			print 'Invalid currency code.'
		elif ticker not in currency_codes:
			print 'Do not yet support this currency.'
		else:
			btc_json = json.load(opener.open('https://api.bitcoinaverage.com/ticker/'+ticker))
			btc_rate = btc_json['last']
			btc_vol = btc_json['total_vol']
			btc_ask = btc_json['ask']
			btc_bid = btc_json['bid']
			btc_spread = btc_ask - btc_bid
			return btc_rate

#DOGE:USD Exchange prices

	def usddoge_crypsty(self):
		cryptsy_dogePrices = opener.open('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=182')
		cryptsy_dogejson = json.load(cryptsy_dogePrices)
		cryptsy_dogelastP = cryptsy_dogejson['return']['markets']['DOGE']['lasttradeprice']
		cryptsy_dogelastT = cryptsy_dogejson['return']['markets']['DOGE']['lasttradetime']
		return cryptsy_dogelastP

	def __str__(self):
		return 'TIME:     '+str(datetime.datetime.now().replace(microsecond=0))+'\n'+\
		       'BTER:     '+str(self.bter)+' : $'+str(self.usdbtc)+' : $'+str(float(self.bter)*self.usdbtc)+'\n'+\
			   'COINEDUP: '+str(self.cup)+' : $'+str(self.usdbtc)+' : $'+str(float(self.cup)*self.usdbtc)+'\n'+\
			   'CRYPTSY:  '+str(self.cryptsy)+' : $'+str(self.usdbtc)+' : $'+str(float(self.cryptsy)*self.usdbtc)+'\n'+\
			   'VIRCUREX:  '+str(self.vrex)+' : $'+str(self.usdbtc)+' : $'+str(float(self.vrex)*self.usdbtc)+'\n'+\
			   'AVERAGE:  '+str(self.avg_dogebtc)+' : $'+str(self.usdbtc)+' : $'+str(float(self.avg_dogebtc)*self.usdbtc)

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		print '          DOGE/BTC:  BTC/USD:  DOGE/USD'
		while True:
			try:
				self.update_prices()
				print self
			except Exception, e:
				print str(e)
			time.sleep(10)