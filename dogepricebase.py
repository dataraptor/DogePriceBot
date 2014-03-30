import sqlite3

class DogePriceBase:
	conn = 0
	c = 0
	
	def __init__(self):
		self.conn = sqlite3.connect('dogePriceBase.db')
		self.c = self.conn.cursor()

	def __str__(self):
		return 'I am the dogePrice database interactive python program.'

	#Only execute this once to create the database
	def create_DB(self):
		self.c.execute("CREATE TABLE dogePrices (year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, dogebtc REAL, usddoge REAL, usdbtc REAL)")

	def update_DB(self, timestamp, dogebtc, usddoge, usdbtc):
		#timestamp is in datetime.now() format
		year = timestamp.year
		month = timestamp.month
		day = timestamp.day
		hour = timestamp.hour
		minute = timestamp.minute
		self.c.execute("INSERT INTO dogePrices (year, month, day, hour, minute, dogebtc, usddoge, usdbtc) VALUES (?,?,?,?,?,?,?,?)",
				   (year, month, day, hour, minute, dogebtc, usddoge, usdbtc))
		self.conn.commit()