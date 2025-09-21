
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List
import csv

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class MarketDataReader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._data: List[MarketDataPoint] = []

    def read_data(self) -> None:
        with open(self.csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = datetime.fromisoformat(row["timestamp"])  # e.g., 2025-09-20T14:30:22.051736
                sym = row["symbol"].strip()
                px = float(row["price"])
                self._data.append(MarketDataPoint(ts, sym, px))
        self._data.sort(key=lambda d: d.timestamp)

    def fetch_data(self) -> List[MarketDataPoint]:
        return list(self._data)
