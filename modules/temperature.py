#!/usr/bin/env python3
"""
systools.py - temp now playing module for casca
"""
import subprocess

def uname(casca, input):
	""".uname - get 'uname -a'"""

	batcmd="uname -a"
	result = subprocess.check_output(batcmd, shell=True).decode('utf-8')
	result = result.replace('\n',' ')
	result = result.replace('       ',' ')
	casca.say(result)
uname.commands = ['uname']
uname.example = '.uname'


def uptime(casca, input):
	""".uptime - get system uptime."""

	batcmd="uptime"
	result = subprocess.check_output(batcmd, shell=True).decode('utf-8')
	result = result.replace('\n',' ')
	result = result.replace('       ',' ')
	casca.say('\x1F Uptime: \x1F' + result)
uptime.commands = ['uptime', 'up']
uptime.example = '.uptime'


def temp(casca, input):
	""".temp - get system temperature."""


	batcmd="sensors | grep Core"
	result = subprocess.check_output(batcmd, shell=True).decode('utf-8')
	result = result.replace('\n',' ')
	result = result.replace('       ',' ')
	casca.say(result)

temp.commands = ['temperature', 'temp']
temp.example = '.temperature'
