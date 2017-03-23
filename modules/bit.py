#!/usr/bin/env python3
"""
wuvt.py - WUVT now playing module for casca
"""

import urllib.request, json

def bit(casca, input):
	""".bit - Find out what is currently playing on the radio station WUVT."""
	#request = urllib.request.Request(location)
	#request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

	#trackinfo = webget('https://www.wuvt.vt.edu/playlists/latest_track')
	url = "http://api.coindesk.com/v1/bpi/currentprice/CNY.json"
	try: 
		data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))	
	except:
		print('Sorry, mate. I could not find that')
		sys.exit(0)
	#difference = str(float(data['last_trade_price']) - float(data['previous_close']))[:4]
	CNY = data['bpi']['CNY']['description'] +': '+ str(data['bpi']['CNY']['rate_float'])
	USD = data['bpi']['USD']['description'] +': '+ str(data['bpi']['USD']['rate_float'])
	news = CNY + ' || ' + USD
	#if float(data['last_trade_price']) > float(data['previous_close']):
	#	news='UP +${}'.format(difference)
	#else:
	#	news='DOWN by $-{}'.format(difference[1:])
	#casca.say("{} last trade price: {}".format(input.groups()[1]), str(data['last_trade_price']))
	casca.say("{}".format(news))
		# trackinfo = web.json(data)

bit.commands = ['bitcoin', 'bit']
bit.example = '.bit GEO'

