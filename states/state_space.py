class CommentState:
    def __init__(self, language, sentiment, toxic, spam, text_length):
        self.language = language
        self.sentiment = sentiment
        self.toxic = toxic
        self.spam = spam
        self.text_length = text_length

        self.weights = {
            "toxic": 0.5,
            "spam": 0.3,
            "negative": 0.2,
            "neutral": 0.1
        }

    def score(self):
        score = 0.0

        if self.toxic:
            score += self.weights["toxic"]

        if self.spam:
            score += self.weights["spam"]

        if self.sentiment == "negative":
            score += self.weights["negative"]

        if self.sentiment == "neutral":
            score += self.weights["neutral"]

        # komentar panjang → risiko ambigu naik
        if self.text_length > 20:
            score += 0.05

        return round(min(score, 1.0), 2)

    def to_dict(self):
        return {
            "language": self.language,
            "sentiment": self.sentiment,
            "toxic": self.toxic,
            "spam": self.spam,
            "risk_score": self.score()
        }
