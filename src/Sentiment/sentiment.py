from transformers import pipeline
import os

class SentimentModel:
    def __init__(self):
        # Load the model from the specified path
        model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model')
        self.pipeline = pipeline("sentiment-analysis", model=model_path)

    def label(self, text):
        # Label sentiment with value ranging from -1 to 1
        output = self.pipeline(text)
        score = output[0]['score']
        return score if output[0]['label'] == 'POSITIVE' else -1 * score
    