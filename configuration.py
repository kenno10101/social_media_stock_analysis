from datetime import datetime, timedelta

# Companies to analyze
COMPANIES = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOGL': 'Google',
    'TSLA': 'Tesla',
    'AMZN': 'Amazon'
}

# Time period
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365*5)  # 5 years

# API Keys
NEWS_API_KEY = "b8c2d650a35d4770abe8c90125eebe65"

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPICS = {
    'news': 'news_stream',
    'tweets': 'tweets_stream',
    'stocks': 'stock_prices'
}

# MongoDB Configuration
MONGO_URI = "mongodb://admin:password@localhost:27017/?authSource=admin"
DB_NAME = "stock_sentiment_bigdata"

# HDFS Configuration (or local simulation)
HDFS_BASE_PATH = "./hdfs_simulation"  # Local folder simulating HDFS
USE_REAL_HDFS = False  # Set to True if you have HDFS running

# Spark Configuration
SPARK_APP_NAME = "StockSentimentAnalysis"
