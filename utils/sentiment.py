from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analyzer(text):
    low_info_string = {"na", "no meaningful content", "", "-", "n/a"}
    if text is None or text.strip().lower() in low_info_string:
        return "none"

    sentiment = SentimentIntensityAnalyzer().polarity_scores(text)

    if sentiment["compound"] > 0.05:
        return "positive"
    elif sentiment["compound"] <= -0.05:
        return "negative"
    else:
        return "neutral"