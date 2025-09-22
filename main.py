from data_loader import MarketDataReader
from strategies import MovingAverageCrossover, Momentum
from engine import BackTestengine
from reporting import PerformanceReporter

def run_backtest(csv_path: str = None, generate_report: bool = True):
    """
    Run complete backtest with performance reporting
    
    Args:
        csv_path: Path to market data CSV file
        generate_report: Whether to generate performance.md report
        
    Returns:
        Dictionary containing backtest results and performance metrics
    """
    print("Starting backtest...")
    
    if csv_path is None:
        import os
        csv_path = os.path.join(os.path.dirname(__file__), "market_data.csv")
    
    # Load market data
    reader = MarketDataReader(csv_path)
    reader.read_data()
    data = reader.fetch_data()
    print(f"Loaded {len(data)} market data points")

    # Initialize strategies
    symbols = sorted({t.symbol for t in data})
    strategies = []
    for sym in symbols:
        strategies.append(MovingAverageCrossover(symbol=sym, short_window=3, long_window=8, trade_qty=2))
        strategies.append(Momentum(symbol=sym, lookback=5, threshold_pct=0.01, trade_qty=1))
    
    print(f"Initialized {len(strategies)} strategies for {len(symbols)} symbols")

    # Run backtest
    engine = BackTestengine(strategies)
    engine.run(data)
    backtest_report = engine.report()
    
    print(f"Backtest completed. Generated {len(backtest_report['orders'])} orders")
    print(f"Final positions: {backtest_report['positions']}")
    print(f"Errors encountered: {len(backtest_report['errors'])}")
    
    # Generate performance report if requested
    if generate_report:
        print("Generating performance report...")
        reporter = PerformanceReporter(initial_capital=10000.0, risk_free_rate=0.02)
        report_content = reporter.generate_performance_report(backtest_report, "performance.md")
        print("Performance report saved to performance.md")
        
        # Calculate and display key metrics
        metrics = reporter.calculate_performance(backtest_report)
        print("\n" + "="*50)
        print("KEY PERFORMANCE METRICS")
        print("="*50)
        print(f"Total Return: {metrics.total_return:.2%}")
        print(f"Annualized Return: {metrics.annualized_return:.2%}")
        print(f"Sharpe Ratio: {metrics.sharpe_ratio:.3f}")
        print(f"Maximum Drawdown: {metrics.max_drawdown:.2%}")
        print(f"Win Rate: {metrics.win_rate:.2%}")
        print(f"Total Trades: {metrics.total_trades}")
        print("="*50)
    
    return backtest_report

if __name__ == "__main__":
    import json
    report = run_backtest()
    print("\nDetailed backtest results:")
    print(json.dumps(report, indent=2))
