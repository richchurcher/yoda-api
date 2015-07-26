import unittest

from google.appengine.api import urlfetch
from google.appengine.ext import testbed

from language import tagger
from language.sentence import Sentence
from rules.yodish import *

class E2eTestCase(unittest.TestCase):
    """ Guide rule development with tests, we must. """
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()
        self.tagger = tagger.PartOfSpeechTagger(
            'http://text-processing.com/api/tag/', 
            'text'
        )

    def tearDown(self):
        self.testbed.deactivate()

    def test_prp_vbp(self):
        sut = Sentence(
            "You are conflicted.",
            self.tagger
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Conflicted, you are.",
            sut.render()
        )

    def test_uppercase_i(self):
        sut = Sentence(
            "ii i i",
            self.tagger
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Ii I I",
            sut.render()
        )

    def test_much_anger(self):
        sut = Sentence(
            "I sense much anger in him.",
            self.tagger
        )
        apply_yodish_grammar(sut)
        self.assertEqual(
            "Much anger in him, I sense.",
            sut.render()
        )

