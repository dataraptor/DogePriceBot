#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
from assembler import Assembler
from datetime import datetime
from dbwrapper import Wrapper

class Streamer:
	#Global variables
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''

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
		last_update = self.wrapper.c.execute("SELECT * FROM Prices ORDER BY month DESC, day DESC, hour DESC").fetchone()
		new_price = base_per_mid*mid_per_quote
		last_price = last_update[5]*last_update[6]
		delta = new_price/last_price - 1
		self.wrapper.update_price_db(timestamp, base_per_mid, mid_per_quote)
		if delta >= 0:
			return '[%s CST]: The average #dogecoin price is now $%.6f, +%.1f%% growth wow (%.2f bits)' \
			% (timestamp.strftime('%m-%d %H:%M'), new_price, delta*100, base_per_mid*(1000000))
		else:
			return '[%s CST]: The average #dogecoin price is now $%.6f, %.1f%% decline (%.2f bits)' \
			% (timestamp.strftime('%m-%d %H:%M'), new_price, delta*100, base_per_mid*(1000000))	
		
		#return '[%s CST]: The average #dogecoin price is now $%.6f (%.2f bits)' \
		#% (timestamp.strftime('%m-%d %H:%M'), new_price, base_per_mid*(1000000))
		#return '[%s CST]: The average dogecoin price is now %.2f bits ($%.6f).\n$1 = Ð%.2f\n1BTC = Ð%d' % (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), dogebtcprice, dogeusdprice, 1/dogeusdprice, dogebtcprice*100000)

	#Continuous price stream
	def stream(self):
		print 'Initiating Dogecoin Price Stream --------------------------'
		while True:
			try:
				tweet = self.priceupdate('DOGE', 'BTC', 'USD')
				self.api.update_status(tweet)
				print tweet
				print 'Tweeted successfully'
			except Exception, e:
				print str(e)
			time.sleep(3570)

if __name__ == "__main__":
	bot = Streamer()
	bot.stream()
