#!/usr/bin/env python3
"""
stocks.py - Look up stocks (powered by Robinhood)

by e7v (https://github.com/e7v)
"""

import urllib.request, json

def stocks(casca, input):
	""".stocks - Find out what is currently playing on the radio station WUVT."""
	#request = urllib.request.Request(location)
	#request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
	
	#trackinfo = webget('https://www.wuvt.vt.edu/playlists/latest_track')
	SYMBOL = input.groups()[1].upper()
	url = "https://api.robinhood.com/quotes/{}/".format(SYMBOL)
	data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))	
	difference = str(float(data['last_trade_price']) - float(data['previous_close']))[:4]
	news = ''
	if float(data['last_trade_price']) > float(data['previous_close']):
		news='UP +${}'.format(difference)
	else:
		news='DOWN by -{}'.format(difference[1:])
	#casca.say("{} last trade price: {}".format(input.groups()[1]), str(data['last_trade_price']))
	casca.say("{}'s last trade price: ${} ({})".format(SYMBOL, data['last_trade_price'], news))
		# trackinfo = web.json(data)
		
stocks.commands = ['st', 'stocks']
stocks.example = '.st GEO'

