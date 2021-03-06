#!/usr/bin/env python
"""
wuvt.py - WUVT now playing module for casca
"""

from tools import GrumbleError
import web


def wuvt(casca, input):
    """.wuvt - Find out what is currently playing on the radio station WUVT."""

    try:
        data = web.get('https://www.wuvt.vt.edu/playlists/latest_track',
                       headers={'Accept': "application/json"})
        trackinfo = web.json(data)
    except:
        raise GrumbleError("Failed to fetch current track from WUVT")

    if 'listeners' in trackinfo:
        casca.say(
            "{dj} is currently playing \"{title}\" by {artist} with "
            "{listeners:d} online listeners".format(
                dj=trackinfo['dj'],
                title=trackinfo['title'],
                artist=trackinfo['artist'],
                listeners=trackinfo['listeners']))
    else:
        casca.say("{dj} is currently playing \"{title}\" by {artist}".format(
            dj=trackinfo['dj'],
            title=trackinfo['title'],
            artist=trackinfo['artist']))
wuvt.commands = ['wuvt']
wuvt.example = '.wuvt'
