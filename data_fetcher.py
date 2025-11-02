import pandas as pd
import yfinance as yf

class DataFetcher:
    def __init__(self):
        self.data = None
    
    def fetch_from_yahoo(self, symbol, start_date, end_date=None):
        try:
            ticker = yf.Ticker(symbol)
            self.data = ticker.history(start=start_date, end=end_date)
            
            if self.data.empty or len(self.data) == 0:
                try:
                    if end_date:
                        self.data = yf.download(symbol, start=start_date, end=end_date, progress=False, timeout=10)
                    else:
                        self.data = yf.download(symbol, start=start_date, progress=False, timeout=10)
                    
                    if isinstance(self.data.columns, pd.MultiIndex):
                        self.data = self.data.iloc[:, 0]
                except Exception:
                    pass
            
            if self.data.empty or len(self.data) == 0:
                from yahooquery import Ticker
                yq = Ticker(symbol)
                hist = yq.history(start=start_date, end=end_date)
                if not hist.empty:
                    if isinstance(hist.index, pd.MultiIndex):
                        hist = hist.reset_index().set_index('date')
                    hist.columns = [col.capitalize() if col.lower() != 'volume' else 'Volume' for col in hist.columns]
                    if all(col in hist.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
                        hist = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
                        self.data = hist
            
            if self.data.empty or len(self.data) == 0:
                raise ValueError(f"No data found for {symbol}")
        except Exception as e:
            if self.data is None or self.data.empty:
                raise ValueError(f"No data found for {symbol}")
        
        return self.data
    
    def load_from_csv(self, file_path, date_column='Date'):
        self.data = pd.read_csv(file_path)
        if date_column in self.data.columns:
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            self.data.set_index(date_column, inplace=True)
        return self.data

