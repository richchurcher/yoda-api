import logging
from language.word import Word

def apply_yodish_grammar(sentence):
    sentence.apply_rule(rule_prp_vbp)
    sentence.apply_rule(rule_rb_jjr)
    sentence.apply_rule(rule_uppercase_i)


def rule_prp_vbp(words):
    """ You are conflicted. -> Conflicted, you are. """
    for i in range(0, len(words)):
        if words[i].tag == 'PRP':
            if words[i+1].tag == 'VBP':
                words.append(Word(',',','))
                words.append(words.pop(i))
                words.append(words.pop(i))
                return


def rule_uppercase_i(words):
    """ Isolated 'i' is always 'I' """
    for i in range(0, len(words)):
        if words[i].text == 'i':
            words[i].text = 'I'


def rule_rb_jjr(words):
    """ I sense much anger in him. -> Much anger I sense in him. """
    for i in range(0, len(words)):
        if words[i].tag == 'RB':
            if words[i+1].tag == 'JJR':
                words.insert(0, words.pop(i))
                words.insert(0, words.pop(i))
                return
