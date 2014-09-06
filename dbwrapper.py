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
	def create_price_DB(self):
		self.c.execute("CREATE TABLE Prices (year INTEGER, month INTEGER, day INTEGER, hour INTEGER, minute INTEGER, base_per_mid REAL, mid_per_quote REAL)")

	def create_id_DB(self):
		self.c.execute("CREATE TABLE ReplyIDs (name REAL, id INTEGER)")

	def update_price_DB(self, timestamp, base_per_mid, mid_per_quote, foreign_rates):
		#timestamp is in datetime.now() format
		year = timestamp.year
		month = timestamp.month
		day = timestamp.day
		hour = timestamp.hour
		minute = timestamp.minute
		self.c.execute("INSERT INTO Prices (year, month, day, hour, minute, base_per_mid, mid_per_quote, foreign_rates) VALUES (?,?,?,?,?,?,?,?)",
				   (year, month, day, hour, minute, base_per_mid, mid_per_quote, foreign_rates))
		self.conn.commit()

	def update_id_DB(self, name, twitterid):
		self.c.execute("INSERT INTO ReplyIDs (name, id) VALUES (?,?)",
					    (name, twitterid))
		self.conn.commit()

	def purge_id_DB(self):
		self.c.execute("DELETE FROM replyIDs")
		self.conn.commit()
