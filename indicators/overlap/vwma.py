from ta.utils import IndicatorMixin
import pandas as pd
from pandas_ta.overlap import vwma


class VWMAIndicator(IndicatorMixin):
    def __init__(self,
                 open: pd.Series,
                 high: pd.Series,
                 low: pd.Series,
                 close: pd.Series,
                 volume: pd.Series,
                 length,
                 fillna: bool = False):
        self.low = low
        self.high = high
        self.open = open
        self.length = length
        self.volume = volume
        self.close = close
        self._fillna = fillna
        self._run()

    def _run(self):
        vwma_open = vwma(close=self.open, volume=self.volume, length=self.length)
        vwma_high = vwma(close=self.high, volume=self.volume, length=self.length)
        vwma_low = vwma(close=self.low, volume=self.volume, length=self.length)
        vwma_close = vwma(close=self.close, volume=self.volume, length=self.length)

        self.vwma_open = vwma(close=vwma_open, volume=self.volume, length=self.length)
        self.vwma_high = vwma(close=vwma_high, volume=self.volume, length=self.length)
        self.vwma_low = vwma(close=vwma_low, volume=self.volume, length=self.length)
        self.vwma_close = vwma(close=vwma_close, volume=self.volume, length=self.length)

    def get_vwma_open(self) -> pd.Series:
        vwma_open = self._check_fillna(self.vwma_open, value=0)
        return pd.Series(vwma_open, name='vwma_open')

    def get_vwma_high(self) -> pd.Series:
        vwma_high = self._check_fillna(self.vwma_high, value=0)
        return pd.Series(vwma_high, name='vwma_high')

    def get_vwma_low(self) -> pd.Series:
        vwma_low = self._check_fillna(self.vwma_low, value=0)
        return pd.Series(vwma_low, name='vwma_low')

    def get_vwma_close(self) -> pd.Series:
        vwma_close = self._check_fillna(self.vwma_close, value=0)
        return pd.Series(vwma_close, name='vwma_low')
