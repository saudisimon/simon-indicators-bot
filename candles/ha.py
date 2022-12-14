import numpy as np
import pandas as pd
from ta.trend import EMAIndicator

from ta.utils import IndicatorMixin

class HeikinAshiCandlestick(IndicatorMixin):
    """HeikinAshiCandlestick

    https://www.investopedia.com/trading/heikin-ashi-better-candlestick/

    Args:
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.
    """

    def __init__(self,
                 open: pd.Series,
                 high: pd.Series,
                 low: pd.Series,
                 close: pd.Series,
                 fillna: bool = False):
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._fillna = fillna
        self._run()

    def _run(self):
        self._ha_close = (self._open + self._high + self._low + self._close) / 4
        self._ha_open = pd.DataFrame(np.nan, index=self._open.index, columns=['Open'])
        self._ha_open.iloc[0] = self._open.iloc[0]
        for i in range(1, len(self._open)):
            self._ha_open.iloc[i] = (self._ha_open.iloc[i - 1] + self._ha_close.iloc[i - 1]) / 2
        self._ha_open = self._ha_open['Open']
        self._ha_high = pd.concat([self._ha_open, self._ha_close, self._high], axis=1).max(axis=1)
        self._ha_low = pd.concat([self._ha_open, self._ha_close, self._low], axis=1).min(axis=1)

    def heikin_ashi_candlestick_open(self) -> pd.Series:
        """Heikin-Ashi Candlestick Open

        Returns:
            pandas.Series: New feature generated.
        """
        ha_open = self._check_fillna(self._ha_open, value=0)
        return pd.Series(ha_open, name='heikin_ashi_candlestick_open')

    def heikin_ashi_candlestick_high(self) -> pd.Series:
        """Heikin-Ashi Candlestick High

        Returns:
            pandas.Series: New feature generated.
        """
        ha_high = self._check_fillna(self._ha_high, value=0)
        return pd.Series(ha_high, name='heikin_ashi_candlestick_high')

    def heikin_ashi_candlestick_low(self) -> pd.Series:
        """Heikin-Ashi Candlestick Low

        Returns:
            pandas.Series: New feature generated.
        """
        ha_low = self._check_fillna(self._ha_low, value=0)
        return pd.Series(ha_low, name='heikin_ashi_candlestick_low')

    def heikin_ashi_candlestick_close(self) -> pd.Series:
        """Heikin-Ashi Candlestick Close

        Returns:
            pandas.Series: New feature generated.
        """
        ha_close = self._check_fillna(self._ha_close, value=0)
        return pd.Series(ha_close, name='heikin_ashi_candlestick_close')



def heikin_ashi_candlestick_open(open, high, low, close, fillna=False):
    """Heikin-Ashi Candlestick Open

    Args:
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    return HeikinAshiCandlestick(open=open,
                                 high=high,
                                 low=low,
                                 close=close,
                                 fillna=fillna).heikin_ashi_candlestick_open()


def heikin_ashi_candlestick_high(open, high, low, close, fillna=False):
    """Heikin-Ashi Candlestick High

    Args:
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    return HeikinAshiCandlestick(open=open,
                                 high=high,
                                 low=low,
                                 close=close,
                                 fillna=fillna).heikin_ashi_candlestick_high()


def heikin_ashi_candlestick_low(open, high, low, close, fillna=False):
    """Heikin-Ashi Candlestick Low

    Args:
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    return HeikinAshiCandlestick(open=open,
                                 high=high,
                                 low=low,
                                 close=close,
                                 fillna=fillna).heikin_ashi_candlestick_low()


def heikin_ashi_candlestick_close(open, high, low, close, fillna=False):
    """Heikin-Ashi Candlestick Close

    Args:
        open(pandas.Series): dataset 'Open' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    return HeikinAshiCandlestick(open=open,
                                 high=high,
                                 low=low,
                                 close=close,
                                 fillna=fillna).heikin_ashi_candlestick_close()

def heikin_ashi_smoothed_candles(df):
    local_df = df

    local_df['heikin_ashi_open'] = EMAIndicator(local_df['ha_open'], window=3).ema_indicator()
    local_df['heikin_ashi_high'] = EMAIndicator(local_df['ha_high'], window=3).ema_indicator()
    local_df['heikin_ashi_low'] = EMAIndicator(local_df['ha_low'], window=3).ema_indicator()
    local_df['heikin_ashi_close'] = EMAIndicator(local_df['ha_close'], window=3).ema_indicator()

    df['heikin_ashi_open'] = EMAIndicator(local_df['heikin_ashi_open'], window=10).ema_indicator()
    df['heikin_ashi_high'] = EMAIndicator(local_df['heikin_ashi_high'], window=10).ema_indicator()
    df['heikin_ashi_low'] = EMAIndicator(local_df['heikin_ashi_low'], window=10).ema_indicator()
    df['heikin_ashi_close'] = EMAIndicator(local_df['heikin_ashi_close'], window=10).ema_indicator()
    df['heikin_ashi_in_uptrend'] = (local_df['heikin_ashi_open'] < local_df['heikin_ashi_close'])
    return df