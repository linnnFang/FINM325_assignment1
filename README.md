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
1. data_generator.py: \n
This is the file used to generate the simulated stock data. We downloaded this code from Canvas page and run to generate `market_data.csv'.

2. data_loader.py: \n
Reads the simulated `market_data.csv` which includes `timestamp`, `symbol`, `price` using Python's built in `CSV` module and translate each row of raw data into defined `MarketDataPoint` dataclass.

3. execution_engine.py: \n
(Run backtest loop? like feed `MarketDataClass` to strategy? Update Position? Container?)

4. models.py: \n


6. strategies.py: \n
This python file defines two main strategies: moving average crossover and momentum trading. The strategy will generate trading signals from `MarketDataPoint`.

7. main.py: \n
This file connected the modules we have in the repo, including data loading, strategy execution, and the final reporting process.

8. reporting.py: \n
Computes required performance metrics required, including:
- Total return
- Series of periodic returns
- Sharpe ratio
- Maximum drawdown

8. performance.ipynb: \n
We also used a Jupyter Notebook to demonstrate the usage of this simple CSV-Based Algorithgmic trading backtester. It includes our test results, metrics, plots, etc.



