#!/usr/bin/env python3
"""
securitytracker.py - pulls the latest bug from securitytracker.com
"""

import urllib
import pickle
from time import sleep
from bs4 import BeautifulSoup
db = False
dblocation = '/var/www/casca/securitytracker.db'
announcing = False


def loadDatabase():
	global db
	try:
		with open(dblocation, 'rb') as f:
			db = pickle.load(f)
	except:
		print('error loading securitytracker.db')
	return db
db = loadDatabase()

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

	
def latest(onlyNew=False):
	global db
	db = loadDatabase()
	html5 = html()
	url = 'http://securitytracker.com'+html5.findAll('a')[9].attrs['href']
	anchortext = html5.findAll('a')[9].text
	answer = False
	if anchortext == db: #nothings changed
		 if onlyNew: 
			 answer = False
		 else: 
			 answer = anchortext
			 answer = answer + ' - ' + url
	else: #somethings changed
		#print(anchortext)	
		answer = anchortext
		db = anchortext
		saveDatabase(anchortext)
		answer = answer + ' - ' + url
	return answer
	#return {'url' : url, 'text' : anchortext}

def securitytracker(casca, input):
	""".wuvt - Find out what is currently playing on the radio station WUVT."""
	casca.say(latest(onlyNew=False))

securitytracker.commands = ['securitytracker']
securitytracker.example = '.securitytracker'

def last5(casca, input):
	html5 = html()
	
	url = 'http://securitytracker.com'
	casca.say(html5.findAll('a')[9].text + ' - ' + url + html5.findAll('a')[9].attrs['href'])
	sleep(.7)
	casca.say(html5.findAll('a')[10].text + ' - ' + url + html5.findAll('a')[9].attrs['href'])
	sleep(.7)
	casca.say(html5.findAll('a')[11].text + ' - ' + url + html5.findAll('a')[9].attrs['href'])
	sleep(.7)
	casca.say(html5.findAll('a')[12].text + ' - ' + url + html5.findAll('a')[9].attrs['href'])
	sleep(.7)
	casca.say(html5.findAll('a')[13].text + ' - ' + url + html5.findAll('a')[9].attrs['href'])
last5.commands = ['securitytracker-last5', 'last5', '!st5']
securitytracker.example = '.securitytracker-last5'
	
def announcer(casca, input):
	""".announce-securitytracker - Announce the latest bugs."""
	global announcing
	if not announcing:
		announcing = True
		answer = latest(onlyNew=False) # returns 'www.whatever.com' or 'False'
		while True:
			if answer:
				#print('new!')
				casca.say(answer)
				answer = latest(onlyNew=True)
				#print("answer should be reset: "+str(answer))
				sleep(20)
			else:
				#print('old! pass.')
				answer = latest(onlyNew=True)
				sleep(20)
	else:
		casca.say('Running...')
announcer.commands = ['announcer-securitytracker', 'securitytracker-announce', '!st', '!securitytracker']
announcer.example = '.announcer-securitytracker'

