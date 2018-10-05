# Casca
This is Casca, a Python IRC bot. Originally written by Sean B. Palmer, it has
been ported to Python3 by mutantmonkey, and is currently maintained by me. 

This version comes with many new modules, SASL support, IPv6 support, TLS support, and unit
tests.

Compatibility with existing Casca modules has been mostly retained, but they
will need to be updated to run on Python3 if they do not already. All of the
core modules have been ported, removed, or replaced.

## Requirements
* Python 3.2+
* [python-requests](http://docs.python-requests.org/en/latest/)

## Installation
1. Run `./casca` - this creates a default config file
2. Edit `~/.casca/default.py`
3. Run `./casca` - this now runs casca with your settings

Enjoy!

## Commands



.choose <red> <blue> - for when you just can't decide.


.g - Google for and return the top result. 

.gc — Get the number of results on Google

.head - Perform an HTTP HEAD on URI. 

.seen - Reports when was last seen. 

.stocks <SYMBOL> - Return current stock information.

.tock - Return the time from the USNO Master Clock. 

.u - Search for a particular Unicode codepoint. 

.u — Search for a unicode character

.weather - Show the weather at airport with the code. 

.wik — Search for something on Wikipedia

casca: tell nick something — Send a message to nick

## Testing
You will need the Python3 versions of `python-nose` and `python-mock`. To run
the tests, simply run `nosetests3`.

## Authors
* Sean B. Palmer, http://github.com/e7v/casca/sbp/
* mutantmonkey, http://mutantmonkey.in
* update