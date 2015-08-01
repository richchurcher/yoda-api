import logging
from language.word import Word

def apply_yodish_grammar(sentence):
    sentence.apply_rule(rule_prp_vbp)
    sentence.apply_rule(rule_rb_jjr)
    sentence.apply_rule(rule_uppercase_i)
    sentence.apply_rule(rule_vb_prp_nn)
    sentence.apply_rule(rule_dt_vbz)
    sentence.apply_rule(rule_nnp_vbz_rb_vb)
    sentence.apply_rule(rule_nnp_prp_rb_jj)


def get_tag_seq(words):
    return [words[i].tag for i in range(len(words))]


def move_tag_seq(words, seq, dest, punc=None):
    """ If seq present (order matters), move words to dest.
    Prepend with punctuation if required. """
    if len(seq) > len(words):
        return None
    seq_start = index_tag_seq(words, seq)
    if seq_start > -1:
        move_words = words[seq_start:seq_start+len(seq)]
        words = words[:seq_start] + words[seq_start+len(seq):]
        if dest == 'start':
            words = move_words + words
        if dest == 'end':
            if punc is not None:
                words.append(punc)
            words += move_words
        return words
    return None


def index_tag_seq(words, seq, strict=False):
    """ Return index of first occurrence of seq in words. Slightly fuzzy
    finding if strict=False, particularly with regard to tolerating 
    plurals. """
    tags = get_tag_seq(words)
    nouns = 'NN' in seq or 'NNS' in seq
    alt_seq = None
    if strict is False:
        if nouns is True:
            alt_seq = [
                'NNS' if x == 'NN' else 
                'NN' if x == 'NNS' else 
                x for x in seq
            ] 
        
    for i in range(len(tags)):
        check_seq = tags[i:i+len(seq)]
        if check_seq == seq:
            return i
        if nouns:
            if check_seq == alt_seq:
                return i

    return -1


def mutate_tag_seq(words, seq1, seq2):
    """ Move/change words matching tag sequence 1 to match sequence 2.
    May not handle duplicates. """
    if len(seq1) > len(words):
        return None
    seq_start = index_tag_seq(words, seq1)
    if seq_start > -1:
        pre = words[:seq_start]
        post = words[seq_start+len(seq1):]
        mutated = []
        for x in seq2:
            for j in range(len(seq1)): 
                if x == words[seq_start+j].tag:
                    mutated.append(words[seq_start+j])
        return pre + mutated + post
    return None


def rule_prp_vbp(words):
    """ You are conflicted. -> Conflicted, you are. """
    return move_tag_seq(words, ['PRP', 'VBP'], 'end', Word(',',','))


def rule_uppercase_i(words):
    """ Isolated 'i' is always 'I' """
    for i in range(0, len(words)):
        if words[i].text == 'i':
            words[i].text = 'I'
    return words


def rule_rb_jjr(words):
    """ I sense much anger in him. -> Much anger I sense in him. """
    return move_tag_seq(words, ['RB', 'JJR'], 'start')


def rule_vb_prp_nn(words):
    """ Put your weapons away. -> Away put your weapons. """
    if index_tag_seq(words, ['VB', 'PRP$', 'NNS', 'RB']) > -1:
        return move_tag_seq(words, ['VB', 'PRP$', 'NNS'], 'end')
    return None


def rule_dt_vbz(words):
    """ This is my home. -> My home this is. """
    return move_tag_seq(words, ['DT', 'VBZ'], 'end')


def rule_nnp_vbz_rb_vb(words):
    """ Size does not matter. -> Size matters not. 
    Conversion of VB to VBZ is blunt at best (adding 's'). """
    original_len = len(words)
    words = mutate_tag_seq(
        words,
        ['NNP','VBZ','RB','VB'],
        ['NNP','VB','RB']
    )
    if words is not None:
        if len(words) < original_len:
            i = index_tag_seq(words, ['NNP', 'VB', 'RB'])
            words[i+1].text += 's'
            words[i+1].tag = 'VBZ'
    return words

def rule_nnp_prp_rb_jj(words):
    return mutate_tag_seq(
        words,
        ['NNP','PRP','RB','JJ'],
        ['RB','JJ','NNP','PRP']
    )
