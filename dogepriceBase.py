import sqlite3
from dogepricestreamer import DogePriceStreamer
from dogepricebot import dogepricebot

conn = sqlite3.connect('dogePriceBase.db')
c = conn.cursor()