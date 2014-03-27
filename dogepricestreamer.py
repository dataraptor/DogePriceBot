#dogestreamer.py
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
	cryptsy = 0
	bter = 0
	cup = 0
	usdbtc = 0
	avg_dogeusd = 0

	def __init__(self):
		self.cryptsy = self.cryptsy_price()
		self.bter = self.bter_price()
		self.cup = self.cup_price()
		self.usdbtc = float(self.BTC_price())
		self.avg_dogebtc = self.avg_price()

	def get_prices(self):
		#RETURN prices in list [bter, cup, cryptsy, average, usdbtc]
		return [self.bter, self.cup, self.cryptsy, self.avg_dogebtc, self.usdbtc]

	def update_prices(self):
		self.cryptsy = self.cryptsy_price()
		self.bter = self.bter_price()
		self.cup = self.cup_price()
		self.usdbtc = float(self.BTC_price())
		self.avg_dogebtc = self.avg_price()

	def cryptsy_price(self):
		#GET DOGE prices from cryptsy using JSON
		cryptsy_dogePrices = opener.open('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132')
		cryptsy_dogejson = json.load(cryptsy_dogePrices)
		cryptsy_dogelastP = cryptsy_dogejson['return']['markets']['DOGE']['lasttradeprice']
		cryptsy_dogelastT = cryptsy_dogejson['return']['markets']['DOGE']['lasttradetime']
		return cryptsy_dogelastP

	def bter_price(self):
		#GET DOGE prices from Bter using JSON
		bter_dogePrices = opener.open('http://data.bter.com/api/1/trade/doge_btc')
		bter_dogejson = json.load(bter_dogePrices)
		bter_dogelastP = bter_dogejson['data'][0]['price']
		bter_dogelastT = bter_dogejson['data'][0]['date']
		bter_dogelastT = datetime.datetime.fromtimestamp(int(bter_dogelastT)).strftime('%Y-%m-%d %H:%M:%S')
		return bter_dogelastP

	def cup_price(self):
		#GET DOGE prices from CoinedUp using wrapper API
		cup_api = API()
		pair = 'doge_btc'
		cup_dogelastP = cup_api.tradingpair(pair).price
		return cup_dogelastP

	def BTC_price(self):
		#GET BTC prices from btc-e
		btcePrices = urllib2.urlopen('https://btc-e.com/api/2/btc_usd/ticker')
		btcejson = json.load(btcePrices)
		btcelastP = float(btcejson['ticker']['last'])
		return btcelastP

	def avg_price(self):
		#GET time and prices from exchange methods
		dogeprices = []
		dogeprices.extend((self.bter, self.cryptsy, self.cup))
		#AVG prices
		avg_dogelastP = reduce(lambda x, y: float(x) + float(y), dogeprices) / len(dogeprices)
		#RETURN bter, cup, cryptsy, avg
		return avg_dogelastP

	def __str__(self):
		return 'TIME:     '+str(datetime.datetime.now().replace(microsecond=0))+'\n'+\
		       'BTER:     '+str(self.bter)+' : $'+str(self.usdbtc)+' : $'+str(float(self.bter)*self.usdbtc)+'\n'+\
			   'COINEDUP: '+str(self.cup)+' : $'+str(self.usdbtc)+' : $'+str(float(self.cup)*self.usdbtc)+'\n'+\
			   'CRYPTSY:  '+str(self.cryptsy)+' : $'+str(self.usdbtc)+' : $'+str(float(self.cryptsy)*self.usdbtc)+'\n'+\
			   'AVERAGE:  '+str(self.avg_dogebtc)+' : $'+str(self.usdbtc)+' : $'+str(float(self.avg_dogebtc)*self.usdbtc)

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		print '          DOGE/BTC:  BTC/USD:  DOGE/USD'
		while True:
			try:
				print self
			except Exception, e:
				print str(e)
			time.sleep(10)