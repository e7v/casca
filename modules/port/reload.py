#!/usr/bin/env python
"""
reload.py - casca Module Reloader Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/e7v/casca/
"""

import sys, os.path, time, imp
import irc

def f_reload(casca, input):
    """Reloads a module, for use by admins only."""
    if not input.admin: return

    name = input.group(2)
    if name == casca.config.owner:
        return casca.reply('What?')

    if (not name) or (name == '*'):
        casca.variables = None
        casca.commands = None
        casca.setup()
        return casca.reply('done')

    if not sys.modules.has_key(name):
        return casca.reply('%s: no such module!' % name)

    # Thanks to moot for prodding me on this
    path = sys.modules[name].__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return casca.reply('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'):
        module.setup(casca)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    casca.register(vars(module))
    casca.bind_commands()

    casca.reply('%r (version: %s)' % (module, modified))
    if hasattr(casca.config, 'logchan_pm'):
        if not input.owner:
            casca.msg(casca.config.logchan_pm, 'RELOADED: %r -- (%s, %s) - %s' % (module, input.sender, input.nick, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'
f_reload.thread = False

if __name__ == '__main__':
    print __doc__.strip()
