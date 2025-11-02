import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
import numpy as np
np.seterr(all='ignore')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from market_analyzer import MarketAnalyzer
from datetime import datetime, timedelta

st.set_page_config(page_title="Trading Statistical Analysis", layout="wide")

POPULAR_STOCKS = {
    "US Stocks": {
        "Apple (AAPL)": "AAPL",
        "Microsoft (MSFT)": "MSFT",
        "Google (GOOGL)": "GOOGL",
        "Amazon (AMZN)": "AMZN",
        "Tesla (TSLA)": "TSLA",
        "NVIDIA (NVDA)": "NVDA",
        "Meta (META)": "META",
        "Netflix (NFLX)": "NFLX",
    },
    "International Stocks": {
        "Toyota (7203.T)": "7203.T",
        "Samsung (005930.KS)": "005930.KS",
        "ASML (ASML.AS)": "ASML.AS",
        "HSBC (HSBA.L)": "HSBA.L",
        "Sony (6758.T)": "6758.T",
    },
    "Indices": {
        "S&P 500 (^GSPC)": "^GSPC",
        "NASDAQ (^IXIC)": "^IXIC",
        "Dow Jones (^DJI)": "^DJI",
        "FTSE 100 (^FTSE)": "^FTSE",
        "Nikkei 225 (^N225)": "^N225",
    }
}

st.title("Statistical Trading Analysis Dashboard")
st.markdown("Analyze stocks, calculate indicators, and assess risk metrics")

col1, col2, col3 = st.columns(3)

with col1:
    stock_category = st.selectbox("Stock Category", list(POPULAR_STOCKS.keys()))

with col2:
    available_stocks = POPULAR_STOCKS[stock_category]
    selected_stock_name = st.selectbox("Select Stock", list(available_stocks.keys()))
    selected_symbol = available_stocks[selected_stock_name]

with col3:
    years_back = st.selectbox("Data Period", [1, 2, 3, 5], index=1)
    start_date = (datetime.now() - timedelta(days=years_back*365)).strftime("%Y-%m-%d")

