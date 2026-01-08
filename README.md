# Stock Sentiment Analysis: News & Social Media Impact on Stock Prices

**Authors:** BECER Dicle, SANGA Kenn-Michael  


## Project Overview

This project implements a Big Data pipeline to analyze the correlation between news sentiment and stock price movements. The system employs Apache Kafka for streaming, Spark for processing, and a hybrid storage solution (HDFS + MongoDB) to demonstrate enterprise-grade data architecture.

### Key Features

- Real-time data streaming architecture using Apache Kafka
- Multi-source sentiment analysis (news articles and social media)
- Ensemble NLP models (VADER, TextBlob, Transformers)
- Distributed storage (HDFS simulation + MongoDB)
- Statistical correlation analysis
- Interactive visualizations

### Data Sources

- **News:** NewsAPI.org
- **Social Media:** Twitter/X (web scraping) or sample data
- **Stock Data:** Yahoo Finance API (5-year historical data)

### Technology Stack

- **Streaming Layer:** Apache Kafka
- **Processing:** Apache Spark (with pandas fallback)
- **Storage:** MongoDB, HDFS (Parquet format)
- **NLP:** VADER, TextBlob, DistilBERT
- **Visualization:** Plotly, Matplotlib, Seaborn

---

## Prerequisites

### Required Software

1. **Docker Desktop** (for Kafka and MongoDB)
2. **Python 3.11+** (Python 3.13 compatible)
3. **Java 11+** (required for Apache Spark)

### Optional Software

- **MongoDB Compass** (database GUI)
- **Apache Spark** (local installation)

---

## Installation Guide

### Step 1: Install Docker Desktop

#### macOS
```bash
# Download Docker Desktop
# Visit: https://www.docker.com/products/docker-desktop

# Or install via Homebrew
brew install --cask docker

# Launch Docker Desktop
open -a Docker

# Verify installation
docker --version
docker ps
```

#### Windows
```bash
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop

# Run installer and follow prompts
# After installation, verify:
docker --version
docker ps
```

#### Linux
```bash
# Install Docker Engine
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker --version
```

---

### Step 2: Install Java (Required for Spark)

#### macOS
```bash
# Check if Java is installed
java -version

# If not installed, use Homebrew
brew install openjdk@11

# Set JAVA_HOME
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 11)' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
java -version
echo $JAVA_HOME
```

#### Windows
```bash
# Download Java JDK 11 from:
# https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html

# Or use Chocolatey
choco install openjdk11

# Set JAVA_HOME environment variable:
# Control Panel > System > Advanced System Settings > Environment Variables
# Add: JAVA_HOME = C:\Program Files\Java\jdk-11

# Verify
java -version
```

#### Linux (Ubuntu/Debian)
```bash
# Install OpenJDK 11
sudo apt-get update
sudo apt-get install openjdk-11-jdk

# Set JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
java -version
echo $JAVA_HOME
```

---

### Step 3: Clone Repository and Setup Project

```bash
# Create project directory
mkdir stock-sentiment-project
cd stock-sentiment-project

# Create subdirectories
mkdir notebooks data hdfs_simulation

# Download project files (docker-compose.yml, requirements.txt, notebook)
# Or clone repository
git clone <repository-url> .
```

---

### Step 4: Install Python Dependencies

#### Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### Install Required Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# Or install manually:
pip install pandas numpy matplotlib seaborn plotly
pip install yfinance requests beautifulsoup4
pip install vaderSentiment textblob
pip install pyarrow wordcloud pymongo kafka-python
pip install jupyter notebook

# Optional (for advanced features):
pip install pyspark transformers torch

# Download TextBlob corpora
python -m textblob.download_corpora
```

#### Verify Installation

```bash
python3 -c "import pandas, yfinance, vaderSentiment; print('All packages installed successfully')"
```

---

### Step 5: Start Docker Services

#### Configure Services

Ensure `docker-compose.yml` is in your project directory with the following services:
- Zookeeper (Kafka dependency)
- Kafka (streaming)
- MongoDB (storage)
- Mongo Express (web UI)

#### Start Services

```bash
# Start all services in background
docker-compose up -d

# Wait for services to initialize (30 seconds)
sleep 30

# Verify all containers are running
docker ps

# Expected output: 4 containers (zookeeper, kafka, mongodb, mongo-express)
```

#### Verify Services

```bash
# Check Kafka
docker logs kafka --tail 20

# Check MongoDB
docker logs mongodb --tail 20

# Access MongoDB Web UI
# Open browser: http://localhost:8081
```

---

### Step 6: Configure API Keys

#### NewsAPI (Required)

1. Register at: https://newsapi.org/register
2. Choose free tier (100 requests/day)
3. Verify email and copy API key
4. Add to notebook configuration:

```python
NEWS_API_KEY = "your_api_key_here"
```

#### Twitter/X (Optional)

Twitter scraping is automated via `snscrape` and requires no API key. If scraping fails, the system automatically generates sample data.

---

### Step 7: Run Jupyter Notebook

```bash
# Ensure virtual environment is active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start Jupyter Notebook
jupyter notebook

