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
        self.quantity = quantity
        self.price = price
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
    

    @property
    def value(self):
        return self.price* self.quantity
    

# unit test

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

