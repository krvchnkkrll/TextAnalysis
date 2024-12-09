from Checkers.NorvigSpellChecker import NorvigSpellChecker
from Checkers.SentimentChecker import SentimentChecker
from Checkers.StopWordChecker import UnwantedWordsChecker
from Checkers.ReadabilityChecker import ReadabilityChecker


class UnifiedTextProcessor:
    def __init__(self, dictionary_file, base_stop_words_file):
        self.spell_checker = NorvigSpellChecker(dictionary_file)
        self.stop_word_checker = UnwantedWordsChecker(base_stop_words_file)
        self.sentiment_checker = SentimentChecker()
        self.readability_checker = ReadabilityChecker

    def process_text(self, text, min_accuracy, make_correct, custom_stop_words_file=None):
        contains_stop_words = self.stop_word_checker.contains_stop_words(text, custom_stop_words_file)
        spell_check_result = self.spell_checker.analyze_text(text)
        accuracy = spell_check_result["accuracy"]
        sentiment_analysis = self.sentiment_checker.analyze_sentiment(text)
        readability_analysis = self.readability_checker.analyze_text(text)
        flesch_score = readability_analysis["flesch_score"]
        readability_rating, readability_description = self.readability_checker.get_readability_rating(flesch_score)

        if accuracy < min_accuracy:
            return {
                "original_text": text,
                "corrected_text": None,
                "contains_stop_words": contains_stop_words,
                "accuracy": accuracy,
                "sentiment_analysis": sentiment_analysis,
                "readability_analysis": {
                    "flesch_score": flesch_score,
                    "readability_rating": readability_rating,
                    "readability_description": readability_description,
                },
                "message": "Текст не соответствует минимальному уровню точности."
            }

        corrected_text = spell_check_result["corrected_text"] if make_correct else text

        return {
            "original_text": text,
            "corrected_text": corrected_text,
            "contains_stop_words": contains_stop_words,
            "accuracy": accuracy,
            "misspelled_words": spell_check_result["misspelled_words"],
            "sentiment_analysis": sentiment_analysis,
            "readability_analysis": {
                "flesch_score": flesch_score,
                "readability_rating": readability_rating,
                "readability_description": readability_description,
            }
        }


dictionary_file = "Packages/dictionary.json"
base_stop_words_file = "Packages/BaseStopWords.txt"
TextAnalysis = UnifiedTextProcessor(dictionary_file, base_stop_words_file)