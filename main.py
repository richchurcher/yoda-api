import json
import logging
import urllib

from flask import Flask, jsonify, request
from google.appengine.api import urlfetch, urlfetch_errors

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello():
    return 'The Yoda API, this is. Mmmmm.'

@app.route('/api/v1/yodish', methods=['GET'])
def get_yodish():
    return jsonify({'yodish': translate(request.args.get('text'))})

def translate(source):
    pos_tagged = fetch_pos(source.lower().strip(' .'))
    words = word_list(pos_tagged.strip('()'))
    return words

def fetch_pos(source):
    """ Parts of speech tagging from text-processing.com. """
    try:
        response = urlfetch.fetch(
            'http://text-processing.com/api/tag/',
            payload = urllib.urlencode({'text': source}),
            method = urlfetch.POST,
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        )
    except urlfetch_errors.DeadlineExceededError:
        return "Timed out, your request has. Mmmmmm. Try again later, you must."

    if response.status_code == 200:
        return json.loads(response.content)['text']

def word_list(sentence):
    words = sentence.split()
    del(words[0])

    for i in range(0, len(words)):
        word, tag = words[i].split('/')
        words[i] = (word, tag)
    logging.warning(words)
    return words
