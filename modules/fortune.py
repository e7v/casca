#!/usr/bin/env python3
'''return fortune cookie'''
import string
import os
printable = set(string.printable)

def fortune(casca, input):
	quotelength = 150

	while quotelength > 140:
		quote = os.popen('fortune').read()
		quote = ''.join(filter(lambda x: x in string.printable, quote))
		quote = quote.replace('\n',' ')
		quote = quote.replace('\t','-')
		if len(quote) < 140:
			
			casca.say(quote)
			quotelength = len(quote)
			break
			
fortune.commands = ['fortune']
fortune.example = '.fortune'