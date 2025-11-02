import pandas as pd
import numpy as np
from datetime import datetime
from data_fetcher import DataFetcher
from statistical_indicators import StatisticalIndicators
from risk_metrics import RiskMetrics

class MarketAnalyzer:
    def __init__(self, symbol=None, data=None, start_date=None, end_date=None):
        self.fetcher = DataFetcher()
        self.symbol = symbol
        self.data = None
        self.indicators = None
        self.risk_metrics = None
        
        if data is not None:
            self.fetcher.data = data
            self.data = data
        elif symbol and start_date:
            self.data = self.fetcher.fetch_from_yahoo(symbol, start_date, end_date)
    
    def load_from_csv(self, file_path):
        self.data = self.fetcher.load_from_csv(file_path)
        return self.data
    
    def calculate_indicators(self, sma_period=20, ema_period=20, volatility_period=20):
        if self.data is None:
            raise ValueError("No data loaded. Load data first.")
        
        self.indicators = StatisticalIndicators(self.data)
        return self.indicators.get_all_indicators(sma_period, ema_period, volatility_period)
    
    def calculate_risk_metrics(self, risk_free_rate=0.02):
        if self.data is None:
            raise ValueError("No data loaded. Load data first.")
        
        self.risk_metrics = RiskMetrics(self.data)
        return self.risk_metrics.get_all_metrics(risk_free_rate)
    
    def correlation_analysis(self, other_analyzer):
        if self.data is None or other_analyzer.data is None:
            raise ValueError("Both analyzers must have data loaded.")
        
        returns1 = self.data['Close'].pct_change().dropna()
        returns2 = other_analyzer.data['Close'].pct_change().dropna()
        
        common_dates = returns1.index.intersection(returns2.index)
        if len(common_dates) < 30:
            return None
        
        returns1_aligned = returns1.loc[common_dates]
        returns2_aligned = returns2.loc[common_dates]
        
        correlation = np.corrcoef(returns1_aligned, returns2_aligned)[0, 1]
        
        return {
            'Correlation': correlation,
            'Common_Period': len(common_dates),
            'Symbol1': self.symbol or 'Asset1',
            'Symbol2': other_analyzer.symbol or 'Asset2'
        }
    
    def generate_report(self):
        if self.data is None:
            return "No data loaded."
        
        report = f"\n{'='*50}\n"
        report += f"Market Analysis Report\n"
        report += f"{'='*50}\n"
        
        if self.symbol:
            report += f"Symbol: {self.symbol}\n"
        date_start = pd.to_datetime(self.data.index[0]).date()
        date_end = pd.to_datetime(self.data.index[-1]).date()
        report += f"Data Period: {date_start} to {date_end}\n"
        report += f"Total Trading Days: {len(self.data)}\n"
        
        if self.risk_metrics:
            metrics = self.risk_metrics.get_all_metrics()
            report += f"\n--- Risk Metrics ---\n"
            for key, value in metrics.items():
                if value is not None:
                    if isinstance(value, float):
                        report += f"{key}: {value:.4f}\n"
                    else:
                        report += f"{key}: {value}\n"
        
        if self.indicators:
            latest_indicators = self.calculate_indicators()
            latest = latest_indicators.iloc[-1]
            report += f"\n--- Latest Indicators ---\n"
            report += f"Current Price: ${latest['Close']:.2f}\n"
            if pd.notna(latest['SMA']):
                report += f"20-Day SMA: ${latest['SMA']:.2f}\n"
            if pd.notna(latest['EMA']):
                report += f"20-Day EMA: ${latest['EMA']:.2f}\n"
            if pd.notna(latest['Volatility']):
                report += f"Volatility (Annualized): {latest['Volatility']:.4f}\n"
        
        report += f"\n{'='*50}\n"
        return report

