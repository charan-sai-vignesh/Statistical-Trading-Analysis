from market_analyzer import MarketAnalyzer

def example_usage():
    print("Statistical Trading Analysis - Example Usage\n")
    
    analyzer1 = MarketAnalyzer(symbol="AAPL", start_date="2022-01-01")
    
    indicators = analyzer1.calculate_indicators()
    print(f"\nLatest indicators:\n{indicators.tail()}")
    
    risk_metrics = analyzer1.calculate_risk_metrics()
    print("\nRisk Metrics:")
    for key, value in risk_metrics.items():
        if value is not None:
            print(f"  {key}: {value:.4f}")
    
    print(analyzer1.generate_report())
    
    analyzer2 = MarketAnalyzer(symbol="MSFT", start_date="2022-01-01")
    correlation = analyzer1.correlation_analysis(analyzer2)
    if correlation:
        print(f"Correlation: {correlation['Correlation']:.4f}")

if __name__ == "__main__":
    example_usage()

