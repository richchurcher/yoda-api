import re

class Sentence(object):
    def __init__(self, words=[]):
        self.words = words

    def add_start(self, word):
        self.words.insert(0, word)

    def add_end(self, word):
        self.words.append(word)

    def apply_rule(self, rule):
        rule(self.words)

    def render(self):
        s = ""
        for i in range(0, len(self.words)):
            s += self.words[i].text + ' '
        s = s.capitalize() + '.'

        # Remove whitespace before punctuation
        return re.sub(r'\s+(\W)', r'\1', s)
