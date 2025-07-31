import requests
from news_table import News
from datetime import datetime

def fetch_data_api():
    
    url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=d02b525d15ec4b69a7695a0c118491df'
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()

    all_articles = news_data["articles"]
    return all_articles

def transform_data(all_articles):
    # list to store article data in sequence
    article_data = []

    for article in all_articles:
        
        article_data.append(News(
            title = article["title"],
            description = article["description"],
            url = article["url"],
            published_at = convert_date(article["publishedAt"]),
            content = article["content"] 
        ))
    return article_data

def convert_date(ts):
    if '.' in ts:
        date_part, frac = ts.split('.')
        frac = frac[:6]  # Truncate to 6 digits
        ts = f"{date_part}.{frac}Z"
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")