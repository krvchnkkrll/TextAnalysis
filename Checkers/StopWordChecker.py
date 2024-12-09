import re


class UnwantedWordsChecker:
    def __init__(self, stop_words_file):
        self.stop_words = self.load_base_stop_words(stop_words_file)

    def load_base_stop_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            stop_words = {line.strip().lower() for line in file if line.strip()}
        return stop_words

    def load_custom_stop_words(self, custom_file_path):
        with open(custom_file_path, 'r', encoding='utf-8') as file:
            custom_stop_words = {line.strip().lower() for line in file if line.strip()}
        return custom_stop_words

    def contains_stop_words(self, text, custom_stop_words_file=None):
        if custom_stop_words_file:
            custom_stop_words = self.load_custom_stop_words(custom_stop_words_file)
            self.stop_words.update(custom_stop_words)

        words = re.findall(r'\b\w+\b', text.lower())
        return any(word in self.stop_words for word in words)