if st.button("Analyze Stock", type="primary"):
    try:
        with st.spinner("Fetching data and calculating metrics..."):
            analyzer = MarketAnalyzer(symbol=selected_symbol, start_date=start_date)
            
            indicators = analyzer.calculate_indicators()
            risk_metrics = analyzer.calculate_risk_metrics()
        
        st.success(f"Analysis completed for {selected_stock_name}")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Indicators", "Risk Metrics", "Price Chart"])
        
        with tab1:
            st.subheader(f"Stock Analysis: {selected_stock_name} ({selected_symbol})")
            
            col1, col2, col3, col4 = st.columns(4)
            
            latest = indicators.iloc[-1]
            
            with col1:
                st.metric("Current Price", f"${latest['Close']:.2f}")
            
            with col2:
                if pd.notna(latest['SMA']):
                    st.metric("20-Day SMA", f"${latest['SMA']:.2f}")
            
            with col3:
                if pd.notna(latest['EMA']):
                    st.metric("20-Day EMA", f"${latest['EMA']:.2f}")
            
            with col4:
                if pd.notna(latest['Volatility']):
                    st.metric("Annualized Volatility", f"{latest['Volatility']:.2%}")
            
            st.markdown("---")
            st.subheader("Risk Metrics Summary")
            
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                if risk_metrics['Sharpe_Ratio']:
                    st.metric("Sharpe Ratio", f"{risk_metrics['Sharpe_Ratio']:.3f}")
            
            with metrics_col2:
                if risk_metrics['Value_at_Risk_5pct']:
                    st.metric("Value at Risk (5%)", f"{risk_metrics['Value_at_Risk_5pct']:.2%}")
            
            with metrics_col3:
                if risk_metrics['Maximum_Drawdown']:
                    st.metric("Max Drawdown", f"{risk_metrics['Maximum_Drawdown']:.2%}")
            
            with metrics_col4:
                if risk_metrics['Avg_Return_Annualized']:
                    st.metric("Avg Return (Annualized)", f"{risk_metrics['Avg_Return_Annualized']:.2%}")
        
        with tab2:
            st.subheader("Statistical Indicators")
            
            indicators_display = indicators[['Close', 'SMA', 'EMA', 'Volatility', 'Momentum']].tail(20)
            indicators_display = indicators_display.rename(columns={
                'Close': 'Price',
                'SMA': 'SMA (20)',
                'EMA': 'EMA (20)',
                'Volatility': 'Volatility (Annualized)',
                'Momentum': 'Momentum (10-day)'
            })
            
            st.dataframe(indicators_display.style.format({
                'Price': '${:.2f}',
                'SMA (20)': '${:.2f}',
                'EMA (20)': '${:.2f}',
                'Volatility (Annualized)': '{:.2%}',
                'Momentum (10-day)': '{:.2%}'
            }))
            
            st.line_chart(indicators[['Close', 'SMA', 'EMA']].tail(100))
        
        with tab3:
            st.subheader("Detailed Risk Metrics")
            
            risk_df = pd.DataFrame([risk_metrics]).T
            risk_df.columns = ['Value']
            risk_df = risk_df.dropna()
            
            for metric_name, metric_value in risk_df.iterrows():
                if isinstance(metric_value['Value'], (int, float)):
                    display_name = metric_name.replace('_', ' ')
                    if 'Return' in display_name or 'Volatility' in display_name or 'Var' in display_name or 'Drawdown' in display_name:
                        st.metric(display_name, f"{metric_value['Value']:.4f} ({metric_value['Value']:.2%})")
                    else:
                        st.metric(display_name, f"{metric_value['Value']:.4f}")
        
        with tab4:
            st.subheader("Price Chart with Indicators")
            
            chart_data = indicators[['Close', 'SMA', 'EMA']].tail(200)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(chart_data.index, chart_data['Close'], label='Close Price', linewidth=2)
            ax.plot(chart_data.index, chart_data['SMA'], label='SMA (20)', alpha=0.7)
            ax.plot(chart_data.index, chart_data['EMA'], label='EMA (20)', alpha=0.7)
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.set_title(f'{selected_stock_name} - Price and Moving Averages')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("---")
            
            if len(analyzer.data) > 0:
                price_stats = analyzer.data['Close'].describe()
                st.subheader("Price Statistics")
                st.write(f"**Period:** {pd.to_datetime(analyzer.data.index[0]).date()} to {pd.to_datetime(analyzer.data.index[-1]).date()}")
                st.write(f"**Trading Days:** {len(analyzer.data)}")
                st.write(f"**Highest Price:** ${price_stats['max']:.2f}")
                st.write(f"**Lowest Price:** ${price_stats['min']:.2f}")
                st.write(f"**Average Price:** ${price_stats['mean']:.2f}")
        
    except Exception as e:
        st.error(f"Error analyzing stock: {str(e)}")
        st.info("Please check your internet connection and try again. Make sure the stock symbol is valid.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Custom Stock Symbol")
custom_symbol = st.sidebar.text_input("Enter custom symbol (e.g., AAPL, TSLA, 7203.T)", "")
custom_start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365*2))

if st.sidebar.button("Analyze Custom Symbol") and custom_symbol:
    try:
        with st.sidebar.spinner("Analyzing..."):
            analyzer = MarketAnalyzer(symbol=custom_symbol, start_date=custom_start_date.strftime("%Y-%m-%d"))
            indicators = analyzer.calculate_indicators()
            risk_metrics = analyzer.calculate_risk_metrics()
        
        st.sidebar.success(f"Analysis for {custom_symbol}")
        latest = indicators.iloc[-1]
        st.sidebar.metric("Current Price", f"${latest['Close']:.2f}")
        if risk_metrics['Sharpe_Ratio']:
            st.sidebar.metric("Sharpe Ratio", f"{risk_metrics['Sharpe_Ratio']:.3f}")
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")

