import logging
import random
import re

from language.word import Word

class Sentence(object):
    def __init__(self, pos_tagged=None):
        self.words = []
        if pos_tagged is not None:
            self.pos_tagged = pos_tagged.strip('()')
            self.tokenise()

    def add_start(self, word):
        self.words.insert(0, word)

    def add_end(self, word):
        self.words.append(word)

    def apply_rule(self, rule):
        result = rule(self.words)
        if result is not None:
            self.words = result

    def parse_token(self, token):
        return token.strip('()').split('/')

    def tokenise(self):
        words = self.pos_tagged.split()
        cat = None
        i = 1
        while i < len(words):
            if words[i] == '(GPE':
                i += 1
                cat = 'GPE'
            word, tag = self.parse_token(words[i])
            if word != '.':
                self.words.append(Word(word, tag, cat))
            i += 1

        w = self.words[0].text
        self.words[0].text = w[:1].lower() + w[1:]
        
    def random_yodaisms(self):
        if random.random() < 0.2:
            return " Yes."
        return ""

    def render(self):
        s = ""
        for i in range(len(self.words)):
            s += self.words[i].text + ' '
        s = s[0].upper() + s[1:]

        # Remove whitespace before punctuation
        s = re.sub(r'\s+(\W)', r'\1', s)

        # random_yodaisms breaks tests
        punctuation = ''
        if self.words[-1].text != '?':
            punctuation = '.'
        return s.strip() + punctuation #+ self.random_yodaisms()
