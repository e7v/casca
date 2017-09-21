#!/usr/bin/env python
"""
insult.py - Jenni Insult Module
by alekhin0w

More info:
 * Jenni: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""
import os, random
from modules import unicode as uc

def insult(casca, input):
    """ insults <target> with configured language insult """
    try:
        insultFilename = os.path.expanduser('~/.casca/insult.'+ casca.config.insult_lang +'.txt')
    except:
        casca.say("You need to configure the default language!")
        return

    target = input.group(2)
    if not target:
        return casca.reply('.i <target>!')
    target.encode('utf-8')
    target = (target).strip()
    try:
        fn = open(insultFilename, "r")
    except IOError as e:
        generateDatabase(casca, insultFilename)
        fn = open(insultFilename, "r")
    lines = fn.readlines()
    fn.close()
    random.seed()
    casca.say(target + ': ' + uc.decode(random.choice(lines)))

insult.commands = ['i']
insult.priority = 'medium'
insult.example = '.i <target>'

def addinsult(casca, input):
    """.iadd <insult> -- adds a harsh adjetive to the insult database"""
    try:
        insultFilename = os.path.expanduser('~/.casca/insult.'+ casca.config.insult_lang +'.txt')
    except:
        casca.say("You need to configure the default language!")
        return

    text = input.group(2)
    text = uc.encode(text)
    fn = open(insultFilename, "a")
    fn.write(text)
    fn.write("\n")
    fn.close()
    casca.reply("Insult added.")
addinsult.commands = ['iadd']
addinsult.priority = 'medium'
addinsult.example = '.iadd Bad Person'
addinsult.rate = 30

def generateDatabase(casca, insultFilename):
    if casca.config.insult_lang == "english":
        insultList = ['fuck you', 'stupid', 'asshole', 'you suck']
    elif casca.config.insult_lang == "spanish":
        insultList = ['puto', 'trolo', 'forro', 'insurrecto', 'trolita', 'aguafiestas', 'actualizame esta gil', 'apestoso usuario de windows']
    else:
        return # silent fail due lack of configuration
    fn = open(insultFilename, "a")

    for insult in insultList:
        fn.write(insult)
        fn.write("\n")
    fn.close()

    casca.say(casca.config.insult_lang + " insult database created.")

if __name__ == '__main__':
    print __doc__.strip()
