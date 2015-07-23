import unittest

from google.appengine.api import urlfetch
from google.appengine.ext import testbed

class UrlfetchTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_you_are_conflicted(self):
        self.assertEqual(1, 1)
