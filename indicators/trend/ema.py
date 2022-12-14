import pandas as pd
from ta.trend import EMAIndicator
from ta.utils import IndicatorMixin


class SimonEMAIndicator(IndicatorMixin):
    def __init__(self,
                 close: pd.Series,
                 fillna: bool = False):
        self.close = close
        self.fillna = fillna
        self._run()

    def _run(self):
        self.ema_60 = EMAIndicator(close=self.close, window=60).ema_indicator()
        self.ema_144 = EMAIndicator(close=self.close, window=144).ema_indicator()
        self.ema_200 = EMAIndicator(close=self.close, window=200).ema_indicator()

    def get_ema_60(self) -> pd.Series:
        ha_open = self._check_fillna(self.ema_60, value=0)
        return pd.Series(ha_open, name='ema_60')

    def get_ema_144(self) -> pd.Series:
        ha_open = self._check_fillna(self.ema_144, value=0)
        return pd.Series(ha_open, name='ema_144')

    def get_ema_200(self) -> pd.Series:
        ha_open = self._check_fillna(self.ema_200, value=0)
        return pd.Series(ha_open, name='ema_200')

    def get_ema_with_period(self, window):
        ema_ = EMAIndicator(close=self.close, window=window).ema_indicator()
        return pd.Series(ema_, name=f"ema_{window}")
