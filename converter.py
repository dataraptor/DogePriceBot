#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
from assembler import Assembler
from datetime import datetime
from dbwrapper import Wrapper

class Converter:
	#Global variables
	fo = open('authentication.txt')
	lines = [str(line.rstrip('\n')) for line in fo]
	consumer_key = lines[0]
	consumer_secret = lines[1]
	access_token = lines[2]
	access_token_secret = lines[3]
	fo.close()

	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creation of the actual interface, using authentication
	api = tweepy.API(auth)

	#All 168 foreign currencies able to be converted via bitcoinaverage
	#Bypasses openexchangerates.org
	currency_codes = ['AED' , 'AFN' , 'ALL' , 'AMD' , 'ANG' , 'AOA' , 'ARS' , 'AUD' , 'AWG' ,\
				      'AZN' , 'BAM' , 'BBD' , 'BDT' , 'BGN' , 'BHD' , 'BIF' , 'BMD' , 'BND' ,\
				      'BOB' , 'BRL' , 'BSD' , 'BTC' , 'BTN' , 'BWP' , 'BYR' , 'BZD' , 'CAD' ,\
				      'CDF' , 'CHF' , 'CLF' , 'CLP' , 'CNY' , 'COP' , 'CRC' , 'CUP' , 'CVE' ,\
				      'CZK' , 'DJF' , 'DKK' , 'DOP' , 'DZD' , 'EEK' , 'EGP' , 'ERN' , 'ETB' ,\
				      'EUR' , 'FJD' , 'FKP' , 'GBP' , 'GEL' , 'GGP' , 'GHS' , 'GIP' , 'GMD' ,\
				      'GNF' , 'GTQ' , 'GYD' , 'HKD' , 'HNL' , 'HRK' , 'HTG' , 'HUF' , 'IDR' ,\
				      'ILS' , 'IMP' , 'INR' , 'IQD' , 'IRR' , 'ISK' , 'JEP' , 'JMD' , 'JOD' ,\
				      'JPY' , 'KES' , 'KGS' , 'KHR' , 'KMF' , 'KPW' , 'KRW' , 'KWD' , 'KYD' ,\
				      'KZT' , 'LAK' , 'LBP' , 'LKR' , 'LRD' , 'LSL' , 'LTL' , 'LVL' , 'LYD' ,\
				      'MAD' , 'MDL' , 'MGA' , 'MKD' , 'MMK' , 'MNT' , 'MOP' , 'MRO' , 'MTL' ,\
				      'MUR' , 'MVR' , 'MWK' , 'MXN' , 'MYR' , 'MZN' , 'NAD' , 'NGN' , 'NIO' ,\
				      'NOK' , 'NPR' , 'NZD' , 'OMR' , 'PAB' , 'PEN' , 'PGK' , 'PHP' , 'PKR' ,\
				      'PLN' , 'PYG' , 'QAR' , 'RON' , 'RSD' , 'RUB' , 'RWF' , 'SAR' , 'SBD' ,\
				      'SCR' , 'SDG' , 'SEK' , 'SGD' , 'SHP' , 'SLL' , 'SOS' , 'SRD' , 'STD' ,\
				      'SVC' , 'SYP' , 'SZL' , 'THB' , 'TJS' , 'TMT' , 'TND' , 'TOP' , 'TRY' ,\
				      'TTD' , 'TWD' , 'TZS' , 'UAH' , 'UGX' , 'USD' , 'UYU' , 'UZS' , 'VEF' ,\
				      'VND' , 'VUV' , 'WST' , 'XAF' , 'XAG' , 'XAU' , 'XCD' , 'XDR' , 'XOF' ,\
				      'XPF' , 'YER' , 'ZAR' , 'ZMK' , 'ZMW' , 'ZWL']

	#Expanding to other cryptocurrencies in v1.7
	cryptocurrency_codes = []

	def __init__(self):
		self.assembler = Assembler()
		self.wrapper = Wrapper()

	def populate_db(self):
		for mention in self.api.mentions_timeline():
			self.wrapper.update_mentions_db(mention.user.screen_name, mention.id, mention.text)
	
	#Return True if mention is a duplicate, False otherwise
	def no_duplicates(self, mention):
		command = "SELECT * FROM Mentions WHERE id = %d" % (mention.id)
		duplicates = self.wrapper.c.execute(command).fetchall()
		if len(duplicates) == 0:
			return True
		return False

	def insert_into_db(self, mention):
		self.wrapper.update_mentions_db(mention.user.screen_name, mention.id, mention.text)

	def convert(self, mention):
		if self.no_duplicates(mention):
			user = mention.user.screen_name
			#Textual trigger
			if '@dogepricebot convert' in mention.text.lower():
				print "Found conversion request"
				print user+" : "+mention.text
				words = mention.text.lower().split(" ")
				command_start = words.index('@dogepricebot')
				amount, base, quote = float(words[command_start+2]), words[command_start+3], words[command_start+5]
				if base.lower() == "dogecoin" or base.lower() == "doge":
					rates = self.assembler.assemble(quote.upper())
					rate = rates[0]*rates[1]
					tweet = '@%s wow such convert: %.1f #dogecoin = %.2f %s' % (user, amount, amount*rate, quote.upper())
					print tweet
					self.api.update_status(tweet)
				else:
					rates = self.assembler.assemble(base.upper())
					rate = rates[0]*rates[1]
					tweet = '@%s wow such convert: %.1f %s = %.2f #dogecoin' % (user, amount, base.upper(), amount/rate)
					print tweet
					self.api.update_status(tweet)
			self.insert_into_db(mention)
		else:
			print "duplicate"

	#Continuous price stream
	def listen(self):
		print 'Listening for @dogepricebot convert requests --------------------------'
		while True:
			for mention in self.api.mentions_timeline(count=10):
				try:
					self.convert(mention)
				except Exception, e:
					print "In exception"
					print str(e)
			time.sleep(300)

if __name__ == "__main__":
	bot = Converter()
	bot.listen()