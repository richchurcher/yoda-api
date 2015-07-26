import json
import urllib

from google.appengine.api import urlfetch, urlfetch_errors

class PartOfSpeechTagger(object):

    def __init__(self, url, field_name):
        self.url = url
        self.field_name = field_name

    def fetch_pos(self, source):
        try:
            response = urlfetch.fetch(
                self.url,
                payload = urllib.urlencode({self.field_name: source}),
                method = urlfetch.POST,
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            )
        except urlfetch_errors.DeadlineExceededError:
            return "Timed out, your request has. Mmmmmm. Try again later, you must."

        if response.status_code == 200:
            return json.loads(response.content)['text']

