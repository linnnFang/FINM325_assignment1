"""
Data Ingestion & Immutable Types

Read market_data.csv (columns: timestamp, symbol, price) using the built-in csv module.

Define a frozen dataclass MarketDataPoint with attributes timestamp (datetime), symbol (str), and price (float).

Parse each row into a MarketDataPoint and collect them in a list.
"""

# here we convert csv into a list for each object
import pandas as pd
from dataclasses import dataclass
import datetime as datetime
import csv


from models import MarketDataPoint

'''
# read data
def loadfile(csv):
    #download
    df = pd.read_csv("market_data.csv")   

    # parse row
    marketList = []       
    for i in range(len(df)):
        marketList.append(MarketDataPoint(df.iloc[i][0],df.iloc[i][1],df.iloc[i][2]))

    return marketList
'''

class MarketDataReader:
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.data_list = []

    def read_data(self):
        try:
            with open(self.csvfile, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        market_data_point = MarketDataPoint(
                            timestamp=datetime.datetime.fromisoformat(row["timestamp"]),
                            symbol=row["symbol"],
                            price=float(row["price"])
                        )
                        self.data_list.append(market_data_point)

                    except Exception as error_in_row:
                        print(f"There is error in row {row}: {error_in_row}")

        except Exception as error_in_csv:
            print(f"There is error reading CSV file: {error_in_csv}")

    def fetch_data(self):
        return self.data_list

