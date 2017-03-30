#!/usr/bin/env python3
"""
link.py - Add url to ST.GABRIEL. this is a highly specific module.
"""

#from tools import GrumbleError

def addlink(url,logfile):
    logfile = open(logfile, 'a')
    html = '\n<li><a href={}>{}</a></li>\n'.format(url,url)
    logfile.write(html)
    logfile.close()

def link(casca, input):
    """.link - Find out what is currently playing on the radio station WUVT."""
    weburl = 'https://st.gabriel.st/?view=Cool%20Links.html'
    logfile = casca.config.linkspy
    if input.admin: 
        link = input.groups()[1]
        addlink(link, logfile)
        casca.say("Added: {} to {}".format(link, weburl))
    else:
        casca.say("Only the king can do that.") 
      
link.commands = ['link']
link.example = '.link https://google.com/'
