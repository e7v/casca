"""
test_mylife.py - tests for the mylife module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock
from modules import mylife


class TestMylife(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_fml(self):
        mylife.fml(self.casca, None)
        assert self.casca.say.called is True
