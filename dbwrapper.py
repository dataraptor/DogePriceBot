import sqlite3

class Wrapper:
	conn = 0
	c = 0
	
	def __init__(self):
		self.conn = sqlite3.connect('dogepricebot.db')
		self.c = self.conn.cursor()

	def __str__(self):
		return 'I am the dogePrice database interactive python program.'

	#Only execute this once to create the database
	def create_price_db(self):
		self.c.execute("CREATE TABLE Prices (year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, base_per_mid REAL, mid_per_quote REAL)")

	def create_mentions_db(self):
		self.c.execute("CREATE TABLE Mentions (name REAL, id INTEGER)")

	def update_price_db(self, timestamp, base_per_mid, mid_per_quote):
		#timestamp is in datetime.now() format
		year = timestamp.year
		month = timestamp.month
		day = timestamp.day
		hour = timestamp.hour
		minute = timestamp.minute
		self.c.execute("INSERT INTO Prices (year, month, day, hour, minute, base_per_mid, mid_per_quote) VALUES (?,?,?,?,?,?,?)",
				   (year, month, day, hour, minute, base_per_mid, mid_per_quote))
		self.conn.commit()

	def update_mentions_db(self, name, twitterid):
		self.c.execute("INSERT INTO Mentions (name, id) VALUES (?,?)",
					    (name, twitterid))
		self.conn.commit()
