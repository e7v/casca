#!/usr/bin/env python
"""
wuvt.py - WUVT now playing module for casca
"""

#from tools import GrumbleError
from web import get as webget


def wuvt(casca, input):
    """.wuvt - Find out what is currently playing on the radio station WUVT."""

    trackinfo = webget('https://www.wuvt.vt.edu/playlists/latest_track')
    casca.say("WUVT is currently playing "+trackinfo)
       # trackinfo = web.json(data)
      
wuvt.commands = ['wuvt']
wuvt.example = '.wuvt'
