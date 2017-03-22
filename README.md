# casca
[![Build Status](https://travis-ci.org/mutantmonkey/casca.png?branch=master)](https://travis-ci.org/mutantmonkey/casca)

This is casca, a Python IRC bot. Originally written by Sean B. Palmer, it has
been ported to Python3.

This version comes with many new modules, SASL support, IPv6 support, TLS support, and unit
tests.

Compatibility with existing casca modules has been mostly retained, but they
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

## Testing
You will need the Python3 versions of `python-nose` and `python-mock`. To run
the tests, simply run `nosetests3`.

## Authors
* Sean B. Palmer, http://inamidst.com/sbp/
* mutantmonkey, http://mutantmonkey.in
