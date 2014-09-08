#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
from assembler import Assembler
from datetime import datetime
from dbwrapper import Wrapper

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

	def __init__(self):
		self.assembler = Assembler()
		self.wrapper = Wrapper()
	
	def priceupdate(self, base, mid, quote):
		timestamp = datetime.fromtimestamp(time.time())
		rates = self.assembler.assemble(base, mid, quote)
		base_per_mid, mid_per_quote = rates[0], rates[1]
		self.wrapper.update_price_db(timestamp, base_per_mid, mid_per_quote)
		return '[%s CST]: The average dogecoin price is now %.2f bits ($%.6f) #dogepricebottest' \
		% (timestamp.strftime('%m-%d %H:%M'), base_per_mid*(1000000), base_per_mid*mid_per_quote)
		#return '[%s CST]: The average dogecoin price is now %.2f bits ($%.6f).\n$1 = Ð%.2f\n1BTC = Ð%d' % (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), dogebtcprice, dogeusdprice, 1/dogeusdprice, dogebtcprice*100000)

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		while True:
			try:
				tweet = self.priceupdate('DOGE', 'BTC', 'USD')
#				self.api.update_status(tweet)
				print tweet
				print 'Tweeted successfully'
			except Exception, e:
				print str(e)
			time.sleep(3570)

if __name__ == "__main__":
	bot = Streamer()
	bot.stream()
