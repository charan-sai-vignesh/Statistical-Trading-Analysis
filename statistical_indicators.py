import pandas as pd
import numpy as np
from scipy import stats

class StatisticalIndicators:
    def __init__(self, price_data):
        if 'Close' not in price_data.columns:
            raise ValueError("Price data must contain 'Close' column")
        self.data = price_data.copy()
        self.close = price_data['Close']
    
    def sma(self, period):
        return self.close.rolling(window=period).mean()
    
    def ema(self, period):
        return self.close.ewm(span=period, adjust=False).mean()
    
    def volatility(self, period=20):
        returns = self.close.pct_change()
        return returns.rolling(window=period).std() * np.sqrt(252)
    
    def rolling_std(self, period=20):
        return self.close.rolling(window=period).std()
    
    def trend_regression(self, period=20):
        trend_data = pd.DataFrame(index=self.data.index)
        trend_data['Slope'] = np.nan
        trend_data['R_Squared'] = np.nan
        
        for i in range(period - 1, len(self.close)):
            window_data = self.close.iloc[i - period + 1:i + 1]
            x = np.arange(len(window_data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, window_data.values)
            
            trend_data.iloc[i, 0] = slope
            trend_data.iloc[i, 1] = r_value ** 2
        
        return trend_data
    
    def price_momentum(self, period=10):
        return self.close.pct_change(periods=period)
    
    def get_all_indicators(self, sma_period=20, ema_period=20, volatility_period=20):
        indicators = pd.DataFrame(index=self.data.index)
        indicators['Close'] = self.close
        indicators['SMA'] = self.sma(sma_period)
        indicators['EMA'] = self.ema(ema_period)
        indicators['Volatility'] = self.volatility(volatility_period)
        indicators['Momentum'] = self.price_momentum()
        return indicators

