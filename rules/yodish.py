from language.word import Word

def rule_prp_vbp(words):
    """ You are conflicted. -> Conflicted, you are. """
    for i in range(0, len(words)):
        if words[i].tag == 'PRP':
            if words[i+1].tag == 'VBP':
                words.append(Word(',',','))
                words.append(words.pop(i))
                words.append(words.pop(i))
                return

