# FINM325_assignment1
for assignment

Learning Objectives
- Parse CSV data into immutable dataclass instances.

- Distinguish and use mutable classes for order management.

- Build an abstract Strategy interface with concrete subclasses.

- Manage time-series data and portfolio state using lists and dictionaries.

- Define custom exceptions and handle errors without stopping the backtest.

- Generate a Markdown report summarizing key performance metrics.

# Task Specifications

1. Data Ingestion & Immutable Types

- Read market_data.csv (columns: timestamp, symbol, price) using the built-in csv module.

- Define a frozen dataclass MarketDataPoint with attributes timestamp (datetime), symbol (str), and price (float).

- Parse each row into a MarketDataPoint and collect them in a list.1

2. Mutable Order Management
- Implement an Order class with mutable attributes: symbol, quantity, price, and status.

