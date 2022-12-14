import string

import pandas as pd
from ta.utils import IndicatorMixin
from ta.volatility import AverageTrueRange


class SupertrendIndicator(IndicatorMixin):
    def __init__(self,
                 df: pd,
                 period: int = 10,
                 atr_multiplier: int = 2.5,
                 window: string = "hl2"):
        self.window = window
        self.atr_multiplier = atr_multiplier
        self.period = period
        self.df = df

    def supertrend(self):
        self.df['atr'] = AverageTrueRange(high=self.df['high'], low=self.df['low'], close=self.df['close'],
                                          window=self.period).average_true_range()
        self.df['upper_band'] = self.df[self.window] + (self.atr_multiplier * self.df['atr'])
        self.df['lower_band'] = self.df[self.window] - (self.atr_multiplier * self.df['atr'])
        self.df['in_uptrend'] = True
        for current in range(1, len(self.df.index)):
            previous = current - 1

            if self.df['close'][current] > self.df['upper_band'][previous]:
                self.df['in_uptrend'][current] = True
            elif self.df['close'][current] < self.df['lower_band'][previous]:
                self.df['in_uptrend'][current] = False
            else:
                self.df['in_uptrend'][current] = self.df['in_uptrend'][previous]

                if self.df['in_uptrend'][current] and self.df['lower_band'][current] < self.df['lower_band'][previous]:
                    self.df['lower_band'][current] = self.df['lower_band'][previous]

                if not self.df['in_uptrend'][current] and self.df['upper_band'][current] > self.df['upper_band'][
                    previous]:
                    self.df['upper_band'][current] = self.df['upper_band'][previous]
        return self.df
