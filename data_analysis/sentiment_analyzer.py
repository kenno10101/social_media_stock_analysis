from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import pandas as pd

class AdvancedSentimentAnalyzer:
    """Multi-model sentiment analysis"""

    def __init__(self):
        # VADER (good for social media)
        self.vader = SentimentIntensityAnalyzer()

        # Transformers (BERT-based - most accurate)
        try:
            self.transformer = pipeline("sentiment-analysis",
                                       model="distilbert-base-uncased-finetuned-sst-2-english",
                                       device=-1)  # CPU
            print("Transformer model loaded (DistilBERT)")
        except:
            print("Transformer model not available")
            self.transformer = None

    def analyze_vader(self, text):
        """VADER sentiment"""
        if not text or pd.isna(text):
            return 0
        scores = self.vader.polarity_scores(str(text))
        return scores['compound']

    def analyze_textblob(self, text):
        """TextBlob sentiment"""
        if not text or pd.isna(text):
            return 0
        try:
            return TextBlob(str(text)).sentiment.polarity
        except:
            return 0

    def analyze_transformer(self, text):
        """Transformer (BERT) sentiment"""
        if not self.transformer or not text or pd.isna(text):
            return 0

        try:
            # Truncate text to max length
            text = str(text)[:512]
            result = self.transformer(text)[0]

            # Convert to -1 to 1 scale
            score = result['score']
            if result['label'] == 'NEGATIVE':
                score = -score
            return score
        except:
            return 0

    def analyze_ensemble(self, text):
        """Ensemble of multiple models"""
        vader_score = self.analyze_vader(text)
        textblob_score = self.analyze_textblob(text)

        # Weight average (VADER is better for social media)
        ensemble_score = (vader_score * 0.6 + textblob_score * 0.4)

        # Add transformer if available
        if self.transformer:
            transformer_score = self.analyze_transformer(text)
            ensemble_score = (ensemble_score * 0.6 + transformer_score * 0.4)

        return ensemble_score

    def categorize_sentiment(self, score):
        """Categorize sentiment score"""
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
