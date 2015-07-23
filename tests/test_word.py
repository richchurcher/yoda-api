import unittest
from language.word import Word

class WordTestCase(unittest.TestCase):

    def test_word_text(self):
        sut = Word('word', 'NN')
        self.assertEqual('word', sut.source)
        self.assertEqual('NN', sut.tag)

