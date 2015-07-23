class Sentence(object):
    def __init__(self):
        self.words = []

    def add_start(self, word):
        self.words.insert(0, word)

    def add_end(self, word):
        self.words.append(word)
