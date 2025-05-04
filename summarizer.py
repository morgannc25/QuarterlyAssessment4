import openai
import os
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
news_api_key = os.environ.get("NEWSAPI_KEY")

def summarize_article(article_text):
    if not openai.api_key:
        print("Error: OpenAI API key is not set.")
        return None
    prompt = f"""Summarize the following article in a concise paragraph:
    {article_text}
    """
    try:
        response = openai.Completion.create(  
            model="gpt-3.5-turbo-instruct", 
            prompt=prompt, 
            max_tokens=150,
            temperature=0.3,
        )
        summary = response.choices[0].text.strip() 
        return summary
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return None

def fetch_news(query="Formula 1 OR Motorsport", language="en", page=1):
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
    news_articles = fetch_news(query="Formula 1 OR Motorsport", language="en", page=1)
    if news_articles:
        print("Fetched news articles. Summarizing...\n")
        for article in news_articles:
            summary = summarize_article(article['content'])
            if summary:
                print("-" * 50)
                print(f"Source: {article['source_name']}")
                print(f"Title: {article['title']}")
                print(f"URL: {article['url']}")
                print("\nSummary:")
                print(summary)
            else:
                print(f"Failed to summarize article: {article['title']}")
    else:
        print("Failed to fetch news articles.")
