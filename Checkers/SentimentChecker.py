from translate import Translator
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


class SentimentChecker:
    def __init__(self):
        nltk.download('vader_lexicon', quiet=True)
        self.analyzer = SentimentIntensityAnalyzer()

    def translate_text(self, text, from_lang='ru', to_lang='en'):
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        return translator.translate(text)

    def analyze_sentiment(self, text):
        translated_text = self.translate_text(text)
        sentiment_scores = self.analyzer.polarity_scores(translated_text)

        if sentiment_scores['compound'] >= 0.05:
            sentiment = "Positive"
        elif sentiment_scores['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "sentiment_scores": sentiment_scores,
            "sentiment": sentiment
        }
