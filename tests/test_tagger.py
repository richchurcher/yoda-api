import unittest
from language import tagger

from google.appengine.api import urlfetch
from google.appengine.ext import testbed

class TaggerTestCase(unittest.TestCase):
    """ Because urlfetch_stub still sends HTTP requests, and every call to
    translate() uses the urlfetch service to talk to text-processing.com,
    this isn't an ideal unit testing picture. Works for initial development 
    though. """
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_tagger(self):
        sut = tagger.PartOfSpeechTagger(
            'http://text-processing.com/api/tag/', 
            'text'
        )
        self.assertEqual(
            u"(S I/PRP am/VBP sorry/JJ)", 
            sut.fetch_pos("I am sorry")
        )


