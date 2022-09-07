import string

import pandas as pd
from stock_pandas import StockDataFrame
from ta.trend import SMAIndicator


class SimonCCIIndicator():
    def __init__(self,
                 df: StockDataFrame,
                 window):
        self.df = df
        self.window = window

    def cci_indicator(self) -> StockDataFrame:
        self.df['cci_' + str(self.window)] = self.calculate_cci(window=self.window)
        return self.df

    def calculate_cci(self, window):
        local_df = self.df
        local_df['TP'] = ((local_df['high'] + local_df['low'] + local_df['close']) / 3)
        local_df['sma'] = SMAIndicator(close=local_df['TP'], window=18).sma_indicator()
        local_df['mad'] = local_df['TP'].rolling(window).apply(lambda x: pd.Series(x).mad())
        self.df['cci_' + str(window)] = (local_df['TP'] - local_df['sma']) / (0.015 * local_df['mad'])
        return pd.Series(self.df['cci_' + str(window)], name=f"cci_{window}")
