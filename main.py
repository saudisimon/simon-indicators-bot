import datetime

import schedule

from services.binance.client import BinanceClient
from indicators.trend.ema import SimonEMAIndicator
from indicators.momentum.kdj import SimonKDJIndicator
from indicators.momentum.cci import SimonCCIIndicator
from candles.ha import HeikinAshiCandlestick, heikin_ashi_smoothed_candles
from indicators.overlap.vwma import VWMAIndicator
from indicators.overlap.supertrend import SupertrendIndicator
from send_message import send_cci_kdj_message, send_super_trend_message, send_heiken_ashi_message, send_supertrend_pull_back_message

def add_indicators(df):
    df['ha_open'] = HeikinAshiCandlestick(open=df['open'], high=df['high'], low=df['low'],
                                          close=df['close']).heikin_ashi_candlestick_open()
    df['ha_high'] = HeikinAshiCandlestick(open=df['open'], high=df['high'], low=df['low'],
                                          close=df['close']).heikin_ashi_candlestick_high()
    df['ha_low'] = HeikinAshiCandlestick(open=df['open'], high=df['high'], low=df['low'],
                                         close=df['close']).heikin_ashi_candlestick_low()
    df['ha_close'] = HeikinAshiCandlestick(open=df['open'], high=df['high'], low=df['low'],
                                           close=df['close']).heikin_ashi_candlestick_close()
    df = heikin_ashi_smoothed_candles(df)
    simon_ema = SimonEMAIndicator(close=df['close'])
    df['ema_60'] = simon_ema.get_ema_60()
    df['ema_144'] = simon_ema.get_ema_144()
    df['ema_200'] = simon_ema.get_ema_200()
    df = SimonKDJIndicator(df=df).kdj_indicator()
    df = SimonCCIIndicator(df=df, window=18).cci_indicator()
    df = SimonCCIIndicator(df=df, window=54).cci_indicator()
    vwma_indicator = VWMAIndicator(open=df['ha_open'], high=df['ha_high'], low=df['ha_low'], close=df['ha_close'], volume=df['volume'], length=7)
    df['vwma_open'] = vwma_indicator.get_vwma_open()
    df['vwma_high'] = vwma_indicator.get_vwma_high()
    df['vwma_low'] = vwma_indicator.get_vwma_low()
    df['vwma_close'] = vwma_indicator.get_vwma_close()
    df['vwma_in_uptrend'] = (df['vwma_open'] < df['vwma_close'])
    df['ha_vwma_in_uptrend'] = (
            (
                    (df['heikin_ashi_in_uptrend'].shift(1) == False) & df['heikin_ashi_in_uptrend'] & df[
                'vwma_in_uptrend']
            ) | (
                    (df['vwma_in_uptrend'].shift(1) == False) & df['vwma_in_uptrend'] & df['heikin_ashi_in_uptrend']
            )
    )
    df['ha_vwma_in_downtrend'] = (
            (
                    (df['heikin_ashi_in_uptrend'] == False) & (df['heikin_ashi_in_uptrend'].shift(1)) & (
                        df['vwma_in_uptrend'] == False)
            ) | (
                    (df['vwma_in_uptrend'] == False) & (df['vwma_in_uptrend'].shift(1)) & (
                        df['heikin_ashi_in_uptrend'] == False)
            )
    )
    return df

