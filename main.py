
from data_loader import MarketDataReader
from strategies import MovingAverageCrossover, Momentum
from execution_engine import BackTestengine

def run_backtest(csv_path: str = "market_data.csv"):
    reader = MarketDataReader(csv_path)
    reader.read_data()
    data = reader.fetch_data()


    symbols = sorted({t.symbol for t in data})
    strategies = []
    for sym in symbols:
        strategies.append(MovingAverageCrossover(symbol=sym, short_window=3, long_window=8, trade_qty=2))
        strategies.append(Momentum(symbol=sym, lookback=5, threshold_pct=0.01, trade_qty=1))

    engine = BackTestengine(strategies)
    engine.run(data)
    return engine.report()

if __name__ == "__main__":
    import json
    report = run_backtest()
    print(json.dumps(report, indent=2))
