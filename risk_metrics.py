import pandas as pd
import numpy as np

class RiskMetrics:
    def __init__(self, price_data):
        if 'Close' not in price_data.columns:
            raise ValueError("Price data must contain 'Close' column")
        self.data = price_data.copy()
        self.returns = self.data['Close'].pct_change().dropna()
    
    def sharpe_ratio(self, risk_free_rate=0.02):
        if len(self.returns) == 0:
            return None
        
        avg_return = self.returns.mean() * 252
        volatility = self.returns.std() * np.sqrt(252)
        
        if volatility == 0:
            return None
        
        return (avg_return - risk_free_rate) / volatility
    
    def value_at_risk(self, confidence_level=0.05):
        if len(self.returns) == 0:
            return None
        return np.percentile(self.returns, confidence_level * 100)
    
    def maximum_drawdown(self):
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def annualized_return(self):
        if len(self.returns) == 0:
            return None
        return self.returns.mean() * 252
    
    def annualized_volatility(self):
        if len(self.returns) == 0:
            return None
        return self.returns.std() * np.sqrt(252)
    
    def get_all_metrics(self, risk_free_rate=0.02):
        return {
            'Sharpe_Ratio': self.sharpe_ratio(risk_free_rate),
            'Value_at_Risk_5pct': self.value_at_risk(0.05),
            'Maximum_Drawdown': self.maximum_drawdown(),
            'Avg_Return_Annualized': self.annualized_return(),
            'Volatility_Annualized': self.annualized_volatility()
        }

