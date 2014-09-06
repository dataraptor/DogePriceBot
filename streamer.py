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

	def main(self):
		if __name__ == "__main__":
			self.stream()
	
	def priceupdate(self, quote):
		rates = self.assembler.assemble(quote)
		base_mid, mid_quote = rates[0], rates[1]
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
