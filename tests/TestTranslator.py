# -*- coding: UTF-8 -*-
import unittest

from pytranslate.translator import Translator
from pytranslate.english_model import EnglishModel
from pytranslate.translation_model import TranslationModel

class TestTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.english_model = EnglishModel(['austen-emma.txt', 'melville-moby_dick.txt'])

    def test_word_disambiguation_mit_ihm(self):
        de_text = 'Mit ihm'
        en_text = 'With him'
        trx = self._new_translator(de_text, en_text, self.english_model)
        self._verify(trx, 'mit ihm', 'with him')

    def test_word_disambiguation_ich_finde_dich(self):
        de_text = 'Ich finde dich\nich will\ner liebt dich'
        en_text = 'I find you\ni want\nhe loves you'
        trx = self._new_translator(de_text, en_text, self.english_model)
        self._verify(trx, 'ich finde dich', 'i find you')
        self._verify(trx, 'ich will dich', 'i want you')

    def test_new_translation_de_en_1(self):
        de_text = '''Ich schreibe auf Deutsch
Ich schreibe auf Englisch
Sie ist Chinesisch
Ich bin mit dir
Sie ist mit mir
Mein Vater ist Deutsch'''
        en_text = '''I write in german
I write in English
She is Chinese
I am with you
She is with me
My dad is german'''
        trx = self._new_translator(de_text, en_text, self.english_model)
        self._verify(trx, 'Ich schreibe auf Chinesisch', 'i write in chinese')
        self._verify(trx, 'Sie ist Englisch', 'she is english')
        self._verify(trx, 'Mein Vater ist Chinesisch', 'my dad is chinese')
        self._verify(trx, 'Ich schreibe auf Deutsch mit dir', 'i write in german with you')

    def test_new_translation_de_en_2(self):
        de_text = '''Geh mit ihm
Mit mir
Geh jetzt
Ich wohne mit ihm
Sie bleibt mit uns
und sie bleibt mit mein hund
ich wohne mit meine katze'''
        en_text = '''Go with him
With me
Go now
I live with him
She stays with us
and she lives with my dog
I live with my cat'''
        trx = self._new_translator(de_text, en_text, self.english_model)
        self._verify(trx, 'Sie bleibt mit mir', 'she stays with me')
        self._verify(trx, 'Sie bleibt mit ihm', 'she stays with him')
        self._verify(trx, 'Geh mit uns jetzt', 'go with us now')

    def test_word_disambiguation_sa_fille(self):
        fr_text = 'Avec sa fille\nma fille\navec nous'
        en_text = 'With his daughter\nmy daughter\nwith us'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'avec sa fille', 'with his daughter')
        self._verify(trx, 'avec ma fille', 'with my daughter')

    def test_word_disambiguation_mais_elle(self):
        fr_text = 'mais elle'
        en_text = 'she but'

        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'mais elle', 'but she')

    def test_new_translations_est_noir(self):
        fr_text = '''le chien est noir
le chat est noir
la vache est blanc
le texte'''
        en_text = '''the dog is black
the cat is black
the cow is white
the text'''
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'le chien est blanc', 'the dog is white')
        self._verify(trx, 'le chat est blanc', 'the cat is white')

    def test_new_translations_qui_est(self):
        fr_text = '''qui est ici
elle est ici
il est rouge
il mange bien'''
        en_text = '''who is here
she is here
he is red
he eats well'''
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'qui est rouge', 'who is red')
        self._verify(trx, 'elle est rouge', 'she is red')
        self._verify(trx, 'qui mange ici', 'who eats here')
        self._verify(trx, 'il mange ici', 'he eats here')
        self._verify(trx, 'qui mange bien', 'who eats well')
        self._verify(trx, 'elle mange bien', 'she eats well')

    def test_word_not_in_text(self):
        fr_text = 'elle est'
        en_text = 'she is'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'Il', '[no-translation-il]')
        self._verify(trx, 'il est', '[no-translation-il] is')

    def test_blank_translation(self):
        fr_text = 'cette dame'
        en_text = 'this woman'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, '', '')

    def test_space_translation(self):
        fr_text = 'cette dame'
        en_text = 'this woman'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, ' ', '')

    def test_leading_space_translation(self):
        fr_text = 'mon ami'
        en_text = 'my friend'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, ' mon ami', 'my friend')

    def test_trailing_space_translation(self):
        fr_text = 'mon ami'
        en_text = 'my friend'
        trx = self._new_translator(fr_text, en_text, self.english_model)
        self._verify(trx, 'mon ami ', 'my friend')

    def _verify(self, translator, source_text, expected_translation):
        self.assertTrue(translator.translate(source_text) == expected_translation)

    def _new_translator(self, fr_text, en_text, english_model):
        translation_model = TranslationModel()
        translation_model.learn_from_text(fr_text, en_text)
        return Translator(translation_model, english_model)

if __name__ == '__main__':
    unittest.main()
