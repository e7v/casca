"""
test_vtluugwiki.py - tests for the VTLUUG wiki module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules import vtluugwiki

@unittest.skip('Skipping until wiki is back up')
class TestVtluugwiki(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_vtluug(self):
        input = Mock(groups=lambda: ['', "VT-Wireless"])
        vtluugwiki.vtluug(self.casca, input)

        out = self.casca.say.call_args[0][0]
        m = re.match('^.* - https:\/\/vtluug\.org\/wiki\/VT-Wireless$',
                out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_vtluug_invalid(self):
        term = "EAP-TLS#netcfg"
        input = Mock(groups=lambda: ['', term])
        vtluugwiki.vtluug(self.casca, input)

        self.casca.say.assert_called_once_with( "Can't find anything in "\
                "the VTLUUG Wiki for \"{0}\".".format(term))

    def test_vtluug_none(self):
        term = "Ajgoajh"
        input = Mock(groups=lambda: ['', term])
        vtluugwiki.vtluug(self.casca, input)

        self.casca.say.assert_called_once_with( "Can't find anything in "\
                "the VTLUUG Wiki for \"{0}\".".format(term))
