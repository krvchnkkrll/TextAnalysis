import re
import json


class NorvigSpellChecker:
    def __init__(self, dictionary_file="dictionary.json"):
        with open(dictionary_file, "r", encoding="utf-8") as file:
            self.word_freq = json.load(file)

        self.words_set = set(word for words in self.word_freq.values() for word in words)

    def _edits1(self, word):
        letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _known(self, words):
        return set(w for w in words if w in self.words_set)

    def _candidates(self, word):
        return (
            self._known([word]) or
            self._known(self._edits1(word)) or
            self._known(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1)) or
            [word]
        )

    def correction(self, word):
        candidates = self._candidates(word)
        return max(candidates, key=lambda w: self.word_freq.get(w[0].upper(), []).count(w))

    def _levenshtein_distance(self, word1, word2):
        # Вычисление расстояния Левенштейна
        len1, len2 = len(word1), len(word2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[len1][len2]

    def analyze_text(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        misspelled = {word for word in words if word not in self.words_set}

        corrections = {}
        error_counts = []

        for word in words:
            if word in misspelled:
                corrected_word = self.correction(word)
                corrections[word] = corrected_word
                error_counts.append(self._levenshtein_distance(word, corrected_word))
            else:
                error_counts.append(0)

        total_words = len(words)
        correct_words = total_words - len(misspelled)
        accuracy = (correct_words / total_words) * 100 if total_words > 0 else 0

        corrected_text = re.sub(
            r'\b\w+\b',
            lambda match: corrections.get(match.group(0), match.group(0)),
            text
        )

        return {
            "accuracy": accuracy,
            "misspelled_words": corrections,
            "error_counts": error_counts,
            "corrected_text": corrected_text
        }
