from language.word import Word

def apply_yodish_grammar(sentence):
    sentence.apply_rule(rule_prp_vbp)
    sentence.apply_rule(rule_uppercase_i)


def rule_prp_vbp(words):
    """ You are conflicted. -> Conflicted, you are. """
    for i in range(0, len(words)):
        if words[i].tag is 'PRP':
            if words[i+1].tag is 'VBP':
                words.append(Word(',',','))
                words.append(words.pop(i))
                words.append(words.pop(i))
                return


def rule_uppercase_i(words):
    """ Isolated 'i' is always 'I' """
    for i in range(0, len(words)):
        if words[i].text is 'i':
            words[i].text = 'I'
