import pymorphy2
import re


class Pymorphy2Wrapper:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def get_word_forms(self, word):
        parsed_word = self.morph.parse(word)[0]
        return {form.word for form in parsed_word.lexeme}

    def lem_text(self, text):
        words = re.findall(r'\b\w+\b', text)
        lem_words = [self.morph.parse(word)[0].normal_form for word in words]
        lem_text = re.sub(r'\b\w+\b', lambda match: lem_words.pop(0), text)
        return lem_text

