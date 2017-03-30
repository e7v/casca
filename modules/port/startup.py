#!/usr/bin/env python
"""
startup.py - casca Startup Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/casca/
"""

import threading, time

def setup(casca):
    # by clsn
    casca.data = {}
    refresh_delay = 300.0

    if hasattr(casca.config, 'refresh_delay'):
        try: refresh_delay = float(casca.config.refresh_delay)
        except: pass

        def close():
            print "Nobody PONGed our PING, restarting"
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

        # Need to wrap handle_connect to start the loop.
        inner_handle_connect = casca.handle_connect

        def outer_handle_connect():
            inner_handle_connect()
            if casca.data.get('startup.setup.pingloop'):
                casca.data['startup.setup.pingloop']()

        casca.handle_connect = outer_handle_connect

def startup(casca, input):
    import time

    if hasattr(casca.config, 'serverpass') and not casca.auth_attempted:
        casca.write(('PASS', casca.config.serverpass))

    if not casca.is_authenticated and hasattr(casca.config, 'password'):
        if hasattr(casca.config, 'user') and casca.config.user is not None:
            user = casca.config.user
        else:
            user = casca.config.nick

        casca.msg('NickServ', 'IDENTIFY %s %s' % (user, casca.config.password))
        time.sleep(10)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in casca.channels:
        casca.write(('JOIN', channel))
        time.sleep(0.5)
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

# Method for populating op/hop/voice information in channels on join
def privs_on_join(casca, input):
    if not input.mode_target or not input.mode_target.startswith('#'):
        return

    channel = input.mode_target
    if input.names and len(input.names) > 0:
        split_names = input.names.split()
        for name in split_names:
            nick_mode, nick = name[0], name[1:]
            if nick_mode == '@':
                casca.add_op(channel, nick)
            elif nick_mode == '%':
                casca.add_halfop(channel, nick)
            elif nick_mode == '+':
                casca.add_voice(channel, nick)
privs_on_join.rule = r'(.*)'
privs_on_join.event = '353'
privs_on_join.priority = 'high'

# Method for tracking changes to ops/hops/voices in channels
def track_priv_change(casca, input):
    if not input.sender or not input.sender.startswith('#'):
        return

    channel = input.sender

    if input.mode:
        add_mode = input.mode.startswith('+')
        del_mode = input.mode.startswith('-')

        # Check that this is a mode change and that it is a mode change on a user
        if (add_mode or del_mode) and input.mode_target and len(input.mode_target) > 0:
            mode_change = input.mode[1:]
            mode_target = input.mode_target

            if add_mode:
                if mode_change == 'o':
                    casca.add_op(channel, mode_target)
                elif mode_change == 'h':
                    casca.add_halfop(channel, mode_target)
                elif mode_change == 'v':
                    casca.add_voice(channel, mode_target)
            else:
                if mode_change == 'o':
                    casca.del_op(channel, mode_target)
                elif mode_change == 'h':
                    casca.del_halfop(channel, mode_target)
                elif mode_change == 'v':
                    casca.del_voice(channel, mode_target)
track_priv_change.rule = r'(.*)'
track_priv_change.event = 'MODE'
track_priv_change.priority = 'high'

if __name__ == '__main__':
    print __doc__.strip()
