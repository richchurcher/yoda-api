import re
from language.word import Word

class Sentence(object):
    def __init__(self, pos_tagged_sentence):
        self.tokenise(pos_tagged_sentence)


    def add_start(self, word):
        self.words.insert(0, word)


    def add_end(self, word):
        self.words.append(word)


    def apply_rule(self, rule):
        rule(self.words)


    def tokenise(self, sentence):
        self.words = sentence.split()
        del(self.words[0])

        for i in range(0, len(self.words)):
            word, tag = self.words[i].split('/')
            self.words[i] = Word(word, tag)


    def render(self):
        s = ""
        for i in range(0, len(self.words)):
            s += self.words[i].text + ' '
        s = s.capitalize() + '.'

        # Remove whitespace before punctuation
        return re.sub(r'\s+(\W)', r'\1', s)
