from data_source.kafka_streaming_layer import KafkaStreamingLayer
from data_source.spark_processor import SparkProcessor
from data_source.stock_data_producer import StockDataProducer
from data_source.news_data_producer import NewsDataProducer
from data_source.twitter_data_producer import TwitterDataProducer
from data_storage.hdfs_storage import HDFSStorage
from data_storage.mongodb_storage import MongoStorage
from data_analysis.sentiment_analyzer import AdvancedSentimentAnalyzer
from configuration import *
import pandas as pd

def run_enhanced_pipeline():
    """Main Big Data pipeline: Kafka → Spark → HDFS/MongoDB"""

    print("\n" + "="*70)
    print("ENHANCED BIG DATA PIPELINE")
    print("   Architecture: Kafka → Spark → HDFS + MongoDB")
    print("="*70)

    # Initialize components
    print("\nInitializing Components...")
    kafka_layer = KafkaStreamingLayer(KAFKA_BOOTSTRAP_SERVERS)
    spark_processor = SparkProcessor()
    hdfs_storage = HDFSStorage(HDFS_BASE_PATH, USE_REAL_HDFS)
    mongo_storage = MongoStorage(MONGO_URI, DB_NAME)
    analyzer = AdvancedSentimentAnalyzer()

    # Step 1: Data Collection with Kafka Producers
    print("\n" + "="*70)
    print("STEP 1: DATA INGESTION → KAFKA STREAMING")
    print("="*70)

    stock_producer = StockDataProducer(kafka_layer)
    stock_data = stock_producer.fetch_and_stream(list(COMPANIES.keys()), START_DATE, END_DATE)

    if NEWS_API_KEY != "YOUR_NEWSAPI_KEY_HERE":
        news_producer = NewsDataProducer(kafka_layer, NEWS_API_KEY)
        news_data = news_producer.fetch_and_stream(COMPANIES)
    else:
        print("\nNewsAPI not configured - skipping")
        news_data = {ticker: [] for ticker in COMPANIES.keys()}

    twitter_producer = TwitterDataProducer(kafka_layer)
    twitter_data = twitter_producer.scrape_and_stream(COMPANIES, max_tweets=50)

    # Step 2: Sentiment Analysis with Multiple Models
    print("\n" + "="*70)
    print("STEP 2: SENTIMENT ANALYSIS (Multi-Model Ensemble)")
    print("="*70)

    sentiment_results = {}

    for ticker in COMPANIES.keys():
        all_sentiments = []

        # Process news
        for article in news_data.get(ticker, []):
            text = f"{article.get('title', '')} {article.get('description', '')}"
            score = analyzer.analyze_ensemble(text)

            all_sentiments.append({
                'ticker': ticker,
                'date': article.get('publishedAt', '')[:10],
                'text': text[:200],
                'sentiment_score': score,
                'sentiment_category': analyzer.categorize_sentiment(score),
                'source': 'news',
                'model': 'ensemble'
            })

        # Process tweets
        for tweet in twitter_data.get(ticker, []):
            score = analyzer.analyze_ensemble(tweet['text'])

            all_sentiments.append({
                'ticker': ticker,
                'date': tweet['created_at'][:10],
                'text': tweet['text'][:200],
                'sentiment_score': score,
                'sentiment_category': analyzer.categorize_sentiment(score),
                'source': 'twitter',
                'model': 'ensemble',
                'likes': tweet.get('likes', 0)
            })

        sentiment_results[ticker] = pd.DataFrame(all_sentiments)
        print(f"{ticker}: {len(all_sentiments)} items analyzed")

    # Step 3: Spark Processing
    print("\n" + "="*70)
    print("STEP 3: SPARK PROCESSING")
    print("="*70)

    if spark_processor.spark:
        for ticker in COMPANIES.keys():
            if not sentiment_results[ticker].empty:
                sentiment_results[ticker] = spark_processor.process_with_spark(
                    sentiment_results[ticker],
                    'sentiment'
                )

    # Step 4: Storage (HDFS + MongoDB)
    print("\n" + "="*70)
    print("STEP 4: DISTRIBUTED STORAGE")
    print("="*70)

    print("\nStoring in HDFS (Parquet format)...")
    for ticker in COMPANIES.keys():
        if ticker in stock_data and not stock_data[ticker].empty:
            hdfs_storage.write_parquet(stock_data[ticker], f"stock_data/{ticker}.parquet")

        if not sentiment_results[ticker].empty:
            hdfs_storage.write_parquet(sentiment_results[ticker], f"sentiment_data/{ticker}.parquet")

    print("\nStoring in MongoDB...")
    for ticker in COMPANIES.keys():
        if not sentiment_results[ticker].empty:
            mongo_storage.store_documents(f"sentiment_{ticker}", sentiment_results[ticker])

    # Step 5: Calculate Correlations
    print("\n" + "="*70)
    print("STEP 5: CORRELATION ANALYSIS")
    print("="*70)

    correlation_results = {}

    for ticker in COMPANIES.keys():
        if sentiment_results[ticker].empty:
            continue

        sentiment_df = sentiment_results[ticker].copy()
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])

        daily_sentiment = sentiment_df.groupby('date').agg({
            'sentiment_score': ['mean', 'std', 'count']
        }).reset_index()
        daily_sentiment.columns = ['date', 'avg_sentiment', 'sentiment_std', 'num_posts']

        if ticker in stock_data:
            stock_df = stock_data[ticker].copy().reset_index()

            if 'Date' in stock_df.columns:
                stock_df = stock_df.rename(columns={'Date': 'date'})
            elif stock_df.columns[0] != 'date':
                stock_df = stock_df.rename(columns={stock_df.columns[0]: 'date'})

            stock_df['daily_return'] = stock_df['Close'].pct_change()

            merged = pd.merge(daily_sentiment, stock_df[['date', 'Close', 'daily_return']],
                            on='date', how='inner')

            if len(merged) > 10:
                corr_same_day = merged['avg_sentiment'].corr(merged['daily_return'])
                merged['next_day_return'] = merged['daily_return'].shift(-1)
                corr_next_day = merged['avg_sentiment'].corr(merged['next_day_return'])

                correlation_results[ticker] = {
                    'same_day_correlation': corr_same_day,
                    'next_day_correlation': corr_next_day,
                    'data': merged,
                    'num_observations': len(merged)
                }

                print(f"{ticker}: Same-day={corr_same_day:.3f}, Next-day={corr_next_day:.3f}")

    # Cleanup
    kafka_layer.close()
    spark_processor.stop()

    print("\n" + "="*70)
    print("PIPELINE COMPLETE!")
    print("="*70)

    return stock_data, sentiment_results, correlation_results