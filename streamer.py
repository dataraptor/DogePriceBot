#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
from assembler import Assembler
from datetime import datetime

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

	currency_codes = ['AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'EUR', 'GBP', 'HKD', \
					  'ILS', 'JPY', 'NOK', 'NZD', 'PLN', 'RUB', 'SEK', 'SGD', \
					  'TRY', 'USD', 'ZAR']
	#Expanding to other cryptocurrencies in v1.7
	cryptocurrency_codes = []

	def __init__(self):
		self.assembler = Assembler()

	def main(self):
		if __name__ == "__main__":
			self.stream()
	
	def priceupdate(self, quote):
		rates = self.assembler.assemble(quote)
		dogebtc, btcusd = rates[0], rates[1]
		return '[%s CST]: The average dogecoin price is now %.2f bits ($%.6f) #dogepricebottest' \
		% (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M'), dogebtc*(1000000), dogebtc*btcusd)
		#return '[%s CST]: The average dogecoin price is now %.2f bits ($%.6f).\n$1 = Ð%.2f\n1BTC = Ð%d' % (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), dogebtcprice, dogeusdprice, 1/dogeusdprice, dogebtcprice*100000)

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		while True:
			try:
				self.api.update_status(self.priceupdate('USD'))
				print 'Tweeted successfully'
			except Exception, e:
				print str(e)
			time.sleep(3570)
