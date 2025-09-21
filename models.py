''''
models.py (dataclasses, Order, exceptions)

----------------------------------------------------------------------------
Mutable Order Management
Implement an Order class with mutable attributes: symbol, quantity, price, and status.
Demonstrate in a unit test that you can update Order.status but not MarketDataPoint.price.

class OrderError(Exception)
class MarketDataPoint
class Order
class TestOrderAndMarketData(unittest.TestCase)
class MarketDataContainer:

----------------------------------------------------------------------------
Exception Handling

Define custom exceptions:

class OrderError(Exception): pass
class ExecutionError(Exception): pass
Raise OrderError for invalid orders (e.g., zero or negative quantity).
In the execution engine, simulate occasional failures and raise ExecutionError; catch and log these errors to continue processing.
'''

import unittest
from dataclasses import FrozenInstanceError
from dataclasses import dataclass
import datetime as datetime
# Exception Handling
class OrderError(Exception): 
    def __init__(self,error):
        super().__init__("This order is not valid")
class ExecutionError(Exception): pass


# define frozen data class
#immutable
@dataclass(frozen = True)
class MarketDataPoint:
    timestamp : datetime.datetime
    symbol : str
    price: float


#mutable
class Order:
    def __init__(self,symbol:str,quantity:int ,price:float,side:str,status:str):
        self.symbol = symbol
        self.quantity = quantity # validate via setter
        self.price = price # validate via setter
        self.side = side
        self.status = status

    @property
    def price(self):
        return self.price
    
    @price.setter
    def price(self,value):
        if value < 0:
            raise OrderError("Price cannot be negative")
        self.price = value

    @property
    def quantity(self):
        return self.quantity
    @quantity.setter
    def quantity(self, v: int):
        if v <= 0:
            raise OrderError("quantity must be > 0")
        self._quantity = int(v)

    @property
    def value(self):
        return self.price* self.quantity
    
    def __str__(self):
        return f"{self.quantity} shares of {self.symbol} at ${self.price:.2f}"
    
    def __repr__(self):
        return f"Order('{self.symbol}',{self.quantity},{self.price})"



# unit test
'''
(maybe deleted later)
'''
class TestOrderAndMarketData(unittest.TestCase):
    def test_mutable_order(self):
        order = Order("AAPL", 10, 150.0,"bid","NEW")
        self.assertEqual(order.status, "NEW")
        order.status = "FILLED"
        self.assertEqual(order.status, "FILLED")

    def test_immutable_marketdatapoint(self):
        point = MarketDataPoint(datetime.datetime.now(), "AAPL", 150.0)
        with self.assertRaises(FrozenInstanceError):
            point.price = 200.0

class MarketDataContainer:
    def __init__(self):
        self.buffer = []
        self.all_positions = {}
        self.trade_signal = []

    def buffer_data(self, data_point):
        self.buffer.append(data_point)

    def add_trade_signal(self, action, symbol, quantity, price):
        self.trade_signal.append((action, symbol, quantity, price))

    def calculate_average_price(self, position):
        if position["total_shares"] > 0:
            position["average_price"] = position["total_cost"] / position["total_shares"]
        else:
            position["average_price"] = 0.0

    def update_position(self, order):
        symbol = order['symbol']
        side = str(order['side']).upper()
        quantity = int(order['quantity'])
        price = float(order['price'])

        if symbol not in self.all_positions:
            self.all_positions[symbol] = {
                "total_shares": 0,
                "total_cost": 0.0,
                "average_price": 0.0
            }
        position = self.all_positions[symbol]

        if side == "BUY":
            position["total_shares"] += quantity
            position["total_cost"] += price * quantity
            self.calculate_average_price(position)

        elif side == "SELL":
            sell_quantity = min(quantity, position["total_shares"])
            if quantity > position["total_shares"]:
                print(f"CANNOT OVERSELL! Currently have shares: {position['total_shares']}. But wanted to sell {quantity}. PROCEED with selling {sell_quantity} shares.")

            position["total_shares"] -= sell_quantity
            position["total_cost"] -= position["average_price"] * sell_quantity
            if position["total_shares"] <= 0:
                position["total_cost"] = 0.0
                position["average_price"] = 0.0
            self.calculate_average_price(position)

    def fetch_current_position(self, symbol):
        return self.all_positions.get(symbol, {
            "total_shares": 0,
            "total_cost": 0.0,
            "average_price": 0.0
        })