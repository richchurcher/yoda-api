import json

from flask import Flask, jsonify, request
from google.appengine.api import urlfetch, urlfetch_errors

from language.sentence import Sentence
from language.tagger import PartOfSpeechTagger
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
    t = PartOfSpeechTagger('http://text-processing.com/api/tag/', 'text')
    s = Sentence(source, t)
    apply_yodish_grammar(s)
    return s.render()

