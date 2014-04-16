import json
import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

cryptsy_prices = opener.open('http://pubapi.cryptsy.com/api.php?method=marketdatav2')
cryptsy_json = json.load(cryptsy_prices)
markets = cryptsy_json['return']['markets']

def getlasttrade(base, alt):	
	#Direct exchange rate
	for market in markets:
		if markets[market]['primarycode'] == base and markets[market]['secondarycode'] == alt:
			rate = float(markets[market]['lasttradeprice'])
			time = markets[market]['lasttradetime']
			return {'type': 'direct',
					'rate': rate,
					'time': time}
		#Maybe the direct market doesn't exist, try indirect?
		elif markets[market]['primarycode'] == alt and markets[market]['secondarycode'] == base:
			rate = float(markets[market]['lasttradeprice'])
			time = markets[market]['lasttradetime']
			return {'type': 'indirect',
					'rate': rate,
					'time': time}
	return "Invalid"

def convert(amount, base, alt):
	base = str(base).upper()
	alt = str(alt).upper()
	conversion = False
	
	last_trade = getlasttrade(base, alt)
	if last_trade != "Invalid":
		if last_trade['type'] == 'direct':
			converted = amount * last_trade['rate']
			print "At %s, %d %s = %.6f %s" % (last_trade['time'], amount, base, converted, alt)
		#Maybe the direct market doesn't exist, try indirect?
		elif last_trade['type'] == 'indirect':
			converted = amount / last_trade['rate']
			print "At %s, %d %s = %.6f %s" % (last_trade['time'], amount, base, converted, alt)
	else:
		print 'Currency pair invalid, requires intermediates'
		secondaries = [markets[market]['secondarycode'] for market in markets if markets[market]['primarycode'] == base and markets[market]['secondarycode'] != alt]
		for secondary in secondaries:
			intermediate = getlasttrade(base, secondary)
			next_intermediate = getlasttrade(secondary, alt)
			if intermediate['type'] == 'direct':
				converted = amount * intermediate['rate']
				print "At %s, %d %s = %.6f %s" % (intermediate['time'], amount, base, converted, secondary)
				print "%s/%s: %.6f" % (secondary, alt, next_intermediate['rate'])
				converted /= next_intermediate['rate']
				print "This converts to %.2f %s" % (converted, alt)
			elif intermediate['type'] == 'indirect':
				converted = amount / next_intermediate['rate']
				print "At %s, %d %s = %.6f %s" % (intermediate['time'], amount, base, converted, secondary)
				print "%s/%s: %.6f" % (secondary, alt, next_intermediate['rate'])
				converted *= next_intermediate['rate']
				print "This converts to %.2f %s" % (converted, alt)
	'''
	if conversion == False:
		print 'An exchange rate must not exist with this currency pair'
		print 'Initiating triangular arbitrage'
		print '====================='
		#Get a list of all intermediate coins
		#Run through the markets list again, average the conversion
		secondaries = [markets[market]['secondarycode'] for market in markets if markets[market]['primarycode'] == base and markets[market]['secondarycode'] != alt]
		for secondary in secondaries:
			for market in markets:
				if markets[market]['primarycode'] == base and markets[market]['secondarycode'] == secondary:
					rate = float(markets[market]['lasttradeprice'])
					time = markets[market]['lasttradetime']
					print 'Direct rate: %.9f' % (rate)
					intermediate = amount * rate
					print "Time: %s \nRate: %.6f %s/%s\n%d %s => %.6f %s" % (time, rate, alt, base, amount, base, converted, secondary)
					break
				#Maybe the direct market doesn't exist, try indirect?
				elif markets[market]['primarycode'] == secondary and markets[market]['secondarycode'] == base:
					rate = float(markets[market]['lasttradeprice'])
					time = markets[market]['lasttradetime']
					print 'Indirect rate: %.9f' % (rate)
					converted = amount / rate
					print "At %s, %d %s = %.6f %s" % (time, amount, base, converted, secondary)
					conversion = True
					break
	'''
while True:
	amount = input("Enter amount to convert: ")
	base = raw_input("Enter base currency: ")
	alt = raw_input("Enter currency to convert to: ")
	convert(amount, base, alt)
#print json.dumps(cryptsy_json, sort_keys=True, indent=4)