# Browser will open automatically at http://localhost:8888
```

#### Configure Notebook

1. Open `Stock_Sentiment_Analysis.ipynb`
2. Update configuration cell with your NewsAPI key
3. Run all cells in sequence

---

## Usage

### Daily Workflow

```bash
# 1. Start Docker services
cd stock-sentiment-project
docker-compose start

# 2. Activate Python environment
source venv/bin/activate

# 3. Start Jupyter Notebook
jupyter notebook

# 4. Run analysis in notebook: presentation.ipynb
```

## Data Pipeline Architecture

```
[Data Sources]
    ↓
[Kafka Producers] → [Kafka Topics]
    ↓
[Spark Processing] (or pandas fallback)
    ↓
[HDFS + MongoDB Storage]
    ↓
[Analytics & Visualization]
```

### Pipeline Components

1. **Data Ingestion:** Kafka producers stream data from APIs
2. **Message Queues:** Kafka topics (news_stream, tweets_stream, stock_prices)
3. **Processing:** Spark (or pandas) for sentiment analysis
4. **Storage:** HDFS (Parquet) + MongoDB (JSON documents)
5. **Analysis:** Correlation calculations and statistical tests
6. **Output:** Interactive visualizations and reports

---

## Configuration Options

### Companies to Analyze

Edit in notebook configuration:

```python
COMPANIES = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOGL': 'Google',
    'TSLA': 'Tesla',
    'AMZN': 'Amazon'
}
```

### Time Period

```python
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365*5)  # 5 years
```

### Sentiment Models

```python
# Available models:
# - VADER (social media)
# - TextBlob (news articles)
# - DistilBERT (advanced, requires transformers)
# - Ensemble (combines all)
```

---

## Troubleshooting

### Docker Issues

**Problem:** "Cannot connect to Docker daemon"
```bash
# Solution: Start Docker Desktop
open -a Docker  # macOS
# or start from Applications menu
```

**Problem:** "Port already in use"
```bash
# Solution: Kill process or change port
lsof -ti:9092 | xargs kill -9  # Kill Kafka port
# Edit docker-compose.yml to use different port
```

### Python Package Issues

**Problem:** "ImportError: No module named..."
```bash
# Solution: Reinstall package
pip install --upgrade package-name

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

### Java/Spark Issues

**Problem:** "Java gateway process exited"
```bash
# Solution: Verify Java installation
java -version
echo $JAVA_HOME

# Set JAVA_HOME if missing
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

**Problem:** "Spark not available"
```bash
# Solution: System automatically uses pandas fallback
# No action needed - analysis will still work
```

### MongoDB Issues

**Problem:** "Cannot connect to MongoDB"
```bash
# Solution: Restart MongoDB container
docker restart mongodb

# Verify it's running
docker logs mongodb
```

### API Issues

**Problem:** "NewsAPI returns 401"
```bash
# Solution: Check API key is correct
# Verify at: https://newsapi.org/account
# Ensure no extra spaces in key
```

---

## Running Without Docker (Simulation Mode)

If Docker is unavailable, the system automatically runs in simulation mode:

```bash
# Install only essential packages
pip install pandas yfinance vaderSentiment textblob matplotlib plotly

# Run notebook - services will be simulated
jupyter notebook
```

**What happens in simulation mode:**
- Kafka: Messages printed to console instead of streamed
- MongoDB: Data stored in memory only
- Spark: Uses pandas for processing
- Analysis: Fully functional with same results

---

## Service Management

### Start Services
```bash
docker-compose start
```

### Stop Services
```bash
docker-compose stop
```

### Restart Services
```bash
docker-compose restart
```

### View Logs
```bash
docker logs kafka
docker logs mongodb
docker-compose logs -f  # Follow all logs
```

### Remove All Data
```bash
docker-compose down -v  # Removes volumes
```

---

## Output Files

### HDFS Storage (Parquet files)
```
hdfs_simulation/stock_data/AAPL.parquet
hdfs_simulation/sentiment_data/AAPL.parquet
```

### MongoDB Collections
```
Database: stock_sentiment_bigdata
Collections: sentiment_AAPL, sentiment_MSFT, etc.
```

### Visualizations
Generated in Jupyter Notebook:
- Sentiment distribution histograms
- Word clouds
- Time-series charts (sentiment vs price)
- Correlation bar charts

---

## Performance Notes

- Free NewsAPI tier: 100 requests/day, 30-day history only
- Stock data: Full 5-year history available
- Processing time: ~2-3 minutes for 5 companies
- Memory usage: ~500MB-1GB during analysis

---

## Acknowledgments

- NewsAPI.org for news data access
- Yahoo Finance for stock market data
- Apache Software Foundation for Kafka and Spark
- NLTK and TextBlob contributors for NLP tools

---

## Support

For technical issues:
1. Check Troubleshooting section
2. Verify all services are running: `docker ps`
3. Check logs: `docker logs <container-name>`
4. Ensure virtual environment is active
5. Verify API keys are configured correctly