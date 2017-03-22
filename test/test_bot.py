"""
Tests for casca's bot.py
"""

import unittest
from mock import call, patch, Mock
import bot


class BotTest(unittest.TestCase):
    @patch('bot.Phenny.setup')
    def setUp(self, mock_setup):
        class MockConfig(object):
            nick = 'casca'
            password = 'nickserv_pass'
            name = 'Phenny'
            host = 'irc.example.com'
            port = 6667
            ssl = False
            ipv6 = True
            channels = ['#casca']
            owner = 'casca_owner'
            admins = [owner, 'casca_admin']
            prefix = '.'

        self.bot = bot.Phenny(MockConfig)

    def test_input(self):
        class MockOrigin(object):
            nick = 'sock_puppet'
            sender = '#casca'

        origin = MockOrigin()
        text = "Are you ready for casca?"
        match = Mock()
        event = "PRIVMSG"
        args = ('#casca', )
        cmdinput = self.bot.input(origin, text, text, match, event, args)

        self.assertEqual(cmdinput.sender, origin.sender)
        self.assertEqual(cmdinput.nick, origin.nick)
        self.assertEqual(cmdinput.event, event)
        self.assertEqual(cmdinput.bytes, text)
        self.assertEqual(cmdinput.match, match)
        self.assertEqual(cmdinput.group, match.group)
        self.assertEqual(cmdinput.groups, match.groups)
        self.assertEqual(cmdinput.args, args)
        self.assertEqual(cmdinput.admin, False)
        self.assertEqual(cmdinput.owner, False)

    def test_owner(self):
        class MockOrigin(object):
            nick = 'casca_owner'
            sender = '#casca'

        origin = MockOrigin()
        text = "Are you ready for casca?"
        match = Mock()
        event = "PRIVMSG"
        args = ('#casca', )
        cmdinput = self.bot.input(origin, text, text, match, event, args)

        self.assertEqual(cmdinput.owner, True)

    def test_admin(self):
        class MockOrigin(object):
            nick = 'casca_admin'
            sender = '#casca'

        origin = MockOrigin()
        text = "Are you ready for casca?"
        match = Mock()
        event = "PRIVMSG"
        args = ('#casca', )
        cmdinput = self.bot.input(origin, text, text, match, event, args)

        self.assertEqual(cmdinput.admin, True)
