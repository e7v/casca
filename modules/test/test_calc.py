# coding=utf-8
"""
test_calc.py - tests for the calc module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.calc import c


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_c(self):
        input = Mock(group=lambda x: '5*5')
        c(self.casca, input)

        self.casca.say.assert_called_once_with('25')

    def test_c_sqrt(self):
        input = Mock(group=lambda x: '4^(1/2)')
        c(self.casca, input)

        self.casca.say.assert_called_once_with('2')

    def test_c_scientific(self):
        input = Mock(group=lambda x: '2^64')
        c(self.casca, input)

        self.casca.say.assert_called_once_with('1.84467440737096 * 10^19')

    def test_c_none(self):
        input = Mock(group=lambda x: 'aif')
        c(self.casca, input)

        self.casca.reply.assert_called_once_with('Sorry, no result.')
