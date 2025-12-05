import json
import time
import requests
from datetime import datetime, timedelta
from kafka import KafkaProducer
from kafka.errors import KafkaError
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.api_keys import (
    NEWS_API_KEY, 
    KAFKA_BOOTSTRAP_SERVERS, 
    KAFKA_NEWS_TOPIC,
    TRACKED_COMPANIES,
    COMPANY_MAPPING
)


class NewsProducer:
    def __init__(self):
        """Initialize Kafka producer and NewsAPI connection"""
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
        
    def fetch_news(self, company_symbol, company_name, from_date, to_date):
        """
        Fetch news articles for a specific company from NewsAPI
        
        Args:
            company_symbol: Stock ticker (e.g., 'AAPL')
            company_name: Company name (e.g., 'Apple')
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
        """
        params = {
            'q': company_name,  # Search query
            'from': from_date,
            'to': to_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': self.api_key,
            'pageSize': 100  # Max articles per request
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                print(f"✓ Fetched {data['totalResults']} articles for {company_name}")
                return data['articles']
            else:
                print(f"✗ Error fetching news: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed for {company_name}: {e}")
            return []
    
    def send_to_kafka(self, company_symbol, article):
        """
        Send a news article to Kafka topic
        
        Args:
            company_symbol: Stock ticker to use as message key
            article: Article data dict
        """
        # Enrich article with metadata
        message = {
            'company_symbol': company_symbol,
            'company_name': COMPANY_MAPPING.get(company_symbol, company_symbol),
            'source': article.get('source', {}).get('name', 'Unknown'),
            'author': article.get('author', 'Unknown'),
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'published_at': article.get('publishedAt', ''),
            'content': article.get('content', ''),
            'fetched_at': datetime.utcnow().isoformat()
        }
        
        try:
            # Send to Kafka with company symbol as key (for partitioning)
            future = self.producer.send(
                KAFKA_NEWS_TOPIC,
                key=company_symbol,
                value=message
            )
            
            # Block for 'synchronous' sends
            record_metadata = future.get(timeout=10)
            print(f"  → Sent to Kafka: {message['title'][:60]}... "
                  f"[partition: {record_metadata.partition}]")
            
        except KafkaError as e:
            print(f"✗ Failed to send message: {e}")
    
    def run(self, days_back=7, interval_seconds=3600):
        """
        Main loop: fetch news and send to Kafka
        
        Args:
            days_back: How many days of historical news to fetch
            interval_seconds: How often to fetch new articles (default: 1 hour)
        """
        print(f"Starting News Producer for companies: {TRACKED_COMPANIES}")
        print(f"Kafka Topic: {KAFKA_NEWS_TOPIC}")
        print(f"Fetching articles from last {days_back} days")
        print("-" * 60)
        
        while True:
            try:
                # Calculate date range
                to_date = datetime.utcnow().date()
                from_date = to_date - timedelta(days=days_back)
                
                # Fetch news for each tracked company
                for company_symbol in TRACKED_COMPANIES:
                    company_name = COMPANY_MAPPING.get(company_symbol, company_symbol)
                    
                    print(f"\nFetching news for {company_name} ({company_symbol})...")
                    articles = self.fetch_news(
                        company_symbol,
                        company_name,
                        from_date.isoformat(),
                        to_date.isoformat()
                    )
                    
                    # Send each article to Kafka
                    for article in articles:
                        self.send_to_kafka(company_symbol, article)
                    
                    # Small delay between companies to avoid rate limits
                    time.sleep(2)
                
                print(f"\n{'='*60}")
                print(f"Batch complete. Next fetch in {interval_seconds} seconds...")
                print(f"{'='*60}\n")
                
                # Wait before next fetch cycle
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                print("\n\nShutting down News Producer...")
                break
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
                time.sleep(60)  # Wait a minute before retrying
        
        # Clean up
        self.producer.flush()
        self.producer.close()
        print("News Producer stopped.")


if __name__ == "__main__":
    # Check if API key is configured
    if not NEWS_API_KEY or NEWS_API_KEY == 'your_newsapi_key_here':
        print("ERROR: NEWS_API_KEY not configured!")
        print("Please set your NewsAPI key in the .env file")
        print("Get a free key at: https://newsapi.org/")
        sys.exit(1)
    
    producer = NewsProducer()
    
    # For initial testing: fetch last 7 days, then check every hour
    producer.run(days_back=7, interval_seconds=3600)