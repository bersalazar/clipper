import unittest
from services.clip import add_quote_character_escape


class TestStringMethods(unittest.TestCase):
    def test_add_quote_character_escape(self):
        a = '"I have often wondered," he said'
        b = "'I have often wondered,' he said"
        c = "This is a simple quote"
        d = '"Don\'t reuse routines in derived classes."'

        self.assertEqual(
            add_quote_character_escape(a), '\\"I have often wondered,\\" he said'
        )
        self.assertEqual(
            add_quote_character_escape(b), "\\'I have often wondered,\\' he said"
        )
        self.assertEqual(add_quote_character_escape(c), "This is a simple quote")
        self.assertEqual(
            add_quote_character_escape(d),
            '\\"Don\\\'t reuse routines in derived classes.\\"',
        )
