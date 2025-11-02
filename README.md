# Trading Statistical Analysis Dashboard

A Streamlit-based web application for analyzing stock market data with statistical indicators and risk metrics.

## Features

- Stock market data analysis
- Statistical indicators (SMA, EMA, Volatility, Momentum)
- Risk metrics calculation (Sharpe Ratio, VaR, Max Drawdown)
- Price charts and visualizations
- Support for US stocks, international stocks, and major indices
- Custom symbol input

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Deployment
The app will be available at: 'https://statistical-trading-analysis.streamlit.app/'
## Requirements

- Python 3.8+
- pandas
- numpy
- yfinance
- yahooquery
- matplotlib
- scipy
- streamlit

## Project Structure

- `app.py` - Main Streamlit application
- `market_analyzer.py` - Core analysis engine
- `data_fetcher.py` - Data fetching module
- `statistical_indicators.py` - Statistical calculations
- `risk_metrics.py` - Risk metrics calculations
- `requirements.txt` - Python dependencies
