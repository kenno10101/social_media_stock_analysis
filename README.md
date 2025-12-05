# Sentiment Analysis of News on Stock Prices

A data engineering project that streams news articles into Kafka and analyzes their sentiment impact on stock prices.

## Team
- Becer Dicle
- Sanga Kenn-Michael

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- NewsAPI Key (free at [newsapi.org](https://newsapi.org/))

### Setup Steps

1. **Clone and navigate to project:**
```bash
cd sentiment-stock-analysis
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API keys:**
```bash
cp .env.example .env
# Edit .env and add your NEWS_API_KEY
```

4. **Start infrastructure (Kafka, MongoDB):**
```bash
chmod +x scripts/setup_kafka_topics.sh
(bash) ./scripts/setup_kafka_topics.sh
```

5. **Run the news producer:**
```bash
python producers/news_producer.py
```

### Verify It's Working

1. **Check Kafka UI:** Visit [http://localhost:8090](http://localhost:8090)
   - You should see the `news_stream` topic
   - Messages should be appearing as the producer runs

2. **Monitor Kafka messages directly:**
```bash
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic news_stream \
  --from-beginning
```

3. **Check Docker logs:**
```bash
docker-compose logs -f kafka
```

## Current Features

✅ Docker-based Kafka + Zookeeper setup  
✅ MongoDB for data storage  
✅ Kafka UI for monitoring  
✅ News producer fetching articles from NewsAPI  
✅ Automatic topic creation  
✅ Company-based news tracking (AAPL, GOOGL, MSFT, TSLA, AMZN)

## Next Steps

- [ ] Add Spark Structured Streaming consumer
- [ ] Implement sentiment analysis with FinBERT
- [ ] Create stock price producer (Yahoo Finance)
- [ ] Build correlation analysis
- [ ] Develop Jupyter notebooks with visualizations

## Configuration

Edit `.env` to customize:
- `NEWS_API_KEY`: Your NewsAPI key
- `TRACKED_COMPANIES`: Comma-separated stock symbols to track
- `KAFKA_NEWS_TOPIC`: Kafka topic name for news

## Troubleshooting

**Kafka not starting:**
```bash
docker-compose down -v
docker-compose up -d
```

**Can't connect to Kafka:**
- Ensure ports 9092, 2181, 27017, 8090 are not in use
- Check Docker logs: `docker-compose logs kafka`

**NewsAPI rate limits:**
- Free tier: 100 requests/day
- Adjust `interval_seconds` in producer to fetch less frequently

## Useful Commands

```bash
# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# List Kafka topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Delete a topic
docker exec kafka kafka-topics --delete --topic news_stream --bootstrap-server localhost:9092

# Connect to MongoDB
docker exec -it mongodb mongosh -u admin -p password123
```

## License

Educational project for data engineering coursework.