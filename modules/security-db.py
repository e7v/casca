#!/usr/bin/env python3
"""
securitytracker.py - pulls the latest bug from securitytracker.com
"""

import urllib
import pickle
from time import sleep
from bs4 import BeautifulSoup
db = False
dblocation = '/var/www/casca/security-db.com.db'
announcing = False

def saveDatabase(anchortext=''):
	with open(dblocation, 'wb') as f:
		pickle.dump(anchortext, f)


def loadDatabase():
	global db
	try:
		with open(dblocation, 'rb') as f:
			db = pickle.load(f)
	except:
		#print('error loading security-db.com.db')
		saveDatabase()
	return db
db = loadDatabase()


def html():
	location = 'http://www.security-db.com/vulnerabilites.html'
	request = urllib.request.Request(location)
	request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
	html5 = urllib.request.urlopen(location).read()
	html5 = BeautifulSoup(html5, "html5lib")
	return html5

	
def latest(onlyNew=False):
	global db
	db = loadDatabase()
	html5 = html()
	url = html5.findAll('a')[7].attrs['href']
	anchortext = html5.findAll('a')[7].text
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

def securitydb(casca, input):
	""".wuvt - Find out what is currently playing on the radio station WUVT."""
	casca.say(latest(onlyNew=False))

securitydb.commands = ['security-db', 'sdb', 'security-db-latest']
securitydb.example = '.sdb'

def sdb5(casca, input):
	html5 = html()
	
	url = 'http://security-db.com'
	for i in range(7,18):
		casca.say(html5.findAll('a')[i].text + ' - ' + html5.findAll('a')[i].attrs['href'])
		sleep(1)

sdb5.commands = ['sdb-lastest', 'last10', ]
sdb5.example = '.sdb-lastest'
	
def securitydbannounce(casca, input):
	""".announce-securitytracker - Announce the latest bugs."""
	global announcing
	if not announcing:
		announcing = True
		answer = latest(onlyNew=False) # returns 'www.whatever.com' or 'False'
		while True:
			if answer:
				#print('new!')
				
				try:
					casca.say(answer)	
					answer = latest(onlyNew=True)
				except: 
					print('error1')
				#print("answer should be reset: "+str(answer))
				sleep(20)
			else:
				#print('old! pass.')
				try:
					answer = latest(onlyNew=True)
					sleep(20)
				except:
					print('error 2')
	else:
		casca.say('Running...')
securitydbannounce.commands = ['securitydbannounce', 'security-db-announce', '!sdb', '!security-db']
securitydbannounce.example = '.securitydbannounce'

