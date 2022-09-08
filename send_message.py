from builtins import print


from services.telegram.client import TeleClient

def round_with_precision(normalized, precision):
    return round(normalized, precision)

def get_precision(default):
    array = str(default).split('.')
    precision = len(array[1])
    return precision

def add_supertrend_pull_back_condition(df):
    pull_back_long_cond = (df['increase:(kdj.j:25,3,3),3,-1']) \
                          & (df['cci_18'] <= -200.0) \
                          & (df['kdj.j:25,3,3,50.0<=20.0']) \
                          & ((df['close'].shift(1) - (df['close'].shift(1) * 0.03)) <= df['atr_lower'].shift(1)) \
                          & (df['in_uptrend'] == True)
    pull_back_short_cond = (df['increase:(kdj.j:25,3,3),3,1']) \
                           & (df['cci_18'] >= 200.0) \
                           & (df['kdj.j:25,3,3,50.0>=80.0']) \
                           & ((df['close'].shift(1) + (df['close'].shift(1) * 0.03)) >= df['atr_upper'].shift(1)) \
                           & (df['in_uptrend'] == False)
    df['pull_back_long_cond'] = pull_back_long_cond
    df['pull_back_short_cond'] = pull_back_short_cond
    return df
def send_supertrend_pull_back_message(symbol, interval, df, alert_once):
    try :
        current_index = len(df.index) - 2
        previous_index = current_index - 1
        df = add_supertrend_pull_back_condition(df)

        current_closed_price = df["close"][current_index]
        precision = get_precision(current_closed_price)
        atr_upper = df["atr_upper"][current_index]
        atr_lower = df["atr_lower"][current_index]

        if df['pull_back_long_cond'][current_index] and not alert_once:
            print("Pull back long condition triggered, buy")
            sl = round_with_precision(atr_lower, precision)
            message = f'LONG {symbol} - Chart: {interval} 💎\n\n' \
                      f'New Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n' \
                      f'#{symbol} #super_trend_pull_back #long #short_term #pull_back_entry \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif df['pull_back_short_cond'][current_index] and not alert_once:
            print("Pull back short condition triggered, buy")
            sl = round_with_precision(atr_upper, precision)
            message = f'SHORT {symbol} - Chart: {interval} 💎\n\n' \
                      f'New Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n' \
                      f'#{symbol} #super_trend_pull_back #short #short_term #pull_back_entry \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif (
                df['pull_back_short_cond'][previous_index] == df['pull_back_short_cond'][current_index]
                and df['pull_back_long_cond'][previous_index] == df['pull_back_long_cond'][current_index]
        ) and alert_once:
            print("set alert pull back back to False")
            alert_once = False
    except Exception as e:
        print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
        pass
    return alert_once

def send_cci_kdj_message(symbol, interval, df, alert_once):
    try :
        current_index = len(df.index) - 2
        previous_index = current_index - 1
        current_closed_price = df["close"][current_index]
        precision = get_precision(current_closed_price)
        diff_percent = round_with_precision(current_closed_price * 0.05, precision)

        if df['cci_kdj_buy_cond'][current_index] and not alert_once:
            print("CCI - KDJ Signal triggered, buy")
            sl = round_with_precision(current_closed_price - diff_percent, precision)
            tp = round_with_precision(current_closed_price + diff_percent, precision)
            message = f'LONG {symbol} - Chart: {interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl} (-5%)\n\n' \
                      f'TP: ${tp} (5%)\n' \
                      f'#{symbol} #cci_kdj_signal #short_term #long #pull_back_entry \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif df['cci_kdj_sell_cond'][current_index] and not alert_once:
            print("CCI - KDJ Signal triggered, sell")
            sl = round_with_precision(current_closed_price + diff_percent, precision)
            tp = round_with_precision(current_closed_price - diff_percent, precision)
            message = f'SHORT {symbol} - Chart: {interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl} (-5%)\n\n' \
                      f'TP: ${tp} (5%)\n' \
                      f'#{symbol} #cci_kdj_signal #short_term #short #pull_back_entry \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif (df['cci_kdj_sell_cond'][previous_index] == df['cci_kdj_sell_cond'][current_index]
                      and df['cci_kdj_buy_cond'][previous_index] == df['cci_kdj_buy_cond'][current_index]) \
                and alert_once:
            print("set alert cci kdj back to False")
            alert_once = False
    except Exception as e:
        print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
        pass
    return alert_once

