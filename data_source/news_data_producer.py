from configuration import END_DATE, START_DATE, KAFKA_TOPICS
from datetime import datetime, timedelta
import time
import requests


class NewsDataProducer:
    """Fetch news and stream to Kafka"""

    def __init__(self, kafka_layer, api_key):
        self.kafka = kafka_layer
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_and_stream(self, companies):
        """Fetch news articles and produce to Kafka"""
        all_news = {}

        print("\nFetching News and Streaming to Kafka...")
        print("-" * 70)

        for ticker, name in companies.items():
            query_end = END_DATE
            query_start = max(START_DATE, END_DATE - timedelta(days=30))

            params = {
                'q': f'{name} OR {ticker}',
                'from': query_start.strftime('%Y-%m-%d'),
                'to': query_end.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'relevancy',
                'apiKey': self.api_key,
                'pageSize': 100
            }

            try:
                response = requests.get(self.base_url, params=params)
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    all_news[ticker] = articles

                    # Stream to Kafka
                    for idx, article in enumerate(articles):
                        message = {
                            'ticker': ticker,
                            'company': name,
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'content': article.get('content', ''),
                            'url': article.get('url', ''),
                            'published_at': article.get('publishedAt', ''),
                            'source': article.get('source', {}).get('name', ''),
                            'timestamp': datetime.now().isoformat()
                        }

                        self.kafka.produce_to_kafka(
                            KAFKA_TOPICS['news'],
                            key=f"{ticker}_{idx}",
                            value=message
                        )

                    print(f"{name}: {len(articles)} articles streamed")
                else:
                    print(f"{name}: API returned {response.status_code}")

                time.sleep(1)

            except Exception as e:
                print(f"{name}: {e}")

        return all_news
