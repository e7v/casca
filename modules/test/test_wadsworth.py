"""
test_nsfw.py - some things just aren't safe for work, the test cases
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.wadsworth import wadsworth


class TestWadsworth(unittest.TestCase):
    def setUp(self):
        self.casca = MagicMock()

    def test_wadsworth(self):
        input = Mock(group=lambda x: "Apply Wadsworth's Constant to a string")
        wadsworth(self.casca, input)

        self.casca.say.assert_called_once_with(
                "Constant to a string")
