#!/bin/bash

echo "================================"
echo "Sentiment Analysis Pipeline Setup"
echo "================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env and add your NEWS_API_KEY${NC}"
    echo "Get a free API key at: https://newsapi.org/"
    exit 1
fi

# Step 2: Start Docker containers
echo -e "${GREEN}Starting Docker containers...${NC}"
docker compose up -d

# Step 3: Wait for services to be ready
echo -e "${GREEN}Waiting for Kafka to be ready...${NC}"
sleep 15

# Step 4: Create Kafka topics (optional - auto-create is enabled)
echo -e "${GREEN}Creating Kafka topics...${NC}"
docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --topic news_stream \
    --partitions 3 \
    --replication-factor 1 \
    --if-not-exists

docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --topic tweets_stream \
    --partitions 3 \
    --replication-factor 1 \
    --if-not-exists

docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --topic stock_prices \
    --partitions 3 \
    --replication-factor 1 \
    --if-not-exists

# Step 5: List topics to verify
echo -e "${GREEN}Available Kafka topics:${NC}"
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Access Kafka UI at: http://localhost:8090"
echo "MongoDB available at: localhost:27017"
echo ""
echo "To start the news producer, run:"
echo "  python producers/news_producer.py"
echo ""
echo "To view Kafka messages:"
echo "  docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic news_stream --from-beginning"