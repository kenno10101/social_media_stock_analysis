import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import numpy as np
from configuration import KAFKA_TOPICS

try:
    import snscrape.modules.twitter as sntwitter
    TWITTER_SCRAPING_AVAILABLE = True
    print("Twitter scraping available (snscrape)")
except (ImportError, AttributeError) as e:
    TWITTER_SCRAPING_AVAILABLE = False
    print("Twitter scraping not available (snscrape compatibility issue)")

class TwitterDataProducer:
    """Scrape Twitter/X data and stream to Kafka"""

    def __init__(self, kafka_layer):
        self.kafka = kafka_layer

    def scrape_twitter_snscrape(self, company_name, ticker, max_tweets=100):
        """Scrape using snscrape (if available)"""
        if not TWITTER_SCRAPING_AVAILABLE:
            return []

        tweets = []
        try:
            query = f"({company_name} OR ${ticker}) lang:en"
            scraper = sntwitter.TwitterSearchScraper(query)

            for i, tweet in enumerate(scraper.get_items()):
                if i >= max_tweets:
                    break

                tweets.append({
                    'ticker': ticker,
                    'company': company_name,
                    'text': tweet.content,
                    'created_at': tweet.date.isoformat(),
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'user': tweet.user.username,
                    'tweet_id': tweet.id,
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Scraping error: {e}")

        return tweets

    def scrape_twitter_alternative(self, company_name, ticker, max_posts=50):
        """Alternative: Scrape from Reddit StockTwits style posts"""
        posts = []

        try:
            # Scrape from public stock discussion forums
            url = f"https://stocktwits.com/symbol/{ticker}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find message containers (this is a simplified example)
                messages = soup.find_all('div', class_='st-widget', limit=max_posts)

                for idx, msg in enumerate(messages):
                    text = msg.get_text(strip=True)
                    if text and len(text) > 10:
                        posts.append({
                            'ticker': ticker,
                            'company': company_name,
                            'text': text[:500],
                            'created_at': datetime.now().isoformat(),
                            'likes': 0,
                            'retweets': 0,
                            'user': 'stocktwits_user',
                            'tweet_id': f'{ticker}_{idx}',
                            'timestamp': datetime.now().isoformat()
                        })
        except Exception as e:
            print(f"      Alternative scraping error: {e}")

        return posts

    def generate_sample_tweets(self, company_name, ticker, count=30):
        """Generate sample tweet-like data for demonstration"""
        sample_sentiments = [
            "{} stock looking strong today!",
            "Thinking of buying more ${} shares",
            "{} earnings report exceeded expectations",
            "Concerned about ${} recent performance",
            "{} innovation continues to impress",
            "Sold my ${} position, taking profits",
            "{} is undervalued right now IMO",
            "Bullish on ${} long term",
            "{} facing some headwinds this quarter",
            "Just added more ${} to my portfolio",
        ]

        tweets = []
        for i in range(count):
            template = np.random.choice(sample_sentiments)
            text = template.format(np.random.choice([company_name, ticker]))

            # Random date within last 30 days
            days_ago = np.random.randint(0, 30)
            date = datetime.now() - timedelta(days=days_ago)

            tweets.append({
                'ticker': ticker,
                'company': company_name,
                'text': text,
                'created_at': date.isoformat(),
                'likes': np.random.randint(0, 1000),
                'retweets': np.random.randint(0, 500),
                'user': f'user_{np.random.randint(1000, 9999)}',
                'tweet_id': f'{ticker}_sample_{i}',
                'timestamp': datetime.now().isoformat()
            })

        return tweets

    def scrape_and_stream(self, companies, max_tweets=100):
        """Scrape Twitter/X and produce to Kafka"""
        all_tweets = {}

        print("\nCollecting Social Media Data and Streaming to Kafka...")
        print("-" * 70)

        for ticker, name in companies.items():
            tweets = []

            # Try Method 1: snscrape
            if TWITTER_SCRAPING_AVAILABLE:
                print(f"  Attempting Twitter scrape for {name}...")
                tweets = self.scrape_twitter_snscrape(name, ticker, max_tweets)

            # Try Method 2: Alternative scraping
            if not tweets:
                print(f"  Attempting alternative scraping for {name}...")
                tweets = self.scrape_twitter_alternative(name, ticker, max_tweets)

            # Fallback: Generate sample data
            if not tweets:
                print(f"  Using sample social media data for {name}...")
                tweets = self.generate_sample_tweets(name, ticker, 30)

            all_tweets[ticker] = tweets

            # Stream to Kafka
            for tweet in tweets:
                self.kafka.produce_to_kafka(
                    KAFKA_TOPICS['tweets'],
                    key=f"{ticker}_{tweet['tweet_id']}",
                    value=tweet
                )

            print(f"{name}: {len(tweets)} social media posts streamed")

        return all_tweets