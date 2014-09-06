import time
import tweepy
import json
import urllib2
from urllib2 import urlopen
from datetime import datetime
import cookielib
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

class Scraper():
	btcdogerates = []
	