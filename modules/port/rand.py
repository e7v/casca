#!/usr/bin/env python
"""
rand.py - casca Rand Module
Copyright 2010-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

import random
import re

def rand(casca, input):
    """.rand <arg1> <arg2> - Generates a random integer between <arg1> and <arg2>."""
    if input.group(2) == " " or not input.group(2):
        casca.reply("I'm sorry, but you must enter at least one number.")
    else:
        random.seed()
        li_integers = input.group(2)
        li_integers_str = li_integers.split()
        if len(li_integers_str) == 1:
            li_integers_str = re.sub(r'\D', '', str(li_integers_str))
            if len(li_integers_str) > 0:
                if int(li_integers_str[0]) <= 1:
                    a = li_integers_str
                    a = int(a)
                    if a < 0:
                        randinte = random.randint(a, 0)
                    if a > 0:
                        randinte = random.randint(0, a)
                else:
                    a = li_integers_str
                    a = int(a)
                    randinte = random.randint(0, a)
                casca.reply("your random integer is: " + str(randinte))
            else:
                casca.reply("lolwut")
        else:
            ln = li_integers.split()
            if len(ln) == 2:
                a, b = ln
                a = re.sub(r'\D', u'', a)
                b = re.sub(r'\D', u'', b)
                if not a:
                    a = 0
                if not b:
                    b = 0
                a = int(a)
                b = int(b)
                if a <= b:
                    randinte = random.randint(a, b)
                else:
                    randinte = random.randint(b, a)
                casca.reply("your random integer is: " + str(randinte))
            else:
                casca.reply("I'm not sure what you want me to do!")

rand.commands = ['rand']
rand.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()
