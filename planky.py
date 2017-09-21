#!/usr/bin/python
# -*- coding: utf8 -*-
 
import socket, string, time, ssl
import re
import time
import datetime
import os
import subprocess
from random import shuffle
today = datetime.date.today()
today = today.strftime('%b %d %Y')
logpath = '/var/www/blog/irc'
log = ''
try: 
	if logpath[-1:] is not '/' : logpath += '/'
	log = open(logpath + today + '.txt', 'a+') 
except: log = open(logpath + today + '.txt', 'w').write('\n')


network = 'irc.freenode.net'
nick = 'planky'
password = 'hello99'
chan = 'avanti!'
chanpw = 'helllllooooo'
port = 6697
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
import lxml.html

def link(data):
	url = data[data.find('!link')+6:]
	title = os.popen("wget -qO- 'http://unix.stackexchange.com/questions/103252/how-do-i-get-a-websites-title-using-command-line' | perl -l -0777 -ne 'print $1 if /<title.*?>\s*(.*?)\s*<\/title/si'").read() #	webpage = urllib.request.urlopen(url).read()
	url = '''\n<li><a href="%s">%s</a></li>\n''' % (url,title)
	f = open('/var/www/blog/posts/Cool Links.html', 'r').readlines()
	f.append(url)
	f.reverse()
	html5 = ''
	for i in f: html5+=i
	open('/var/www/blog/posts/Cool Links.html', 'w').write(html5)

def gettime():
	return time.strftime('%l:%M%p %Z on %b %d, %Y')

def uptime():
	uptimes = subprocess.check_output(["uptime"])
	return uptimes

def fortune():
	fortunes = subprocess.check_output(["fortune"])
	fortunes = ' '.join(fortunes.split()) #strip \t \n
	return fortunes

def greeting():
	cgreeting = ['Ahoy-hoy!', 'Hola', 'Hi! How are you?', "Huh? I'm Awake!", "Shh. I'm napping.", "Are you awake?"]
	shuffle(cgreeting)
	return cgreeting[0]
	
	
def main(network, nick, chan, port):
	socket.connect((network,port))
	irc = ssl.wrap_socket(socket)
	irc.send('NICK %s\n' % nick)
	irc.send('PASS %s\n' % password)
	data = irc.recv(4096) 
	if data.find('PING') != -1: irc.send('PONG '+data.split()[1]+'')
	print(irc.recv(4096))
	irc.send('USER %s %s %s :My Best Friend Plank\n' % (nick,nick,nick))
	print(irc.recv(4096))
	time.sleep(3)
	irc.send("PRIVMSG nickserv :identify %s %s\r\n" % (nick, password))
	time.sleep(2)
	irc.send('JOIN #%s %s\n' % (chan, chanpw))
	print(irc.recv(4096))
	while True:
		data = irc.recv(4096) 
		if data.find('PING') != -1:
			irc.send('PONG '+data.split()[1]+'')
		if data.find('!quit') != -1:
			irc.send( 'PRIVMSG #Avanti! :Bye Bye!')
			exit()
		if data.find ( 'slaps planky' ) != -1:
			irc.send ( 'PRIVMSG #Avanti! :This is the Trout Protection Agency. Please put the Trout Down and walk away with your hands in the air.\r\n' )
		if data.find ( '#avanti! :planky' ) != -1:
			cgreeting = greeting()
			irc.send ( 'PRIVMSG #Avanti! :%s\r\n' % cgreeting)
			log.write( '<planky> %s\n' % cgreeting)
		if data.find ( '!link' ) != -1:
			irc.send ( 'PRIVMSG #Avanti! :W00t! Learning is cool!\r\n' )
			link(data)
		if data.find ( '!time' ) != -1:
			currentTime = gettime()
			irc.send ( 'PRIVMSG #Avanti! :%s\r\n' % currentTime() )
			log.write("<planky> %s\n" % currentTime)
		if data.find ( '!fortune' ) != -1:
			fortunes = fortune()
			irc.send ( 'PRIVMSG #Avanti! :%s\r\n' % fortunes )
			log.write("<planky> %s\n" % fortunes)
		if data.find ( '!uptime' ) != -1:
			cUptime = uptime()
			irc.send ( 'PRIVMSG #Avanti! :%s\r\n' % cUptime )
			log.write("<planky> %s\n" % cUptime)
			
		if data.find('PRIVMSG') != -1:
			uNick = data.split(':')[1].split('!')[0]
			uMsg = data.split(':')[2]
			uMsg = '<' + uNick + '> ' + uMsg
			log.flush()
			log.write(uMsg)
			log.flush() #don't wait for next message, write it now!
			print(data)
		
		
import signal
import sys
def signal_handler(signal, frame):
        print('\nExiting...\n')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

 
if __name__=='__main__':
	print("Starting IRC logger in verbose mode ...\n")
	main(network, nick, chan, port)
