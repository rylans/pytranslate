'''TranslationScore'''

class TranslationScore(object):
    '''Score a translation'''
    def __init__(self):
        pass

    def of(self, actual_text, expected_text):
        actual_parts = actual_text.split(' ')
        expected_parts = expected_text.split(' ')

        if len(expected_parts) == 0:
            return 1.0

        actual_in_expected = 0
        for actual in actual_parts:
            if actual in expected_parts:
                actual_in_expected += 1
        true_positive = actual_in_expected/float(len(actual_parts))

        expected_not_in_actual = 0
        for expected in expected_parts:
            if expected not in actual_parts:
                expected_not_in_actual += 1
        maxlen = max(len(expected_parts), len(actual_parts))
        true_negative = 1.0 - expected_not_in_actual/float(maxlen)

        return true_positive * true_negative
