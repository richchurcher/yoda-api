import unittest
from language.word import Word

class WordTestCase(unittest.TestCase):

    def test_word_text(self):
        sut = Word('word', 'NN')
        self.assertEqual('word', sut.text)
        self.assertEqual('NN', sut.tag)


