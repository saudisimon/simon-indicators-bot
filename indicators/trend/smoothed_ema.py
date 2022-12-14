import pandas as pd
from pandas_ta.overlap import ema
from ta.utils import IndicatorMixin


class SmoothedEMAIndicator(IndicatorMixin):
    def __init__(self,
                 open: pd.Series,
                 high: pd.Series,
                 low: pd.Series,
                 close: pd.Series,
                 volume: pd.Series,
                 period,
                 smooth,
                 fillna: bool = False):
        self.low = low
        self.high = high
        self.open = open
        self.period = period
        self.smooth = smooth
        self.volume = volume
        self.close = close
        self._fillna = fillna
        self._run()

    def _run(self):
        sema_open = ema(close=self.open, volume=self.volume, length=self.period)
        sema_high = ema(close=self.high, volume=self.volume, length=self.period)
        sema_low = ema(close=self.low, volume=self.volume, length=self.period)
        sema_close = ema(close=self.close, volume=self.volume, length=self.period)

        self.sema_open = ema(close=sema_open, volume=self.volume, length=self.smooth)
        self.sema_high = ema(close=sema_high, volume=self.volume, length=self.smooth)
        self.sema_low = ema(close=sema_low, volume=self.volume, length=self.smooth)
        self.sema_close = ema(close=sema_close, volume=self.volume, length=self.smooth)

    def get_sema_open(self) -> pd.Series:
        sema_open = self._check_fillna(self.sema_open, value=0)
        return pd.Series(sema_open, name='sema_open')

    def get_sema_high(self) -> pd.Series:
        sema_high = self._check_fillna(self.sema_high, value=0)
        return pd.Series(sema_high, name='sema_high')

    def get_sema_low(self) -> pd.Series:
        sema_low = self._check_fillna(self.sema_low, value=0)
        return pd.Series(sema_low, name='sema_low')

    def get_sema_close(self) -> pd.Series:
        sema_close = self._check_fillna(self.sema_close, value=0)
        return pd.Series(sema_close, name='sema_low')
