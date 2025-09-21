# FINM325 Assignment 1: CSV-Based Algorithmic Trading Backtester

## Authors: Simon Guo, Lin Fang, Roxxane Wang, Victor Ji

## Project Overview
In this group project, we built a simple CSV-Based Algorithmic trading backtester, with simulated stock data generated for Apple (ticker symbol: AAPL). We processed the simulated stock price, and applied two popular trading strategies, including the moving average crossover and momentum trading to simulate the investment returns. Last, we analyzed the performance of these two trading strategies.

## Setup Instructions:
1. Create and activate the environment for this backtester:
```bash
conda create -n finm python=3.13.5
conda activate finm
```

2. Install package dependencies:
```bash
conda install numpy pandas matplotlib ipykernal
```

3. Cloning:
```bash
git clone https://github.com/linnnFang/FINM325_assignment1
cd FINM325_assignment1
```

## Module Descriptions:
1. data_generator.py:
This is the file used to generate the simulated stock data. We downloaded this code from Canvas page and run to generate `market_data.csv'.


3. data_loader.py:
Reads the simulated `market_data.csv` which includes `timestamp`, `symbol`, `price` using Python's built in `CSV` module and translate those information into defined `MarketDataPoint` dataclass. It outputs a list of `MarketDataPoint` that is sorted and ordered by time.

3. execution_engine.py:




