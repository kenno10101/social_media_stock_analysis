Stock Sentiment Analysis: News & Social Media Impact on Stock Prices
A University Project by BECER Dicle and SANGA Kenn-Michael

This notebook analyzes sentiment from news articles and social media (Reddit)
and correlates it with stock price movements over the past 5 years.

Data Sources:
- News: NewsAPI.org (alternative: web scraping from Google News)
- Social Media: Reddit API (praw)
- Stock Data: Yahoo Finance (yfinance)

Storage: MongoDB for structured data storage
Analysis: VADER & TextBlob for sentiment analysis
Visualization: Plotly, Matplotlib, WordCloud


# STOCK SENTIMENT ANALYSIS - QUICK SETUP SCRIPT
# Copy-paste these commands one section at a time
# STEP 1: INSTALL DOCKER DESKTOP FIRST!
# Download from: https://www.docker.com/products/docker-desktop
# Install it, then come back here

# Verify Docker is installed:
docker --version
docker ps

# STEP 2: INSTALL PYTHON PACKAGES


# Minimal installation (5 minutes):
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn plotly
pip install yfinance requests beautifulsoup4
pip install vaderSentiment textblob
pip install pyarrow wordcloud pymongo kafka-python
pip install jupyter notebook

# Or
pip install -r requirements.txt

# Download TextBlob data:
python -m textblob.download_corpora

# Verify:
python3 -c "import pandas, yfinance, vaderSentiment; print('✅ Packages work!')"


# STEP 3: START DOCKER SERVICES
Start all services (first time will download images):
docker-compose up -d

# STEP 4: GET NEWSAPI KEY

1. Go to: https://newsapi.org/register
2. Sign up (free)
3. Copy your API key

# STEP 5: START JUPYTER NOTEBOOK

# DONE! Now in Jupyter:
# 1. Add your NewsAPI key
# 2. Run the cells!



# USEFUL COMMANDS FOR LATER:


# To stop services:
docker-compose stop

# To restart services (next day):
docker-compose start

# To see logs:
# docker logs kafka
docker logs mongodb

# To completely remove everything:
docker-compose down -v

# Daily workflow:
cd ~/stock-sentiment-project
docker-compose start
source venv/bin/activate
jupyter notebook
`