import unittest
from language.word import Word
from language.sentence import Sentence
from rules.yodish import *

class SentenceTestCase(unittest.TestCase):

    def test_sentence_grows(self):
        sut = Sentence()
        sut.add_start(Word('word', 'NN'))
        self.assertEqual('word', sut.words[0].text)

    def test_render_case_and_fullstop(self):
        sut = Sentence()
        sut.add_end(Word('you', 'PRP'))
        sut.add_end(Word('are', 'VBP'))
        sut.add_end(Word('conflicted', 'VBN'))
        self.assertEqual('You are conflicted.', sut.render())

    def test_apply_rule(self):
        sut = Sentence()
        sut.add_end(Word('you', 'PRP'))
        sut.add_end(Word('are', 'VBP'))
        sut.add_end(Word('conflicted', 'VBN'))

        sut.apply_rule(rule_prp_vbp)
        self.assertEqual('Conflicted, you are.', sut.render())
