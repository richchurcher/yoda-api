import json
import logging

from flask import Flask, jsonify, request
from google.appengine.api import urlfetch, urlfetch_errors

from language.sentence import Sentence
from language.tagger import PartOfSpeechTagger
from language.contractions import expand_contractions
from rules.yodish import apply_yodish_grammar

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
    source = expand_contractions(source)
    source = t.tag(source)
    source = source.replace('\n','')
    logging.warning("Foo: " + source)
    sentences = source.split(')(')

    translated = ""
    for pos_tagged in sentences:
        s = Sentence(pos_tagged)
        apply_yodish_grammar(s)
        translated += s.render() + ' '
    return translated.strip()

