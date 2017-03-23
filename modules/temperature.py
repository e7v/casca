#!/usr/bin/env python3
"""
temp.py - temp now playing module for casca
"""
import subprocess

def temp(casca, input):
	""".temp - Find out what is currently playing on the radio station temp."""


	batcmd="sensors | grep Core"
	result = subprocess.check_output(batcmd, shell=True).decode('utf-8')
	result = result.replace('\n',' ')
	result = result.replace('       ',' ')
	casca.say(result)

temp.commands = ['temp']
temp.example = '.temp'
