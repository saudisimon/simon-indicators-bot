import string

from stock_pandas import StockDataFrame


class SimonKDJIndicator():
    def __init__(self,
                 df: StockDataFrame,
                 k: string = "25",
                 d: string = "3",
                 j: string = "3"):
        self.df = df
        self.j = j
        self.d = d
        self.k = k

    def kdj_indicator(self) -> StockDataFrame:
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}", create_column=True)
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}", create_column=True)
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}/20.0", create_column=True)
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}\80.0", create_column=True)
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}>=80.0", create_column=True)
        self.df.exec(f"kdj.j:{self.k},{self.d},{self.j}<=20.0", create_column=True)
        return self.df
