#dogetweetbot.py
# -*- coding: iso-8859-15 -*-
import tweepy
import time, datetime, calendar
import json, urllib2
import string
from pricestreamer import Streamer
from dbwrapper import Wrapper

class DogePriceBot:
	# Consumer keys and access tokens, used for OAuth
	consumer_key = 'Mhy5lNERB3dTkT3wcWeFGw'
	consumer_secret = 'ozX3svU54uif0bZWn1jt0DrQwSmHoAWnh0ZToBYVFI'
	access_token = '2409405422-JOZnjcCh4ZiMngnT6x0tEAKRSf9iq8s6nPZoDyr'
	access_token_secret = 'o3xl4L4WTIFZGlAjUmlylClAVNNJf49OyvCuhdtnsvt83'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	# Sample method, used to update a status
	# api.update_status("Hello twitter, from dogetweetbot!")

	#Creates the user object. The me() method returns the user whose authentication keys were used
	#user = api.me()
	#print('Name: ', user.name)
	#print('Friends: ', user.friends_count)

	#Instatiation of the Dogestreamer object
	streamer = Streamer()
	db = Wrapper()

	currenttime = 0
	lasttime = 0
	dogebtc = usdbtc = dogeusd = usddoge = 0
	last_hour_dogebtc = last_hour_usdbtc = last_hour_usddoge = 0

	def __init__(self):
		self.currenttime = datetime.datetime.now().replace(microsecond=0)
		#Need to update database for minute column
		last_hour_tweet = self.db.c.execute("SELECT * FROM dogePrices ORDER BY month DESC, day DESC, hour DESC").fetchone()
		self.lasttime = datetime.datetime(last_hour_tweet[0], last_hour_tweet[1], last_hour_tweet[2], last_hour_tweet[3], last_hour_tweet[4], second=0, microsecond=0)
		self.last_hour_dogebtc = last_hour_tweet[5]
		self.last_hour_usddoge = last_hour_tweet[6]
		self.last_hour_usdbtc = last_hour_tweet[7]
		self.update_prices()

	def percent_change(self, new, old):
		change = (float(new)-float(old))/float(old)
		if change >= 0.000:
			return "+"+'%.1f' % abs(change*100)+'%'
		else:
			return '%.1f' % (change*100)+'%'

	def set_prices(self, dogebtc, usddoge, usdbtc):
		self.dogebtc = dogebtc
		#self.dogeusd = dogeusd
		self.usddoge = usddoge
		self.usdbtc = usdbtc
		self.format_prices()

	def update_prices(self):
		#Getting updated doge prices
		self.currenttime = datetime.datetime.now().replace(microsecond=0)
		self.streamer.update_prices()
		self.dogebtc = self.streamer.avg_btcdoge()
		self.usdbtc = self.streamer.btc_to('USD')
		self.usddoge = float(self.dogebtc)*float(self.usdbtc)
		#self.dogeusd = 1/self.usddoge
		self.format_prices()

	def format_prices(self):
		self.dogebtc = '%.8f' % self.dogebtc
		self.usdbtc = '%.2f' % self.usdbtc
		#self.dogeusd = '%.2f' % self.dogeusd
		self.usddoge = '%.6f' % self.usddoge

	def default_tweet(self):
		return '[%s EST]: The average dogecoin price is now %.2f μBTC ($%.6f).' \
		% (datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'), self.dogebtc/0.000001, self.usddoge)

	def __str__(self):
		return 'Current ['+str(self.currenttime)+']:'+'\n'+str(self.dogebtc)+'  DOGE:BTC'+'\n'+\
			   '$'+str(self.usddoge)+'   USD:DOGE'+'\n'+\
			   '$'+str(self.usdbtc)+'     USD:BTC'+'\n'+'\n'+\
			   'Last ['+str(self.lasttime)+']:'+'\n'+str(self.last_hour_dogebtc)+'  DOGE:BTC'+'\n'+\
			   '$'+str(self.last_hour_usddoge)+'   USD:DOGE'+'\n'+\
			   '$'+str(self.last_hour_usdbtc)+'     USD:BTC'
			   #'D'+str(self.dogeusd)+'    DOGE:USD'+'\n'+\
			   
	def hourly_update(self):
		status = self.default_tweet()
		print ''
		#Comment out when testing
		#self.api.update_status(status)
		#print 'Tweet posted:'
		print status
			  #'D'+self.dogeusd+'  DOGE:$', self.percent_change(self.dogeusd, self.last_hour_dogeusd)+'\n'+\
		print ''
		print 'Updating price database...'
		self.db.update_price_DB(self.currenttime, self.dogebtc, self.usddoge, self.usdbtc)
		print '...done'
		print ''
		last_hour_tweet = self.db.c.execute("SELECT * FROM dogePrices ORDER BY month DESC, day DESC, hour DESC").fetchone()
		self.lasttime = datetime.datetime(last_hour_tweet[0], last_hour_tweet[1], last_hour_tweet[2], last_hour_tweet[3], last_hour_tweet[4], second=0, microsecond=0)
		self.last_hour_dogebtc = last_hour_tweet[5]
		self.last_hour_usddoge = last_hour_tweet[6]
		self.last_hour_usdbtc = last_hour_tweet[7]
			  
	def convert(self):
		replys = self.db.c.execute("SELECT * FROM replyIDs").fetchall()
		ids = [reply[1] for reply in replys]

		for mention in self.api.mentions_timeline():
			user = mention.user.screen_name
			if user == "dogepricebot":
				continue
			amount = 0
			#First check to see if we've replied to this tweet before
			if mention.id not in ids:
				#Next, check to see if they have the word 'convert' in the tweet
				if 'convert' in mention.text.lower():
					#Split the words into a list
					words = mention.text.split(" ")
					currency = ''
					for word in words:
						#Parse through the list looking for a numeric amount and a currency code
						if word.isnumeric() == True:
							amount = float(word)
						if word.upper() in self.streamer.currency_codes:
							currency = word
					if currency not in self.streamer.currency_codes:
						tweet = '@%s such sorry! either invalid currency code or I don\'t yet support that currency'
						print tweet
						self.api.update_status(tweet, mention.id)
						self.db.update_id_DB(user, mention.id)
					else:
						if amount != 0:
							#Direct exchange rate
							if 'doge to' in mention.text.lower() or 'dogecoins to' in mention.text.lower() or 'dogecoin to' in mention.text.lower():
								tweet = '@%s wow such convert: %.1f #dogecoin = %.2f %s' % (user, float(amount), float(amount)*float(self.dogebtc)*float(self.streamer.btc_to(currency)), currency)
								print tweet
								self.api.update_status(tweet, mention.id)
								self.db.update_id_DB(user, mention.id)
							#Indirect exchange rate
							elif 'to doge' in mention.text.lower() or 'to dogecoins' in mention.text.lower() or 'to dogecoin' in mention.text.lower():
								tweet = '@%s wow such convert: %.1f %s = %.2f #dogecoin' % (user, float(amount), currency, float(amount)/float(self.streamer.btc_to(currency))/float(self.dogebtc))
								print tweet
								self.api.update_status(tweet, mention.id)
								self.db.update_id_DB(user, mention.id)
			else:
				print 'Duplicate tweet, skipping'

	def stream(self):
		while True:
			try:
				print 'Replying to conversion requests:'
				self.convert()
				print '...done'
				print ''
				self.update_prices()
				print 'Current time:', self.currenttime
				print 'Last tweeted:', self.lasttime
				if (self.currenttime - self.lasttime).seconds/3600 >= 1:
					print 'Hour has passed, updating now'
					self.hourly_update()
				else:
					print self.currenttime, 'Hour has not yet passed'
			#if new hour, hourly_update()
			#if 5pm, daily_update()
			except Exception, e:
				print str(e)
			#Sleep for an hour
			print 'Sleeping for 10 minutes...'
			print ''
			time.sleep(600)

if __name__ == "__main__":
	bot = DogePriceBot()
	bot.stream()
