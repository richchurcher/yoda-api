import json
import logging
import re
import urllib

from flask import Flask, jsonify, request
from google.appengine.api import urlfetch, urlfetch_errors

from language.word import Word
from language.sentence import Sentence
from rules.yodish import *

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello():
    return 'The Yoda API, this is. Mmmmm.'

@app.route('/api/v1/yodish', methods=['GET'])
def get_yodish():
    return jsonify({'yodish': translate(request.args.get('text'))})

def translate(source):
    source = source[:1].lower() + source[1:]
    pos_tagged = fetch_pos(source.strip(' .'))
    words = word_list(pos_tagged.strip('()'))
    s = Sentence(words)
    apply_yodish_grammar(s)
    return s.render()

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
        logging.warning(response.content)
        return json.loads(response.content)['text']

def word_list(pos_tagged_words):
    words = pos_tagged_words.split()
    del(words[0])

    for i in range(0, len(words)):
        word, tag = words[i].split('/')
        words[i] = Word(word, tag)
    return words

def apply_yodish_grammar(sentence):
    sentence.apply_rule(rule_prp_vbp)

