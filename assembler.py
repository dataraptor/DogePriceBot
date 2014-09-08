import time
import tweepy
import json
import urllib2
from scraper import Scraper
from urllib2 import urlopen
from datetime import datetime
import cookielib
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

class Assembler():

	def __init__(self):
		self.scraper = Scraper()

	def assemble(self, base, mid, quote):
		#return 'Average price of dogecoin: %s %.7f' % (quote, self.base_average(self.current_rates) * self.get_bitcoinaverage(quote))
		base_average = self.get_baseaverage(self.scraper.get_prices(base, mid))
		return [base_average, self.get_bitcoinaverage(quote)]

	def get_baseaverage(self, rates):
		return sum(rates)/len(rates)

	def get_bitcoinaverage(self, quote):
		print "In Assembler.py: scraping for bitcoin average"
		url = 'https://api.bitcoinaverage.com/ticker/global/all'
		market = json.load(opener.open(url))
		print "Opened JSON"
		print market['USD']['last']
		bitcoin_average = float(market[quote]['last'])
		print "In Assembler.py: scraped bitcoin_average %.2f" % (bitcoin_average)
		return float(bitcoin_average)

if __name__ == "__main__":
	bot = Assembler()
	print bot.assemble("DOGE", "BTC", "USD")