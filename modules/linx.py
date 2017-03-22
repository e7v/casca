#!/usr/bin/python3
"""
linx.py - linx.li tools
author: andreim <andreim@andreim.net>
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from tools import GrumbleError
import requests
import json


def linx(casca, input, short=False):
    """.linx <url> - Upload a remote URL to linx.li."""

    url = input.group(2)
    if not url:
        casca.reply("No URL provided")
        return

    try:
        r = requests.get("https://linx.vtluug.org/upload?", params={"url": url}, headers={"Accept": "application/json"})
        if "url" in r.json():
            casca.reply(r.json()["url"])
        else:
            casca.reply(r.json()["error"])

    except Exception as exc: 
        raise GrumbleError(exc)

linx.rule = (['linx'], r'(.*)')


