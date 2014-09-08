import time
import tweepy
import json
import urllib2
from urllib2 import urlopen
from datetime import datetime
import cookielib
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

class Scraper():

	def __init__(self):
		self.update_prices('DOGE', 'BTC')
		self.cryptsy, self.bter, self.vrex = 0, 0, 0

	def get_prices(self, base, quote):
		self.update_prices(base, quote)
		return [self.cryptsy, self.bter, self.vrex]

	def update_prices(self, base, quote):
		self.cryptsy = self.get_cryptsy(base)
		self.bter = self.get_bter(base)
		self.vrex = self.get_vrex(base)
		
	def get_cryptsy(self, base):
		url = 'http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132'
		market = json.load(opener.open(url))
		lastprice = float(market['return']['markets'][base]['lasttradeprice'])
		return lastprice

	def get_bter(self, base):
		url = 'http://data.bter.com/api/1/trade/%s_btc' % (base)
		market = json.load(opener.open(url))
		lastprice = float(market['data'][0]['price'])
		return lastprice

	def get_vrex(self, base):
		url = 'https://api.vircurex.com/api/get_info_for_1_currency.json?base=%s&alt=BTC' % (base)
		market = json.load(opener.open(url))
		lastprice = float(market['last_trade'])
		return lastprice