#dogetweetbot.py
import tweepy
import time, datetime
from datetime import datetime
import json, urllib2
import sqlite3
#Build database of dogecoin prices with sqlite3
from dogestreamer import Dogestreamer

class DogeTweetbot:
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
	streamer = Dogestreamer()

	currenttime = 0
	lasttime = 0
	dogebtc = usdbtc = dogeusd = usddoge = 0
	last_hour_dogebtc = last_hour_usdbtc = last_hour_dogeusd = last_hour_usddoge = 0
	last_day_dogebtc = last_day_usdbtc = last_day_dogeusd = last_day_usddoge = 0
	last_week_dogebtc = last_week_usdbtc = last_week_dogeusd = last_week_usddoge = 0

	def __init__(self):
		self.currenttime = datetime.now().replace(microsecond=0)
		self.last_hour_dogebtc = 0.00000111
		self.last_hour_usddoge = 0.000637
		self.last_hour_usdbtc = 572.52
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
		self.lasttime = self.currenttime
		self.currenttime = datetime.now().replace(microsecond=0)
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
		self.update_prices()

		self.api.update_status('['+self.currenttime.time().strftime("%H")+':'+self.currenttime.time().strftime("%M")+' EST] Avg #DOGE prices:'+'\n'+\
			self.dogebtc+'  DOGE:BTC '+self.percent_change(self.dogebtc, self.last_hour_dogebtc)+'\n'+\
			'$'+self.usddoge+'   $:DOGE   '+self.percent_change(self.usddoge, self.last_hour_usddoge)+'\n'+\
			'$'+self.usdbtc+'     $:BTC    '+self.percent_change(self.usdbtc, self.last_hour_usdbtc)+'\n'+\
			'#dogecoin #BTC #dogepricebot')
		print ''
		print 'Tweet posted:'
		print '['+self.currenttime.time().strftime("%H")+':'+self.currenttime.time().strftime("%M")+' EST] Avg #DOGE prices:'+'\n'+\
			self.dogebtc+'  DOGE:BTC '+self.percent_change(self.dogebtc, self.last_hour_dogebtc)+'\n'+\
			'$'+self.usddoge+'   $:DOGE   '+self.percent_change(self.usddoge, self.last_hour_usddoge)+'\n'+\
			'$'+self.usdbtc+'     $:BTC    '+self.percent_change(self.usdbtc, self.last_hour_usdbtc)+'\n'+\
			'#dogecoin #BTC #dogepricebot'
			  #'D'+self.dogeusd+'  DOGE:$', self.percent_change(self.dogeusd, self.last_hour_dogeusd)+'\n'+\
		print ''
		lasttime = self.currenttime
		#Update last_hour variables
		
		print 'Last DOGE:BTC', self.last_hour_dogebtc
		self.last_hour_dogebtc = self.dogebtc
		print 'New DOGE:BTC', self.dogebtc
		
		#self.last_hour_dogeusd = self.dogeusd

		print 'Last USD:DOGE', self.last_hour_usddoge
		self.last_hour_usddoge = self.usddoge
		print 'New USD:DOGE', self.usddoge

		print 'Last USD:BTC', self.last_hour_usdbtc
		self.last_hour_usdbtc = self.usdbtc
		print 'New USD:BTC', self.usdbtc
			  
	def daily_update(self):
		print 'Today\'s #DOGE performance:'+'\n'+\
			  dogebtc+'  DOGE:BTC', percent_change(dogebtc, last_day_dogebtc)+'\n'+\
			  '$'+dogeusd+'  USD:DOGE', percent_change(usdbtc, last_day_usdbtc)+'\n'+\
			  'D'+usddoge+'   DOGE:USD', percent_change(dogeusd, last_day_dogeusd)+'\n'+\
			  '$'+btcusd+'    USD:BTC', percent_change(usddoge, last_day_usddoge)+'\n'+\
			  '#dogepricebot'
	
	def weekly_update(self):
		print 'This week\'s #DOGE performance:'+'\n'+\
			  dogebtc+'  DOGE:BTC', percent_change(dogebtc, last_day_dogebtc)+'\n'+\
			  '$'+dogeusd+'  USD:DOGE', percent_change(usdbtc, last_day_usdbtc)+'\n'+\
			  'D'+usddoge+'   DOGE:USD', percent_change(dogeusd, last_day_dogeusd)+'\n'+\
			  '$'+btcusd+'    USD:BTC', percent_change(usddoge, last_day_usddoge)+'\n'+\
			  '#dogepricebot'	
	
	def stream(self):
		while True:
			try:
				self.hourly_update()
			#if new hour, hourly_update()
			#if 5pm, daily_update()
			except Exception, e:
				print e
			#Sleep for an hour
			print 'Sleeping for 30 minutes...'
			time.sleep(1800)
		'''
		while True:
			try:
				currenttime = datetime.now().replace(microsecond=0)
				if currenttime.minute == 0:
					print 'New hour, posting tweet'
					print ''
					hourly_update()
					print ''
					print 'Tweet posted'
			except Exception, e:
				print str(e)
			print 'Sleeping for 60 seconds...'
			time.sleep(60)
		'''
		'''
		print 'Avg #dogecoin price at '+str(time.time())+':'+'\n'+\
						  dogebtc+' #DOGE:#BTC'+'\n'+\
						  '$'+dogeusd+'  USD:DOGE'+'\n'+\
						  'D'+usddoge+'   DOGE:USD '+'\n'+\
						  '$'+btcusd+'    USD:BTC '+'\n'+\
						  '#dogepricebot'
		print ''
		print 'Daily #DOGE update for '+str(time.date())+':''\n'+\
						  dogebtc+' #DOGE:#BTC'+'\n'+\
						  '$'+dogeusd+'  USD:DOGE'+'\n'+\
						  'D'+usddoge+'   DOGE:USD '+'\n'+\
						  '$'+btcusd+'    USD:BTC '+'\n'+\
						  '#dogepricebot'
		print ''
		while True:
			try:
				pricelist = getprices()
				api.update_status()
			except Exception, e:
				print str(e)
		'''

bot = DogeTweetbot()
print bot
print ''
bot.stream()