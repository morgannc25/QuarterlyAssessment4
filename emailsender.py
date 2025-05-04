import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv()
print(f"Loaded NEWSAPI_KEY: {os.getenv('NEWSAPI_KEY')}")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

sender_email = "morgan.mc0727@gmail.com"
recipient_email = "macrawford46@gmail.com"
subject = "Your Daily Motorsports News Summary"

def fetch_motorsports_news():
    url = f"https://newsapi.org/v2/everything?q=motorsports&apiKey={NEWSAPI_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return [article["title"] + ". " + article["description"] for article in articles if article["description"]]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def summarize_motorsports_news(news_articles):
    # Replace this with your actual LLM summarization logic
    return news_articles[:3] # Placeholder: Returns the first 3 articles as summaries

def send_demonstration_email(api_key, sender, recipient, sub, news):
    if not api_key:
        print("Error: EMAIL_API_KEY not found.")
        return

    summary_list_items = ""
    if news:
        for summary in news:
            summary_list_items += f"<li>{summary}</li>"
        email_body = f"""
        <html>
        <head></head>
        <body>
            <h1>Your Daily Motorsports News Summary</h1>
            <p>Here's a brief overview of today's top motorsports stories:</p>
            <ul>
                {summary_list_items}
            </ul>
            <p>Stay informed!</p>
        </body>
        </html>
        """
    else:
        email_body = """
        <html>
        <head></head>
        <body>
            <h1>Your Daily Motorsports News Summary</h1>
            <p>No motorsports news summaries were generated today.</p>
        </body>
        </html>
        """

    sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email(sender)
    to_email = To(recipient)
    email_content = Content("text/html", email_body)
    mail = Mail(from_email, to_email, sub, email_content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(f"Email sent successfully to {recipient}!")
        print(f"Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")

if __name__ == '__main__':
    motorsports_news = fetch_motorsports_news()
    news_summaries = summarize_motorsports_news(motorsports_news)
    send_demonstration_email(EMAIL_API_KEY, sender_email, recipient_email, subject, news_summaries)
    print("\nGenerated Motorsports News Summaries:")
    if news_summaries:
        for summary in news_summaries:
            print(f"- {summary}")
    else:
        print("No motorsports news summaries were generated.")