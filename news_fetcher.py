import requests
import os
from dotenv import load_dotenv

def fetch_news(query="Formula 1 OR Motorsport", language="en", page=1):
    load_dotenv()
    news_api_key = os.environ.get("NEWSAPI_KEY")
    if not news_api_key:
        print("Error: NEWSAPI_KEY is not set in the .env file.")
        return []
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&page={page}&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        formatted_articles = []
        for article in articles:
            formatted_article = {
                'title': article.get('title', 'No Title'),
                'url': article.get('url', 'No URL'),
                'description': article.get('description', ''),
                'content': article.get('content', ''),
                'source_name': article.get('source', {}).get('name', 'Unknown Source')
            }
            formatted_articles.append(formatted_article)
        return formatted_articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")
        return []

if __name__ == '__main__':
    f1_news = fetch_news(query="Formula 1 OR Motorsport", language="en", page=1)
    if f1_news:
        print("Successfully fetched Formula 1/Motorsport news:")
        for article in f1_news:
            print(f"Title: {article['title']}")
            print(f"Source: {article['source_name']}")
            print(f"URL: {article['url']}")
            print("-" * 30)
    else:
        print("Failed to fetch Formula 1/Motorsport news.")

    print("\nTesting with a different query (MotoGP):")
    motogp_news = fetch_news(query="MotoGP", language="en", page=1)
    if motogp_news:
        for article in motogp_news:
            print(f"Title: {article['title']}")
            print(f"Source: {article['source_name']}")
            print(f"URL: {article['url']}")
            print("-" * 30)
    else:
        print("Failed to fetch MotoGP news.")
