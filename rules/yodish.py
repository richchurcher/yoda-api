import logging
from language.word import Word

def apply_yodish_grammar(sentence):
    sentence.apply_rule(rule_prp_vbp)
    sentence.apply_rule(rule_rb_jjr)
    sentence.apply_rule(rule_uppercase_i)
    sentence.apply_rule(rule_vb_prp_nn)


def get_tag_list(words):
    return [words[i].tag for i in range(len(words))]


def move_tag_seq(words, seq, pos, punc=None):
    """ If seq present (order matters), move words to start or end.
    Prepend with punctuation if required. """
    if len(seq) > len(words):
        return
    tags = get_tag_list(words)
    for i in range(len(tags)):
        if tags[i:i+len(seq)] == seq:
            if pos == 'start':
                for x in range(len(seq)):
                    words.insert(0, words.pop(i))
            if pos == 'end':
                if punc is not None:
                    words.append(punc)
                for x in range(len(seq)):
                    words.append(words.pop(i))


def rule_prp_vbp(words):
    """ You are conflicted. -> Conflicted, you are. """
    move_tag_seq(words, ['PRP', 'VBP'], 'end', Word(',',','))


def rule_uppercase_i(words):
    """ Isolated 'i' is always 'I' """
    for i in range(0, len(words)):
        if words[i].text == 'i':
            words[i].text = 'I'


def rule_rb_jjr(words):
    """ I sense much anger in him. -> Much anger I sense in him. """
    move_tag_seq(words, ['RB', 'JJR'], 'start')


def rule_vb_prp_nn(words):
    """ Put your weapons away. -> Away put your weapons. """
    tags = get_tag_list(words)
    seq = ['VB', 'PRP$', 'NNS', 'RB']
    for i in range(len(tags)):
        if tags[i:i+len(seq)] == seq:
            move_tag_seq(words, ['VB', 'PRP$', 'NNS'], 'end')
