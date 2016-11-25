'''Text utils'''

def preprocess(line):
    '''Process a line into a list of tokens

    >>> preprocess("it's (here) ok.")
    ["it'", 's', '(', 'here', ')', 'ok', '.']

    >>> preprocess("Uppercase-lower, case? m")
    ['uppercase', 'lower', ',', 'case', '?', 'm']
    '''
    no_newline = line.replace('\n', '')
    lowline = no_newline.lower()
    comma_sep = lowline.replace(',', ' ,')
    apostrophe_sep = comma_sep.replace("'", "' ")
    period_sep = apostrophe_sep.replace('.', ' .')
    hyphen_sep = period_sep.replace('-', ' ')
    question_sep = hyphen_sep.replace('?', ' ?')
    open_parens = question_sep.replace('(', '( ')
    close_parens = open_parens.replace(')', ' )')
    return close_parens.split(' ')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
