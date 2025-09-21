# FINM325 Assignment 1: CSV-Based Algorithmic Trading Backtester
## Authors: Simon Guo, Lin Fang, Roxxane Wang, Victor Ji

## Setup Instructions:
1. Create and activate the environment for this backtester:
```bash
conda create -n finm python=3.13.5
conda activate finm
```

2. Install package dependencies
```bash
conda install numpy pandas matplotlib ipykernal
```



# Task Specifications

1. Data Ingestion & Immutable Types

- Read market_data.csv (columns: timestamp, symbol, price) using the built-in csv module.

- Define a frozen dataclass MarketDataPoint with attributes timestamp (datetime), symbol (str), and price (float).

- Parse each row into a MarketDataPoint and collect them in a list.1

2. Mutable Order Management
- Implement an Order class with mutable attributes: symbol, quantity, price, and status.

