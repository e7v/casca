#!/usr/bin/env python3
"""
securitytracker.py - WUVT now playing module for casca
"""

import urllib
import pickle
from bs4 import BeautifulSoup
db = False
dblocation = '/var/www/casca/securitytracker.db'


def securitytracker(casca, input):
	""".wuvt - Find out what is currently playing on the radio station WUVT."""
	casca.say(latest())


def loadDatabase():
	global db
	try:
		with open(dblocation, 'rb') as f:
			db = pickle.load(f)
	except:
		print('error loading bookmarks.db')
	return db

def saveDatabase(anchortext=''):
	with open(dblocation, 'wb') as f:
		pickle.dump(anchortext, f)

def html():
	location = 'http://securitytracker.com/archives/summary/9000.html'
	request = urllib.request.Request(location)
	request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
	html5 = urllib.request.urlopen(location).read()
	html5 = BeautifulSoup(html5, "html5lib")
	return html5

	
def latest():
	global db
	html5 = html()
	url = 'http://securitytracker.com'+html5.findAll('a')[9].attrs['href']
	anchortext = html5.findAll('a')[9].text
	if anchortext == loadDatabase(): print('same!')
	else:
		print(anchortext)	
		saveDatabase(anchortext)
	return anchortext
	#return {'url' : url, 'text' : anchortext}

securitytracker.commands = ['securitytracker']
securitytracker.example = '.securitytracker'