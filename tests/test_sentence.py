import unittest
from language.word import Word
from language.sentence import Sentence

class SentenceTestCase(unittest.TestCase):

    def test_sentence_grows(self):
        sut = Sentence()
        sut.add_start(Word('word', 'NN'))
        self.assertEqual('word', sut.words[0].text)



