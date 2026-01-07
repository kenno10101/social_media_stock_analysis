import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import numpy as np
from configuration import COMPANIES

def create_visualizations(stock_data, sentiment_results, correlation_results):
    """Create comprehensive visualizations"""

    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70 + "\n")

    # 1. Sentiment Distribution
    fig1, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig1.suptitle('Sentiment Distribution by Company', fontsize=16, fontweight='bold')

    for idx, (ticker, name) in enumerate(COMPANIES.items()):
        ax = axes[idx // 3, idx % 3]

        if ticker in sentiment_results and not sentiment_results[ticker].empty:
            data = sentiment_results[ticker]

            ax.hist(data['sentiment_score'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax.axvline(data['sentiment_score'].mean(), color='red', linestyle='--',
                      label=f'Mean: {data["sentiment_score"].mean():.3f}')
            ax.set_title(f'{name} ({ticker})')
            ax.set_xlabel('Sentiment Score')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    # 2. Word Clouds
    print("Generating word clouds...")
    fig2, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig2.suptitle('Most Common Terms in Discussions', fontsize=16, fontweight='bold')

    for idx, (ticker, name) in enumerate(COMPANIES.items()):
        ax = axes[idx // 3, idx % 3]

        if ticker in sentiment_results and not sentiment_results[ticker].empty:
            text = ' '.join(sentiment_results[ticker]['text'].astype(str))

            wordcloud = WordCloud(width=400, height=300, background_color='white',
                                colormap='viridis').generate(text)

            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(f'{name} ({ticker})')
            ax.axis('off')

    plt.tight_layout()
    plt.show()

    # 3. Interactive Sentiment vs Stock Price Timeline
    print("Creating interactive charts...")

    for ticker in COMPANIES.keys():
        if ticker not in correlation_results:
            continue

        data = correlation_results[ticker]['data']

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(f'{COMPANIES[ticker]} Stock Price', 'Average Daily Sentiment'),
            vertical_spacing=0.15,
            row_heights=[0.6, 0.4]
        )

        # Stock price
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['Close'], name='Close Price',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )

        # Sentiment
        fig.add_trace(
            go.Scatter(x=data['date'], y=data['avg_sentiment'], name='Sentiment',
                      line=dict(color='green', width=2), fill='tozeroy'),
            row=2, col=1
        )

        fig.add_hline(y=0, line_dash="dash", line_color="red", row=2, col=1)

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Sentiment Score", row=2, col=1)

        fig.update_layout(
            title_text=f"{COMPANIES[ticker]} ({ticker}): Sentiment vs Stock Price",
            height=700,
            showlegend=True
        )

        fig.show()

    # 4. Correlation Summary
    fig3, ax = plt.subplots(figsize=(12, 6))

    tickers = []
    same_day = []
    next_day = []

    for ticker, results in correlation_results.items():
        tickers.append(ticker)
        same_day.append(results['same_day_correlation'])
        next_day.append(results['next_day_correlation'])

    x = np.arange(len(tickers))
    width = 0.35

    ax.bar(x - width/2, same_day, width, label='Same-Day Correlation', color='steelblue')
    ax.bar(x + width/2, next_day, width, label='Next-Day Correlation', color='coral')

    ax.set_xlabel('Company')
    ax.set_ylabel('Correlation Coefficient')
    ax.set_title('Sentiment-Stock Price Correlation Analysis', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    plt.show()

    print("All visualizations created!")