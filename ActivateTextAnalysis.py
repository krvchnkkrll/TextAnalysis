import re

from Checkers.NorvigSpellChecker import NorvigSpellChecker
from Checkers.SemanticChecker import SemanticSimilarity
from Checkers.SentimentChecker import SentimentChecker
from Checkers.StopWordChecker import UnwantedWordsChecker
from Checkers.ReadabilityChecker import ReadabilityChecker


class AnalysisTextActivator:
    def __init__(self, dictionary_file, base_stop_words_file):
        self.spell_checker = NorvigSpellChecker(dictionary_file)
        self.stop_word_checker = UnwantedWordsChecker(base_stop_words_file)
        self.sentiment_checker = SentimentChecker()
        self.readability_checker = ReadabilityChecker
        self.marks = []
        self.sentimental = []
        self.semantic = []

    def process_text(self, text, user_words, min_accuracy, make_correct, custom_stop_words_file=None):
        contains_stop_words = self.stop_word_checker.contains_stop_words(text, custom_stop_words_file)
        spell_check_result = self.spell_checker.analyze_text(text)
        accuracy = spell_check_result["accuracy"]
        error_counts = spell_check_result["error_counts"]
        sentiment_analysis = self.sentiment_checker.analyze_sentiment(text)
        readability_analysis = self.readability_checker.analyze_text(text)
        flesch_score = readability_analysis["flesch_score"]
        readability_rating, readability_description = self.readability_checker.get_readability_rating(flesch_score)
        corrected_text = spell_check_result["corrected_text"] if make_correct else text
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        for sentence in sentences:
            readability_sentence = self.readability_checker.analyze_text(sentence)
            flesch_score_sentence = readability_sentence["flesch_score"]
            readability_rating_sentence, readability_description_sentence = self.readability_checker.get_readability_rating(
                flesch_score_sentence)
            self.marks.append(readability_rating_sentence)

            sentiment_analysis_sentence = self.sentiment_checker.analyze_sentiment(sentence)
            if sentiment_analysis_sentence["sentiment"] == "Negative":
                self.sentimental.append(-1)
            elif sentiment_analysis_sentence["sentiment"] == "Neutral":
                self.sentimental.append(0)
            else:
                self.sentimental.append(1)

        similarity_calculator = SemanticSimilarity(text, user_words, threshold=0.5)

        similarities = similarity_calculator.get_similarity()

        for word, similarity in zip(user_words, similarities):
            is_close = similarity_calculator.is_close(similarity)
            result = "близко" if is_close else "не близко"
            self.semantic.append({"word": word, "similarity": similarity, "result": result})

        return {
            "original_text": text,
            "corrected_text": corrected_text,
            "error_counts": error_counts,
            "contains_stop_words": contains_stop_words,
            "accuracy": accuracy,
            "misspelled_words": spell_check_result["misspelled_words"],
            "sentiment_analysis": sentiment_analysis,
            "readability_analysis": {
                "flesch_score": flesch_score,
                "readability_rating": readability_rating,
                "readability_description": readability_description,
            },
            "marks": self.marks,
            "sentimental": self.sentimental,
            "semantic": self.semantic
        }


dictionary_file = "Packages/dictionary.json"
base_stop_words_file = "Packages/BaseStopWords.txt"
TextAnalysis = AnalysisTextActivator(dictionary_file, base_stop_words_file)
