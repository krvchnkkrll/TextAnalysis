import json
import re
from ParseExcel import ParseExcelWrapper
from Pymorphy2 import Pymorphy2Wrapper


class Dictionary:
    def __init__(self, dictionary_file="Packages/dictionary.json"):
        self.cleaned_data = []
        self.dictionary = {}
        self.parser = ParseExcelWrapper()
        self.morph_wrapper = Pymorphy2Wrapper()
        self.data = self.parser.parse_excel_data()
        self.dictionary_file = dictionary_file

    def filter_and_clean_data(self):
        unique_words = set()
        self.cleaned_data = [
            re.sub(r"'", '', word) for word in self.data
            if isinstance(word, str) and re.match(r'^[а-яА-ЯёЁ]+$', word)
               and word not in unique_words and not unique_words.add(word)
        ]
        self.cleaned_data.sort()
        return self.cleaned_data

    def build_dictionary(self):
        if not self.cleaned_data:
            self.filter_and_clean_data()
        grouped_data = {}
        for word in self.cleaned_data:
            first_letter = word[0].upper()
            if first_letter not in grouped_data:
                grouped_data[first_letter] = []
            grouped_data[first_letter].append(word)
        self.dictionary = grouped_data
        return self.dictionary

    def add_missing_word_forms(self):
        self.build_dictionary()

        word_count = 0
        for word in self.cleaned_data:
            word_forms = self.morph_wrapper.get_word_forms(word)
            for form in word_forms:
                first_letter = form[0].upper()
                if first_letter not in self.dictionary:
                    self.dictionary[first_letter] = []
                if form not in self.dictionary[first_letter]:
                    self.dictionary[first_letter].append(form)

            word_count += 1
            if word_count % 1000 == 0:
                print(f"Обработано {word_count} слов.")

        print(f"Всего обработано слов: {word_count}")
        return self.dictionary

    def save_to_file(self):
        with open(self.dictionary_file, "w", encoding="utf-8") as file:
            json.dump(self.dictionary, file, ensure_ascii=False, indent=4)
        print(f"Словарь сохранён в файл: {self.dictionary_file}")


dictionary = Dictionary()
dictionary.filter_and_clean_data()
dictionary.add_missing_word_forms()
dictionary.save_to_file()