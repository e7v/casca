#!/usr/bin/env python3
"""
link.py - Add url to ST.GABRIEL
"""

#from tools import GrumbleError

def addlink(url):
    logfile = '/var/www/blog/posts/Cool Links.html'
    logfile = open(logfile, 'a')
    html = '\n<li><a href={}>{}</a></li>\n'.format(url,url)
    logfile.write(html)
    logfile.close()

def link(casca, input):
    """.link - Find out what is currently playing on the radio station WUVT."""
    weburl = 'https://st.gabriel.st/?view=Cool%20Links.html'
    link = input.groups()[1]
    addlink(link)
    casca.say("Added: {} to {}".format(link, weburl))
       # trackinfo = web.json(data)
      
link.commands = ['link']
link.example = '.link https://google.com/'
