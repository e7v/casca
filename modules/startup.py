#!/usr/bin/env python
"""
startup.py - Casca Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://github.com/faxalter/casca/casca/
"""

import threading, time

def setup(casca): 
    print("Setting up casca")
    # by clsn
    casca.data = {}
    refresh_delay = 300.0

    if hasattr(casca.config, 'refresh_delay'):
        try: refresh_delay = float(casca.config.refresh_delay)
        except: pass

        def close():
            print("Nobody PONGed our PING, restarting")
            casca.handle_close()
      
        def pingloop():
            timer = threading.Timer(refresh_delay, close, ())
            casca.data['startup.setup.timer'] = timer
            casca.data['startup.setup.timer'].start()
            # print "PING!"
            casca.write(('PING', casca.config.host))
        casca.data['startup.setup.pingloop'] = pingloop

        def pong(casca, input):
            try:
                # print "PONG!"
                casca.data['startup.setup.timer'].cancel()
                time.sleep(refresh_delay + 60.0)
                pingloop()
            except: pass
        pong.event = 'PONG'
        pong.thread = True
        pong.rule = r'.*'
        casca.variables['pong'] = pong

def startup(casca, input):
    import time

    # Start the ping loop. Has to be done after USER on e.g. quakenet
    if casca.data.get('startup.setup.pingloop'):
        casca.data['startup.setup.pingloop']()

    if hasattr(casca.config, 'serverpass'): 
        casca.write(('PASS', casca.config.serverpass))

    if hasattr(casca.config, 'password'): 
        casca.msg('NickServ', 'IDENTIFY %s' % casca.config.password)
        time.sleep(5)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in casca.channels: 
        casca.write(('JOIN', channel))
        time.sleep(0.5)
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

if __name__ == '__main__': 
    print(__doc__.strip())
