import string

import pandas as pd
from stock_pandas import StockDataFrame
from ta.trend import SMAIndicator, EMAIndicator
from pandas_ta.statistics import stdev

class BollingerKeltnerSqueezeKDJ():
    def __init__(self,
                 df: StockDataFrame,
                 close: pd.Series,
                 bb_stdev: int = 2.0,
                 kel_range: int = 1.5,
                 length: int = 20
                 ):
        self.df = df
        self.length = length
        self.close = close
        self.bb_stdev = bb_stdev
        self.kel_range = kel_range

    def _run(self):
        self.df = self.standard_deviation_bollinger_bands()
        self.df = self.keltner_channels()
        self.df['bb_k_current_fill'] = ((self.df['bb_upper'] <= self.df['k_upper']) & (self.df['bb_lower'] >= self.df['k_lower']))
        self.df['bb_k_previous_fill'] = ((self.df['bb_upper'].shift(1) <= self.df['k_upper'].shift(1)) & (self.df['bb_lower'].shift(1) >= self.df['k_lower'].shift(1)) & self.df['bb_k_current_fill'] == True)

        self.df['upper'] = (self.df['bb_upper'] <= self.df['k_upper'])
        self.df['lower'] = (self.df['bb_lower'] >= self.df['k_lower'])
        df2 = self.df.where((self.df['upper']) & (self.df['lower']))
        self.df['bb_k_latest_fill'] = ((df2['upper'] == True) & (df2['lower'] == True))
        self.df = self.add_indicator_signal()

        return self.df

    def add_indicator_signal(self) -> StockDataFrame:
        self.df['has_crossed'] = False
        self.df['bb_k_buy'] = False
        self.df['bb_k_sell'] = False
        self.df['has_bb_k_latest_fill'] = False
        for current in range(1, len(self.df.index)):
            previous = current - 1

            # reset Flag to false
            if ((self.df['bb_k_current_fill'][current] == False) & (self.df['bb_k_previous_fill'][previous] == True)):
                self.df['has_crossed'][current] = False
            else:
                self.df['has_crossed'][current] = self.df['has_crossed'][previous]

            if (self.df['bb_k_buy'][previous] == True):
                self.df['bb_k_buy'][current] = False
            else:
                self.df['bb_k_buy'][current] = self.df['bb_k_buy'][previous]

            if (self.df['bb_k_sell'][previous] == True):
                self.df['bb_k_sell'][current] = False
            else:
                self.df['bb_k_sell'][current] = self.df['bb_k_sell'][previous]

            if (self.df['bb_k_latest_fill'][previous] == True):
                self.df['has_bb_k_latest_fill'][current] = True
            else:
                self.df['has_bb_k_latest_fill'][current] = self.df['has_bb_k_latest_fill'][previous]

            if ((self.df['kdj.j:25,3,3,50.0/20.0'][current] == True) & (self.df['bb_k_current_fill'][current] == False) & (self.df['has_bb_k_latest_fill'][previous] == True) & (self.df['has_crossed'][current] == False)):
                self.df['bb_k_buy'][current] = True
                self.df['has_bb_k_latest_fill'][current] = False
                self.df['has_crossed'][current] = True
            elif ((self.df['kdj.j:25,3,3,50.0\80.0'][current] == True) & (self.df['bb_k_current_fill'][current] == False) & (self.df['has_bb_k_latest_fill'][previous] == True) & (self.df['has_crossed'][current] == False)):
                self.df['bb_k_sell'][current] = True
                self.df['has_bb_k_latest_fill'][current] = False
                self.df['has_crossed'][current] = True


        return self.df
    def bb_kdj_indicator(self) -> StockDataFrame:
        self.df = self._run()
        return self.df

    def standard_deviation_bollinger_bands(self) -> StockDataFrame:
        self.df['bb_basis'] = SMAIndicator(close=self.close, window=self.length).sma_indicator()
        self.df['bb_dev'] = self.bb_stdev * stdev(close=self.close, length=self.length)
        self.df['bb_upper'] = (self.df['bb_basis'] + self.df['bb_dev'])
        self.df['bb_lower'] = (self.df['bb_basis'] - self.df['bb_dev'])
        return self.df

    def keltner_channels(self) -> StockDataFrame:
        self.df['k_ma'] = EMAIndicator(close=self.close, window=self.length).ema_indicator()
        self.df['k_range'] = self.tr()
        self.df['k_range_ma'] = EMAIndicator(close=self.df['k_range'], window=self.length).ema_indicator()
        self.df['k_upper'] = self.df['k_ma'] + self.df['k_range_ma'] * self.kel_range
        self.df['k_lower'] = self.df['k_ma'] - self.df['k_range_ma'] * self.kel_range

        return self.df

    def tr(self):
        self.df['previous_close'] = self.df['close'].shift(1)
        self.df['high-low'] = abs(self.df['high'] - self.df['low'])
        self.df['high-pc'] = abs(self.df['high'] - self.df['previous_close'])
        self.df['low-pc'] = abs(self.df['low'] - self.df['previous_close'])

        tr = self.df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

        return tr
