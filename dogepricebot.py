#dogetweetbot.py
import tweepy
import time, datetime, calendar
import json, urllib2
import string
from dogepricestreamer import DogePriceStreamer
from dogepricebase import DogePriceBase

class DogePriceBot:
	# Consumer keys and access tokens, used for OAuth
	consumer_key = 'Mhy5lNERB3dTkT3wcWeFGw'
	consumer_secret = 'ozX3svU54uif0bZWn1jt0DrQwSmHoAWnh0ZToBYVFI'
	access_token = '2409405422-JOZnjcCh4ZiMngnT6x0tEAKRSf9iq8s6nPZoDyr'
	access_token_secret = 'o3xl4L4WTIFZGlAjUmlylClAVNNJf49OyvCuhdtnsvt83'
	#consumer_key = ''
	#consumer_secret = ''
	#access_token = ''
	#access_token_secret = ''
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
	streamer = DogePriceStreamer()
	pricedb = DogePriceBase()
	replied_tweetids = []

	currenttime = 0
	lasttime = 0
	dogebtc = usdbtc = dogeusd = usddoge = 0
	last_hour_dogebtc = last_hour_usdbtc = last_hour_usddoge = 0
	last_day_dogebtc = last_day_usdbtc = last_day_usddoge = 0
	last_week_dogebtc = last_week_usdbtc = last_week_usddoge = 0

	def __init__(self):
		self.currenttime = datetime.datetime.now().replace(microsecond=0)
		#Need to update database for minute column
		last_hour_tweet = self.pricedb.c.execute("SELECT * FROM dogePrices ORDER BY day DESC, hour DESC").fetchone()
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
		self.dogebtc = self.streamer.avg_dogebtc
		self.usdbtc = self.streamer.usdbtc
		self.usddoge = float(self.dogebtc)*float(self.usdbtc)
		#self.dogeusd = 1/self.usddoge
		self.format_prices()

	def format_prices(self):
		self.dogebtc = '%.8f' % self.dogebtc
		self.usdbtc = '%.2f' % self.usdbtc
		#self.dogeusd = '%.2f' % self.dogeusd
		self.usddoge = '%.6f' % self.usddoge

	def __str__(self):
		return str(self.dogebtc)+'  DOGE:BTC'+'\n'+\
			   '$'+str(self.usddoge)+'   USD:DOGE'+'\n'+\
			   '$'+str(self.usdbtc)+'     USD:BTC'
			   #'D'+str(self.dogeusd)+'    DOGE:USD'+'\n'+\
			   
	def hourly_update(self):
		status = '['+self.currenttime.time().strftime("%H")+':'+self.currenttime.time().strftime("%M")+' EST] Avg #DOGE prices:'+'\n'+\
			self.dogebtc+'  BTC:DOGE '+self.percent_change(self.dogebtc, self.last_hour_dogebtc)+'\n'+\
			'$'+self.usddoge+'   $:DOGE   '+self.percent_change(self.usddoge, self.last_hour_usddoge)+'\n'+\
			'$'+self.usdbtc+'     $:BTC    '+self.percent_change(self.usdbtc, self.last_hour_usdbtc)+'\n'+\
			'#dogecoin #BTC #dogepricebot'
		print ''
		#Comment out when testing
		#self.api.update_status(status)
		#print 'Tweet posted:'
		print status
			  #'D'+self.dogeusd+'  DOGE:$', self.percent_change(self.dogeusd, self.last_hour_dogeusd)+'\n'+\
		print ''
		print 'Updating price database...'
		self.pricedb.update_DB(self.currenttime, self.dogebtc, self.usddoge, self.usdbtc)
		print '...done'
		print ''
			  
	def daily_update(self):
		#Need to update for beginning and end of months
		#Assumption is that this would happen at 5pm everyday
		#Determining the last_day, even if it's the end of the month
		months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
		if self.currenttime.day == 1:
			last_month = self.currenttime.month-1
			#Assigns last_day to 31 if last month was within the list of months
			#   with 31 days
			if last_month in months_with_31_days:
				last_day = 31
			#Assigns last_day to 29 if last month was feburary in a leap year, otherwise
			#   is 28
			elif last_month  == 2:
				if calendar.isleap(self.currenttime.year):
					last_day = 29
				else:
					last_day = 28
			else:
				last_day = 30

		last_day_tweet = self.pricedb.c.execute("SELECT * FROM dogePrices WHERE (day = ? AND hour = ?)", (last_day, 19)).fetchone()
		self.last_day_dogebtc = last_day_tweet[5]
		self.last_day_usddoge = last_day_tweet[6]
		self.last_day_usdbtc = last_day_tweet[7]

		status = 'Today\'s #DOGE performance:'+'\n'+\
			self.dogebtc+'  BTC:DOGE '+self.percent_change(self.dogebtc, self.last_hour_dogebtc)+'\n'+\
			'$'+self.usddoge+'   $:DOGE   '+self.percent_change(self.usddoge, self.last_hour_usddoge)+'\n'+\
			'$'+self.usdbtc+'     $:BTC    '+self.percent_change(self.usdbtc, self.last_hour_usdbtc)+'\n'+\
			'#dogecoin #BTC #dogepricebot'

		print status

	def weekly_update(self):
		#Need to update for beginning and end of months
		#Assumption is that this would happen at 5pm everyday
		last_week = (self.currenttime.day - 7)
		last_week_tweet = self.pricedb.c.execute("SELECT * FROM dogePrices WHERE (day = ? AND hour = ?)", (last_week, 11)).fetchone()
		try:
			self.last_week_dogebtc = last_week_tweet[5]
			self.last_week_usddoge = last_week_tweet[6]
			self.last_week_usdbtc = last_week_tweet[7]
			print 'This week\'s #DOGE performance:'+'\n'+\
				  self.dogebtc+'  BTC:DOGE', self.percent_change(self.dogebtc, self.last_week_dogebtc)+'\n'+\
			  	'$'+self.usddoge+'  USD:DOGE', self.percent_change(self.usddoge, self.last_week_usddoge)+'\n'+\
			  	'$'+self.usdbtc+'    USD:BTC', self.percent_change(self.usdbtc, self.last_week_usdbtc)+'\n'+\
			  	'#dogecoin #BTC #dogepricebot'
		except Exception, e:
			print str(e)
	
	def convert(self):
		for mention in self.api.mentions_timeline():
			user = mention.user.screen_name
			amount = 0
			print user
			print mention.text
			if mention.id not in self.replied_tweetids:
				if 'convert' in mention.text:
					if 'doge to usd' in mention.text.lower():
						words = mention.text.split()
						for word in words:
							if word.isnumeric() == True:
								amount = float(word)
						if amount != 0:
							tweet = '@'+str(user)+' wow such convert: '+str(amount)+\
								    ' dogecoins = $'+str(amount*float(self.usddoge))+\
								    ' #dogepricebottest'
							print tweet
							self.api.update_status(tweet, mention.id)
							self.replied_tweetids.append(mention.id)
					elif 'usd to doge' in mention.text.lower():
						words = mention.text.replace('$','').split()
						for word in words:
							if word.isnumeric() == True:
								amount = float(word)
						if amount != 0:
							tweet = '@'+str(user)+' wow such convert: $'+str(amount)+\
								    ' = '+str(amount/float(self.usddoge))+' dogecoins'+\
								    ' #dogepricebottest'
							print tweet
							self.api.update_status(tweet, mention.id)
							self.replied_tweetids.append(mention.id)
			else:
				print 'Duplicate tweet, skipping'


	def stream(self):
		while True:
			try:
				self.update_prices()
				print 'Current time:', self.currenttime
				print 'Last tweeted:', self.lasttime
				if (self.currenttime - self.lasttime).seconds/3600 >= 1:
					print 'Hour has passed, updating now'
					self.hourly_update()
					self.lasttime = self.currenttime
				else:
					print self.currenttime, 'Hour has not yet passed'
			#if new hour, hourly_update()
			#if 5pm, daily_update()
			except Exception, e:
				print str(e)
			#Sleep for an hour
			print 'Sleeping for 60 seconds...'
			print ''
			time.sleep(60)

if __name__ == "__main__":
	bot = DogePriceBot()
	print bot
	print ''
	bot.convert()