import sqlite3
from dogepricestreamer import DogePriceStreamer
from dogepricebot import dogepricebot

conn = sqlite3.connect('dogePriceBase.db')
c = conn.cursor()

#Only execute this once to create the database
def createDB():
	c.execute("CREATE TABLE dogePrices (year INTEGER, month INTEGER, day INTEGER, hour INTEGER, dogebtc REAL, usddoge REAL, usdbtc REAL")

#createDB()

def updateDB(timestamp, dogebtc, usddoge, usdbtc):
	#timestamp is in datetime.now() format
	year = timestamp.year
	month = timestamp.month
	day = timestamp.day
	hour = timestamp.hour
	c.execute("INSERT INTO dogePrices")