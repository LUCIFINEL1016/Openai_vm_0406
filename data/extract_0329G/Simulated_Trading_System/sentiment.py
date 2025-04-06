import requests
import os
import openai
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Retrieve API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ✅ Fetch Market News
def fetch_market_news():
    """Retrieve the latest business and financial news."""
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        return [f"{article['title']} - {article['description']}" for article in articles[:5]]  # Get top 5 news articles
    else:
        print(f"❌ News API Error {response.status_code}: {response.text}")
        return []

# ✅ Perform Sentiment Analysis
def analyze_sentiment(news_list):
    """Analyze sentiment of the provided financial news articles."""
    if not news_list:
        return "❌ No news available for analysis."
    
    prompt = "Analyze the sentiment of the following financial news and summarize if the market sentiment is positive, neutral, or negative:\n\n"
    prompt += "\n".join(news_list)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a financial sentiment analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    sentiment_result = response["choices"][0]["message"]["content"]
    return sentiment_result

# ✅ Main Execution
if __name__ == "__main__":
    print("📡 Fetching the latest market news...")
    news_data = fetch_market_news()
    
    if news_data:
        print("\n📰 Latest News:")
        for i, news in enumerate(news_data, start=1):
            print(f"{i}. {news}")

        print("\n🤖 AI Sentiment Analysis:")
        sentiment = analyze_sentiment(news_data)
        print(sentiment)
    else:
        print("⚠️ No news data retrieved.")