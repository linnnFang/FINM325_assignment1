
from __future__ import annotations
from collections import deque
from typing import Deque, Dict, List, Tuple, Optional

# Public signal shape: (action, symbol, qty, price)
Signal = Tuple[str, str, int, float]

class Strategy:
    def generate_signals(self, tick, positions=None) -> List[Signal]:
        raise NotImplementedError

class MovingAverageCrossover(Strategy):
    def __init__(self, symbol: str, short_window: int = 5, long_window: int = 20, trade_qty: int = 1) -> None:
        if not (1 <= short_window < long_window):
            raise ValueError("Require 1 <= short_window < long_window")
        self.symbol = symbol
        self._short_w = short_window
        self._long_w = long_window
        self._prices: Deque[float] = deque(maxlen=long_window)
        self._prev_diff: Optional[float] = None
        self._qty = trade_qty

    @staticmethod
    def _mean(seq) -> float:
        return sum(seq) / float(len(seq))

    def generate_signals(self, tick, positions=None) -> List[Signal]:
        if tick.symbol != self.symbol:
            return []
        price = float(tick.price)
        self._prices.append(price)
        if len(self._prices) < self._long_w:
            return []

        short_ma = self._mean(list(self._prices)[-self._short_w:])
        long_ma  = self._mean(self._prices)
        diff = short_ma - long_ma

        out: List[Signal] = []
        if self._prev_diff is not None:
            # cross up -> BUY
            if self._prev_diff <= 0 and diff > 0:
                out.append(("BUY", tick.symbol, self._qty, price))
            # cross down -> SELL (position-aware)
            elif self._prev_diff >= 0 and diff < 0:
                qty = int(positions.get(tick.symbol, {}).get("quantity", 0)) if positions else 0
                sell_qty = min(self._qty, qty)
                if sell_qty > 0:
                    out.append(("SELL", tick.symbol, sell_qty, price))
        self._prev_diff = diff
        return out

class Momentum(Strategy):
    def __init__(self, symbol: str, lookback: int = 10, threshold_pct: float = 0.01, trade_qty: int = 1) -> None:
        if lookback < 1:
            raise ValueError("lookback must be >= 1")
        if threshold_pct < 0:
            raise ValueError("threshold_pct must be >= 0")
        self.symbol = symbol
        self._window = lookback
        self._th = threshold_pct
        self._prices: Deque[float] = deque(maxlen=lookback+1)  # need past & now
        self._qty = trade_qty

    def generate_signals(self, tick, positions=None) -> List[Signal]:
        if tick.symbol != self.symbol:
            return []
        self._prices.append(float(tick.price))
        if len(self._prices) < self._prices.maxlen:
            return []

        past = self._prices[0]
        now  = self._prices[-1]
        if past <= 0:
            return []

        change = (now - past) / past
        out: List[Signal] = []
        if change >= self._th:
            out.append(("BUY", tick.symbol, self._qty, now))
        elif change <= -self._th:
            qty = int(positions.get(tick.symbol, {}).get("quantity", 0)) if positions else 0
            sell_qty = min(self._qty, qty)
            if sell_qty > 0:
                out.append(("SELL", tick.symbol, sell_qty, now))
        return out
