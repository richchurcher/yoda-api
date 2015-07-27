import unittest
from language.word import Word
from language.sentence import Sentence
from rules.yodish import *

class SentenceTestCase(unittest.TestCase):

    def setUp(self):
        self.sut = Sentence()
        self.sut.add_end(Word('you', 'PRP'))
        self.sut.add_end(Word('are', 'VBP'))
        self.sut.add_end(Word('conflicted', 'VBN'))

    def test_sentence_grows(self):
        self.sut.add_start(Word('word', 'NN'))
        self.assertEqual(4, len(self.sut.words))

    def test_render_case_and_fullstop(self):
        self.assertEqual("You are conflicted.", self.sut.render())

    def test_expand_contractions(self):
        actual = self.sut.expand_contractions("can't ain't i'm you're")
        self.assertEqual("cannot am not I am you are", actual)

    def test_move_tag_seq(self):
        move_tag_seq(
            self.sut.words,
            ['PRP','VBP'],
            'end'
        )
        self.assertEqual(['VBN','PRP','VBP'], get_tag_seq(self.sut.words))

    def test_plurals(self):
        pass