def add_indicators_signal_flag(df):
    # CCI Signal
    short_df_min = df.rolling(window=20).min().shift(1)
    short_df_max = df.rolling(window=20).max().shift(1)
    df['cci_cross_up'] = (
                (df['cci_18'] > -100.0) & (short_df_min['cci_18'] < -200.0) & (short_df_max['cci_18'] < 200.0) & (
                    df['cci_18'] >= df['cci_54']) & (df['cci_18'].shift(1) <= df['cci_54'].shift(1)))
    df['cci_cross_down'] = (
                (df['cci_18'] < 100.0) & (short_df_max['cci_18'] > 200.0) & (short_df_min['cci_18'] < -200.0) & (
                    df['cci_18'] <= df['cci_54']) & (df['cci_18'].shift(1) >= df['cci_54'].shift(1)))

    # KDJ and CCI Signal
    df['cci_kdj_buy_cond'] = (df['cci_cross_up']) \
                             & (df['kdj.j:25,3,3/20.0'] | df['kdj.j:25,3,3/20.0'].shift(1) | df[
        'kdj.j:25,3,3/20.0'].shift(2) | df['kdj.j:25,3,3/20.0'].shift(3))
    df['cci_kdj_sell_cond'] = (df['cci_cross_down']) \
                              & (df['kdj.j:25,3,3\80.0'] | df['kdj.j:25,3,3\80.0'].shift(1) | df[
        'kdj.j:25,3,3\80.0'].shift(2) | df['kdj.j:25,3,3\80.0'].shift(3))
    return df
def get_chart_1h():
    interval = '1h'
    period = 10
    atr_multiplier = 2.5
    window = "ema_60"
    limit = 800
    return interval, period, atr_multiplier, window, limit


def get_chart_4h():
    interval = '4h'
    period = 20
    atr_multiplier = 3.5
    window = "ema_144"
    limit = 800
    return interval, period, atr_multiplier, window, limit

def run_bot(symbol, interval, period, atr_multiplier, window, limit, alert_once, alerts_cci_kdj, alerts_pull_back, alerts_ha):
    try:
        now = datetime.datetime.now()
        print(f"Fetching Historical Klines: {symbol} - Chart: {interval} - Time: {now} ...... ")
        df = binance_client.fetch_historical_klines(symbol=symbol, interval=interval, limit=limit)
        df = add_indicators(df)
        df = add_indicators_signal_flag(df)
        df = SupertrendIndicator(df=df, period=period, atr_multiplier=atr_multiplier, window=window).supertrend()

        # get current bar -1 because bar doesn't close
        alert_once[symbol] = send_super_trend_message(symbol, interval, df, alert_once[symbol])
        alerts_cci_kdj[symbol] = send_cci_kdj_message(symbol, interval, df, alerts_cci_kdj[symbol])
        alerts_pull_back[symbol] = send_supertrend_pull_back_message(symbol, interval, df, alerts_pull_back[symbol])
        alerts_ha[symbol] = send_heiken_ashi_message(symbol, interval, df, alerts_ha[symbol])
        print(df.tail(4))
        # exit()
        return alert_once, alerts_cci_kdj, alerts_pull_back, alerts_ha
    except Exception as e:
        print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
        pass

if __name__ == '__main__':
    binance_client = BinanceClient()
    symbols = binance_client.get_all_tickers()
    interval1h, period1h, atr_multiplier1h, window1h, limit1h = get_chart_1h()
    interval4h, period4h, atr_multiplier4h, window4h, limit4h = get_chart_4h()

    alerts1h = {}.fromkeys(symbols, False)
    alerts_cci_kdj_1h = {}.fromkeys(symbols, False)
    alerts_pull_back_1h = {}.fromkeys(symbols, False)
    alerts_ha_1h = {}.fromkeys(symbols, False)
    alerts4h = {}.fromkeys(symbols, False)
    alerts_cci_kdj_4h = {}.fromkeys(symbols, False)
    alerts_pull_back_4h = {}.fromkeys(symbols, False)
    alerts_ha_4h = {}.fromkeys(symbols, False)

    for symbol in symbols:
        if 'USDT' in symbol:
            try:
                schedule.every(2).seconds.do(run_bot, symbol, interval1h, period1h, atr_multiplier1h, window1h, limit1h,
                                             alerts1h, alerts_cci_kdj_1h, alerts_pull_back_1h, alerts_ha_1h)
                schedule.every(2).seconds.do(run_bot, symbol, interval4h, period4h, atr_multiplier4h, window4h, limit4h,
                                             alerts4h, alerts_cci_kdj_4h, alerts_pull_back_4h, alerts_ha_4h)
            except Exception as e:
                print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
                pass

    while True:
        schedule.run_pending()