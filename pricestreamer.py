#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
import json
import urllib2
from urllib2 import urlopen
from datetime import datetime
import cookielib
from cookielib import CookieJar
import CryptoCoinChartsApi
from CryptoCoinChartsApi import API

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

class Streamer:
	#Global variables
	consumer_key = 'Mhy5lNERB3dTkT3wcWeFGw'
	consumer_secret = 'ozX3svU54uif0bZWn1jt0DrQwSmHoAWnh0ZToBYVFI'
	access_token = '2409405422-JOZnjcCh4ZiMngnT6x0tEAKRSf9iq8s6nPZoDyr'
	access_token_secret = 'o3xl4L4WTIFZGlAjUmlylClAVNNJf49OyvCuhdtnsvt83'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)
	cryptsy, bter, vrex, usdbtc, avg_dogeusd = 0, 0, 0, 0, 0
	currency_codes = ['AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'EUR', 'GBP', 'HKD', \
						  'ILS', 'JPY', 'NOK', 'NZD', 'PLN', 'RUB', 'SEK', 'SGD', \
						  'TRY', 'USD', 'ZAR']
	#Expanding to other cryptocurrencies
	cryptocurrency_codes = []

	def __init__(self):
		self.update_prices()

	def update_prices(self):
		self.cryptsy = self.btcdoge_cryptsy()
		self.bter = self.btcdoge_bter()
		#self.cup = self.btcdoge_coinedup()
		self.vrex = self.btcdoge_vircurex()
		self.usdbtc = self.btc_to('USD')
		self.avg = self.avg_btcdoge()

	def btcdoge_cryptsy(self):
		#GET DOGE/BTC prices from cryptsy using JSON
		cryptsy_dogePrices = opener.open('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132')
		cryptsy_dogejson = json.load(cryptsy_dogePrices)
		cryptsy_dogelastP = cryptsy_dogejson['return']['markets']['DOGE']['lasttradeprice']
		return float(cryptsy_dogelastP)

	def btcdoge_bter(self):
		#GET DOGE prices from Bter using JSON
		bter_dogePrices = opener.open('http://data.bter.com/api/1/trade/doge_btc')
		bter_dogejson = json.load(bter_dogePrices)
		bter_dogelastP = bter_dogejson['data'][0]['price']
		return float(bter_dogelastP)

	#def btcdoge_coinedup(self):
		#GET DOGE prices from CoinedUp using wrapper API
	#	coinedup_api = API()
	#	pair = 'doge_btc'
	#	coinedup_dogelastP = coinedup_api.tradingpair(pair).price
	#	return float(coinedup_dogelastP)

	def btcdoge_vircurex(self):
		vrex_dogejson = json.load(opener.open('https://api.vircurex.com/api/get_info_for_1_currency.json?base=DOGE&alt=BTC'))
		vrex_dogelastP = vrex_dogejson['last_trade']
		return float(vrex_dogelastP)

	def avg_btcdoge(self):
		btcdogeprices = [self.btcdoge_bter(), self.btcdoge_cryptsy(), self.btcdoge_vircurex()]
		average = sum(btcdogeprices)/len(btcdogeprices)
		return average

#BTC Exchange prices
#Refactored to work with Bitcoin Average website
	
	def btc_to(self, ticker):
		btc_json = json.load(opener.open('https://api.bitcoinaverage.com/ticker/'+ticker))
		btc_rate = btc_json['last']
		return btc_rate

	def priceupdate(self):
		self.update_prices()
		dogebtcprice = self.avg/0.000001
		dogeusdprice = self.avg*self.btc_to('USD')
		return '[%s EST]: The average dogecoin price is now %.2f μBTC ($%.6f).\n$1 = Ð%.2f\n1BTC = Ð%d' % (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), dogebtcprice, dogeusdprice, 1/dogeusdprice, dogebtcprice*100000)

	def __str__(self):
		return '[%s EST]: The average dogecoin price is now %.2f bits ($%.7f).' \
		% (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), self.avg/0.000001, self.avg*self.btc_to('USD'))

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		while True:
			try:
				self.api.update_status(self.priceupdate())
			except Exception, e:
				print str(e)
			time.sleep(3600)
