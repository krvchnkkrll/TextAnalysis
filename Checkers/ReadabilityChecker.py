import re


class ReadabilityAnalyzer:
    def count_syllables(self, word):
        word = word.lower()
        vowels = "аеёиоуыэюя"
        return sum(1 for char in word if char in vowels)

    def analyze_text(self, text):
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = re.findall(r'\b\w+\b', text)

        total_syllables = sum(self.count_syllables(word) for word in words)
        num_sentences = len(sentences)
        num_words = len(words)

        avg_words_per_sentence = num_words / num_sentences if num_sentences > 0 else 0
        avg_syllables_per_word = total_syllables / num_words if num_words > 0 else 0

        flesch_score = (
                206.835
                - 1.3 * avg_words_per_sentence
                - 60.1 * avg_syllables_per_word
        )

        return {
            "flesch_score": flesch_score,
            "average_words_per_sentence": avg_words_per_sentence,
            "average_syllables_per_word": avg_syllables_per_word,
        }

    def get_readability_rating(self, flesch_score):
        if flesch_score >= 90:
            return 5, "Очень легко читается"
        elif flesch_score >= 70:
            return 4, "Легко читается"
        elif flesch_score >= 50:
            return 3, "Средняя сложность"
        elif flesch_score >= 30:
            return 2, "Сложный текст"
        else:
            return 1, "Очень сложный текст"


ReadabilityChecker = ReadabilityAnalyzer()
