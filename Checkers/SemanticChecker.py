from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSimilarity:
    def __init__(self, text, user_words, model_name="all-MiniLM-L6-v2", threshold=0.5):
        self.text = text
        self.user_words = user_words
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def get_similarity(self):
        text_vector = self.model.encode([self.text])
        word_vectors = self.model.encode(self.user_words)

        similarities = [cosine_similarity(text_vector, word_vector.reshape(1, -1))[0][0] for word_vector in
                        word_vectors]
        return similarities

    def is_close(self, similarity):
        return similarity >= self.threshold

