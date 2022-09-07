
from binance.client import Client
from .config import BINANCE_API_KEY, BINANCE_SECRET_KEY
from stock_pandas import StockDataFrame
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
import warnings

warnings.filterwarnings('ignore')


class BinanceClient:
    def __init__(self):
        self.limit = None
        self.interval = None
        self.symbol = None
        self._run()

    def _run(self):
        # Verify binance API Key to access data
        self.binance_client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

    def get_all_tickers(self):
        symbols = [x['symbol'] for x in Client.get_all_tickers(self=self.binance_client)]
        return symbols

    def fetch_historical_klines(self, symbol, interval, limit) -> pd:
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        df = StockDataFrame(
            self.binance_client.futures_historical_klines(symbol=self.symbol, interval=self.interval,
                                                          start_str='2022-04-01',
                                                          limit=self.limit))
        df = df.iloc[:, :6]
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize("UTC").dt.tz_convert('Asia/Bangkok')

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col])
        return df
