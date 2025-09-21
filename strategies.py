from collections import deque
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick):
        pass

class MovingAverageCrossover(Strategy):
    def __init__(self, short_window=5, long_window=20, trade_qty=1):
        self._short_w = short_window
        self._long_w = long_window
        self._prices = deque(maxlen=long_window) #这个的意思就是只能有long_window个元素 如果再往里追加新元素 最旧的元素会自动被丢掉
        self._prev_diff = None
        self._qty = trade_qty

    def _mean(self, seq):
        return sum(seq) / float(len(seq))

    def generate_signals(self, tick, positions=None):
        self._prices.append(tick.price)
        signals = []

        if len(self._prices) < self._long_w:
            return signals

        short_ma = self._mean(list(self._prices)[-self._short_w:])
        long_ma = self._mean(self._prices)
        diff = short_ma - long_ma

        if self._prev_diff is not None:
            if self._prev_diff <= 0 and diff > 0:
                signals.append(("BUY", tick.symbol, self._qty, tick.price))

            # SELL 时检查仓位是否足够
            elif self._prev_diff >= 0 and diff < 0:
                current_shares = 0
                if positions and tick.symbol in positions:
                    current_shares = positions[tick.symbol]["total_shares"]
                if current_shares >= self._qty:
                    signals.append(("SELL", tick.symbol, self._qty, tick.price))
                else:
                    print(f"Skip SELL: only {current_shares} shares in {tick.symbol}, need {self._qty}")
        self._prev_diff = diff
        return signals



class Momentum(Strategy):
    def __init__(self, lookback=10, threshold_pct=0.002, trade_qty=1):
        if lookback < 1:
            raise ValueError("lookback must be >= 1")
        if threshold_pct < 0:
            raise ValueError("threshold_pct must be >= 0")
        self._window = lookback
        self._th = threshold_pct
        self._prices = deque(maxlen=lookback+1)
        self._qty = trade_qty

    def generate_signals(self, tick, positions=None):
        self._prices.append(tick.price)
        signals = []

        if len(self._prices) < self._prices.maxlen:
            return signals

        past = self._prices[0]
        now = self._prices[-1]
        if past <= 0:
            return signals
        change = (now - past) / past

        if change >= self._th:
            signals.append(("BUY", tick.symbol, self._qty, tick.price))
        elif change <= -self._th:
            current_shares = 0
            if positions and tick.symbol in positions:
                current_shares = positions[tick.symbol]["total_shares"]
            if current_shares >= self._qty:
                signals.append(("SELL", tick.symbol, self._qty, tick.price))
            else:
                print(f"Skip SELL: only {current_shares} shares in {tick.symbol}, need {self._qty}")
        return signals