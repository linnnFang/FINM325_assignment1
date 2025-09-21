
from __future__ import annotations
from typing import Iterable, List, Dict, Tuple
import random

from models import Order, OrderError, ExecutionError, MarketDataContainer, MarketDataPoint
from strategies import Strategy

class BackTestengine:
    """Ticks -> signals -> orders -> fills -> positions, with resilient logging."""
    def __init__(self, strategies: Iterable[Strategy]) -> None:
        self.strategies: List[Strategy] = list(strategies)
        self.container = MarketDataContainer()  # holds buffer, positions, signals
        self.order_log: List[Order] = []
        self.error_log: List[str] = []

    # ---- lifecycle ----
    def on_tick(self, tick: MarketDataPoint) -> None:
        self.container.buffer_data(tick)
        positions = self.container.positions  # schema: quantity + avg_price

        for strat in self.strategies:
            try:
                signals = strat.generate_signals(tick, positions) or []
                if not signals:
                    continue

                orders = self._create_orders(signals, tick)
                for order in orders:
                    try:
                        self._execute(order)
                    except Exception as ex:
                        order.status = "REJECTED"
                        self.error_log.append(f"{tick.timestamp} {order.symbol} {order.side} x{order.quantity}: EXECUTION ERROR: {ex}")
                    finally:
                        self.order_log.append(order)
            except Exception as ex:
                self.error_log.append(f"{tick.timestamp} Strategy {type(strat).__name__} error: {ex}")

    def run(self, market: Iterable[MarketDataPoint]) -> None:
        for tick in sorted(market, key=lambda t: t.timestamp):
            self.on_tick(tick)

    def report(self) -> Dict:
        return {
            "positions": {k: v.copy() for k, v in self.container.positions.items()},
            "orders": [{
                "time": o.timestamp.isoformat(),
                "symbol": o.symbol,
                "side": o.side,
                "qty": o.quantity,
                "price": o.price,
                "status": o.status
            } for o in self.order_log],
            "errors": list(self.error_log),
        }

    # ---- helpers ----
    def _create_orders(self, signals: List[Tuple], tick: MarketDataPoint) -> List[Order]:
        orders: List[Order] = []
        for s in signals:
            if len(s) == 3:
                side, symbol, qty = s
                price = float(tick.price)
            elif len(s) == 4:
                side, symbol, qty, price = s
            else:
                raise OrderError(f"Bad signal shape: {s}")
            o = Order(side=str(side).upper(), symbol=symbol, quantity=int(qty), price=float(price), timestamp=tick.timestamp)
            o.validate()
            orders.append(o)
        return orders

    def _execute(self, order: Order) -> None:
        # Simulate flaky fills 3% of the time
        if random.random() < 0.03:
            raise ExecutionError("Simulated venue outage")
        # Fill at provided price
        order.status = "FILLED"
        # apply to positions (quantity + avg_price schema)
        self.container.apply_fill(order)
