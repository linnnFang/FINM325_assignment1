
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ---------------- Exceptions ----------------
class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass

# ---------------- Core types ----------------
@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

@dataclass
class Order:
    side: str                  # "BUY" | "SELL"
    symbol: str
    quantity: int
    price: float
    timestamp: datetime
    status: str = "NEW"        # "NEW" -> "FILLED"/"REJECTED"

    def validate(self) -> None:
        s = self.side.upper()
        if s not in {"BUY","SELL"}:
            raise OrderError(f"Invalid side: {self.side}")
        if self.quantity <= 0:
            raise OrderError("Quantity must be > 0")
        if self.price <= 0:
            raise OrderError("Price must be > 0")
        if not self.symbol:
            raise OrderError("Symbol is required")
        self.side = s

# ---------------- Containers for Data & Signals ----------------
class MarketDataContainer:
    """
    - Buffer incoming MarketDataPoint instances in a list (self.buffer)
    - Store open positions as {'SYM': {'quantity': int, 'avg_price': float}}
    - Collect signals as a list of tuples (action, symbol, qty, price)
    """
    def __init__(self) -> None:
        self.buffer: List[MarketDataPoint] = []
        self.positions: Dict[str, Dict[str, float]] = {}
        self.signals: List[Tuple[str, str, int, float]] = []

    def buffer_data(self, data_point: MarketDataPoint) -> None:
        self.buffer.append(data_point)

    def last(self) -> Optional[MarketDataPoint]:
        return self.buffer[-1] if self.buffer else None

    def recent(self, n: int):
        return self.buffer[-n:] if n > 0 else []

    def __len__(self) -> int:
        return len(self.buffer)

    def __iter__(self):
        return iter(self.buffer)

    # position
    def _ensure_pos(self, symbol: str) -> Dict[str, float]:
        if symbol not in self.positions:
            self.positions[symbol] = {"quantity": 0, "avg_price": 0.0}
        return self.positions[symbol]

    def apply_fill(self, order: Order) -> None:
        pos = self._ensure_pos(order.symbol)
        q = int(order.quantity)
        px = float(order.price)

        if order.side == "BUY":
            old_q = pos["quantity"]
            new_q = old_q + q
            pos["avg_price"] = (pos["avg_price"] * old_q + px * q) / new_q if new_q > 0 else 0.0
            pos["quantity"] = new_q
        elif order.side == "SELL":
            sell_q = min(q, pos["quantity"])
            pos["quantity"] -= sell_q
            if pos["quantity"] == 0:
                pos["avg_price"] = 0.0

    # signal
    def add_signal(self, action: str, symbol: str, qty: int, price: float) -> None:
        self.signals.append((action, symbol, qty, price))

    def clear_signals(self) -> None:
        self.signals.clear()
