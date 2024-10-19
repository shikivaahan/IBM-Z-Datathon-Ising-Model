from transformers import pipeline
import os

class SentimentModel:
    def __init__(self):
        # Load the model from the specified path
        model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model')
        self.pipeline = pipeline("sentiment-analysis", model=model_path)

    def label(self, text, discrete=False):
        """
        Label sentiment with float ranging from -1 to 1 by default. 
        Set discrete to True to label with either value -1 or +1
        """
        output = self.pipeline(text)[0]
        print(output)
        if discrete:
            return 1 if output['label'] == 'POSITIVE' else -1
        else:
            return output['score'] if output['label'] == 'POSITIVE' else -1 * output['score'] 