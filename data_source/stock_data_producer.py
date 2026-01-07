from configuration import KAFKA_TOPICS
from datetime import datetime
import yfinance as yf
import pandas as pd


class StockDataProducer:
    """Fetch stock data and stream to Kafka"""

    def __init__(self, kafka_layer):
        self.kafka = kafka_layer

    def fetch_and_stream(self, tickers, start_date, end_date):
        """Fetch stock data and produce to Kafka"""
        stock_data = {}

        print("\nFetching Stock Data and Streaming to Kafka...")
        print("-" * 70)

        for ticker in tickers:
            print(f"Processing {ticker}...")
            try:
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)

                # Fix MultiIndex columns
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                stock_data[ticker] = data

                # Stream to Kafka
                for date, row in data.iterrows():
                    message = {
                        'ticker': ticker,
                        'date': date.strftime('%Y-%m-%d'),
                        'open': float(row['Open']),
                        'high': float(row['High']),
                        'low': float(row['Low']),
                        'close': float(row['Close']),
                        'volume': int(row['Volume']),
                        'timestamp': datetime.now().isoformat()
                    }

                    self.kafka.produce_to_kafka(
                        KAFKA_TOPICS['stocks'],
                        key=f"{ticker}_{date.strftime('%Y%m%d')}",
                        value=message
                    )

                print(f"{ticker}: {len(data)} records streamed")

            except Exception as e:
                print(f"Error: {e}")

        return stock_data