import requests
import pandas as pd
import numpy as np
from transformers import pipeline


def connect_api(url):
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['articles'])
        caption = df['description'].tolist()
        caption = [c for c in caption if c is not None]
        return caption
    
    except Exception as e:
        print(f'An unexpected error has occured: {e}')
    
def analyze_sentiment(c):
    try:
        sentiment_pipeline = pipeline('sentiment-analysis', model = 'ProsusAI/finbert')
        result = sentiment_pipeline(c)[0]
        return result
    except Exception as e:
        print(f'An error has occured: {e}')
        return None

def categorize_sentiment(caption, positive, negative, neutral):
    for c in caption:
        result = analyze_sentiment(c)
        if result['label'] == 'negative':
            negative.append(result['score'])
        if result['label'] == 'positive':
            positive.append(result['score'])
        if result['label'] == 'neutral':
            neutral.append(result['score'])  
    return positive, negative, neutral

def sentiment_score(positive, negative, neutral):
    pos_sum = np.sum(positive)
    neg_sum = np.sum(negative)
    neu_sum= np.sum(neutral)
    total = pos_sum + neg_sum + neu_sum
    if total == 0:
        return 0
    score = 100 * (pos_sum - neg_sum) / total
    return round(score, 2)

url = (f'https://newsapi.org/v2/top-headlines?'
       'q=Apple&'
       'from=2025-04-03&'
       'sortBy=popularity&'
       'apiKey=b2b6428600dc47d2b4460c559df86757')

def main():
    articles = connect_api(url=url)
    results = analyze_sentiment(articles)
    positive, negative, neutral = categorize_sentiment(results)
    score = sentiment_score(positive, neutral, negative)
    mar_sentiment = sentiment_score(positive, negative, neutral)

if __name__ == '__main__':
    main()
