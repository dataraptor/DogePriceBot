#dogestreamer.py
# -*- coding: iso-8859-15 -*-
import time
import tweepy
from assembler import Assembler
from datetime import datetime
from dbwrapper import Wrapper

class Converter:
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

	#All 168 foreign currencies able to be converted via bitcoinaverage
	#Bypasses openexchangerates.org
	currency_codes = ['AED', 'AFN' , 'ALL' , 'AMD' , 'ANG' , 'AOA' , 'ARS' , 'AUD' , 'AWG' , \
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

	def convert(self, mention):
		command = "SELECT * FROM Mentions WHERE id = %d" % (mention.id)
		previous_mentions = self.wrapper.c.execute(command).fetchall()
		if len(previous_mentions) != 0:
			return "Duplicate tweet, skipping"

		print "No duplicates"
		user = mention.user.screen_name

		#Textual trigger
		if '@dogepricebot convert' in mention.text.lower():
			print "Found conversion request"
			print user+" : "+mention.text
			words = mention.text.lower().split(" ")
			amount, base, quote = float(words[2]), words[3], words[5]
			print amount, base, quote
			rates = self.assembler.assemble(base.upper(), "BTC", quote.upper())
			rate = rates[0]*rates[1]

			#Direct exchange rate
			if 'doge to' in mention.text.lower() or 'dogecoins to' in mention.text.lower() or 'dogecoin to' in mention.text.lower():
				tweet = '@%s wow such convert: %.1f #dogecoin = %.2f %s' % (user, amount, amount*rate, quote)
				return tweet
			#Indirect exchange rate
			elif 'to doge' in mention.text.lower() or 'to dogecoins' in mention.text.lower() or 'to dogecoin' in mention.text.lower():
				tweet = '@%s wow such convert: %.1f %s = %.2f #dogecoin' % (user, amount, quote, amount/rate)
				return tweet
		
	#Continuous price stream
	def listen(self):
		print 'Listening for @dogepricebot convert requests --------------------------'
		while True:
			for mention in self.api.mentions_timeline(count=1):
				try:
					self.convert(mention)
				except Exception, e:
					print "In exception"
					print str(e)
			time.sleep(300)

if __name__ == "__main__":
	bot = Converter()
	bot.listen()