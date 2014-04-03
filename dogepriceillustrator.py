import plotly
from datetime import datetime
from dogepricebase import DogePriceBase

database = DogePriceBase()
py = plotly.plotly("dataraptor", "97xc9d5r1u")
graph_data = []
x = []
y = []
text = []

tweets = database.c.execute("SELECT * FROM dogePrices ORDER BY month, day, hour").fetchall()
for tweet in tweets:
	timestamp = datetime(tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], second=0, microsecond=0)
	x.append(timestamp)
	y.append(tweet[5])
	text.append("BTC:DOGE")
	print timestamp, tweet[5]

graph_data.append(
	{
		'name': "BTC:DOGE",
		'x': x,
		'y': y,
		'text': text,

		'type': 'scatter',
		'mode': 'lines'
	})

layout = {
	'xaxis': {'title': 'Timestamp'},
	'yaxis': {'title': 'BTC:DOGE Exchange Rate'},
	'title': 'Market Dogecoin Prices'
}

py.plot(graph_data, layout=layout,
		filename='My first plotly graph', fileopt='overwrite',
		world_readable = True, width = 1000, height = 650)