def send_heiken_ashi_message(symbol, interval, df, alert_once):
    try:
        current_index = len(df.index) - 2
        previous_index = current_index - 1

        current_closed_price = df["close"][current_index]
        precision = get_precision(current_closed_price)
        atr_upper = df["atr_upper"][current_index]
        atr_lower = df["atr_lower"][current_index]

        # Buy
        if df['ha_vwma_in_uptrend'][current_index] and df['in_uptrend'][current_index] and not alert_once:
            print("heikin ashi changed to uptrend, buy " + symbol)
            sl = round_with_precision(atr_lower, precision)
            message = f'LONG {symbol} - Chart:{interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n' \
                      f'#{symbol} #heikin_ashi_signal #pull_back_entry #long #short_term \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif df['ha_vwma_in_downtrend'][current_index] and not df['in_uptrend'][current_index] and not alert_once:
            print("heikin ashi changed to downtrend, sell " + symbol)
            sl = round_with_precision(atr_upper, precision)
            message = f'SHORT {symbol} - Chart:{interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n' \
                      f'#{symbol} #heikin_ashi_signal #pull_back_entry #short_term #short \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif (df['ha_vwma_in_downtrend'][previous_index] == df['cci_kdj_sell_cond'][current_index]
                      and df['ha_vwma_in_uptrend'][previous_index] == df['ha_vwma_in_uptrend'][current_index]) and alert_once:
            print("set alert back to False")
            alert_once = False
    except Exception as e:
        print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
        pass
    return alert_once

def send_super_trend_message(symbol, interval, df, alert_once):
    try:
        current_index = len(df.index) - 2
        previous_index = current_index - 1

        current_closed_price = df["close"][current_index]
        precision = get_precision(current_closed_price)
        atr_upper = df["atr_upper"][current_index]
        atr_lower = df["atr_lower"][current_index]

        diff_5_percent = round_with_precision(current_closed_price * 0.05, precision)
        diff_10_percent = round_with_precision(current_closed_price * 0.10, precision)
        diff_15_percent = round_with_precision(current_closed_price * 0.15, precision)

        if not df['in_uptrend'][previous_index] and df['in_uptrend'][current_index] and not alert_once:
            print("changed to uptrend, buy " + symbol)
            sl = round_with_precision(atr_lower, precision)
            tp_5_percent = round_with_precision(current_closed_price + diff_5_percent, precision)
            tp_10_percent = round_with_precision(current_closed_price + diff_10_percent, precision)
            tp_15_percent = round_with_precision(current_closed_price + diff_15_percent, precision)
            message = f'LONG {symbol} - Chart:{interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n\n' \
                      f'TP 1: ${tp_5_percent} (5%)\n' \
                      f'TP 2: ${tp_10_percent} (10%)\n' \
                      f'TP 3: ${tp_15_percent} (15%)\n' \
                      f'#{symbol} #super_trend_signal #long #uptrend #long_term \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif df['in_uptrend'][previous_index] and not df['in_uptrend'][current_index] and not alert_once:
            print("changed to downtrend, sell " + symbol)
            sl = round_with_precision(atr_upper, precision)
            tp_5_percent = round_with_precision(current_closed_price - diff_5_percent, precision)
            tp_10_percent = round_with_precision(current_closed_price - diff_10_percent, precision)
            tp_15_percent = round_with_precision(current_closed_price - diff_15_percent, precision)
            message = f'SHORT {symbol} - Chart:{interval} 💎\n\n' \
                      f'Entry: ${current_closed_price}\n' \
                      f'SL: ${sl}\n\n' \
                      f'TP 1: ${tp_5_percent} (5%)\n' \
                      f'TP 2: ${tp_10_percent} (10%)\n' \
                      f'TP 3: ${tp_15_percent} (15%)\n' \
                      f'#{symbol} #super_trend_signal #short #downtrend #long_term \n\n'
            TeleClient(message=message).send_message()
            alert_once = True
        elif df['in_uptrend'][previous_index] == df['in_uptrend'][current_index] and alert_once:
            print("set alert back to False")
            alert_once = False
    except Exception as e:
        print("=========Ticker:" + symbol + " Error: " + str(e) + "===========")
        pass
    return alert_once