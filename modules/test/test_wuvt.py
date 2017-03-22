"""
test_wuvt.py - tests for the wuvt module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock
from modules.wuvt import wuvt

class TestWuvt(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_wuvt(self):
        wuvt(self.casca, None)

        out = self.casca.say.call_args[0][0]
        m = re.match('^.* is currently playing .* by .*$', out,
                flags=re.UNICODE)
        self.assertTrue(m)
