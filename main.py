import json
import logging
import re
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
    yodish = apply_yodish_grammar(words)
    sentence = assemble(yodish)
    return sentence

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
    return words

def apply_yodish_grammar(words):
    yodish = []
    current = 0 

    for i in range(0, len(words)):
        tag = words[i][1]

        # RULE: PRP + VBP pairings go to the end, prepended with comma
        # Example: "You are sad." -> "Sad, you are."
        if tag == 'PRP':
            if words[i+1][1] == 'VBP':
                yodish.append(',')
                yodish.append(words[i][0])
                yodish.append(words[i+1][0])
        elif tag == 'VBP':
            continue
        else:
            yodish.insert(current, words[i][0])
            current += 1

    return yodish

def assemble(words):
    words[0] = words[0].capitalize()
    words[-1] += '.'
    # Remove whitespace before punctuation
    return re.sub(
        r'\s+(\W)',
        r'\1',
        ' '.join(words)
    )

