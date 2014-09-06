import time
import tweepy
import json
import urllib2
import scraper
from urllib2 import urlopen
from datetime import datetime
import cookielib
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

class Converter():

	def __init__(self):
		self.scraper = scraper.Scraper()
		self.current_rates = self.scraper.get_prices("DOGE", "BTC")

	def convert(self, quote):
		#return 'Average price of dogecoin: %s %.7f' % (quote, self.base_average(self.current_rates) * self.get_bitcoinaverage(quote))
		return self.base_average(self.current_rates) * self.get_bitcoinaverage(quote)

	def base_average(self, rates):
		return sum(rates)/len(rates)

	def get_bitcoinaverage(self, quote):
		url = 'https://api.bitcoinaverage.com/ticker/%s' % (quote)
		market = json.load(opener.open(url))
		bitcoin_average = market['last']
		return bitcoin_average