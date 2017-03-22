"""
test_hs.py - tests for the hokie stalker module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.hs import search, hs


class TestHs(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_search(self):
        data = search('john')

        assert len(data) >= 1
        self.assertIn('uid', data[0])
        self.assertIn('cn', data[0])

    def test_single(self):
        input = Mock(group=lambda x: 'marchany')
        hs(self.casca, input)

        pattern = re.compile(
            '^.* - http://search\.vt\.edu/search/person\.html\?person=\d+$',
            flags=re.UNICODE)
        out = self.casca.reply.call_args[0][0]
        self.assertRegex(out, pattern)

    def test_multi(self):
        input = Mock(group=lambda x: 'john')
        hs(self.casca, input)

        pattern = re.compile(
            '^Multiple results found; try http://search\.vt\.edu/search/people\.html\?q=.*$',
            flags=re.UNICODE)
        out = self.casca.reply.call_args[0][0]
        self.assertRegex(out, pattern)

    def test_2char(self):
        input = Mock(group=lambda x: 'hs')
        hs(self.casca, input)

        out = self.casca.reply.call_args[0][0]
        self.casca.reply.assert_called_once_with("No results found")

    def test_none(self):
        input = Mock(group=lambda x: 'THIS_IS_NOT_A_REAL_SEARCH_QUERY')
        hs(self.casca, input)

        out = self.casca.reply.call_args[0][0]
        self.casca.reply.assert_called_once_with("No results found")
