## Simon Custom Indicators Telegram Notifications Bot
A notifications' bot made with Python,  which executes message to telegram on trend changes.

## Use the following strategy 🚀
* Supertrend
* KDJ Stochastic
* Commodity Channel Index (CCI)
* Smoothed Heikin Ashi Candles
* Volume Weighted Moving Average (VWMA)

## Install Dependencies 🛠

Install Python dependencies provided in the `requirements.txt` file.

Run the following line in the project directory: 

```
pip install -r requirements.txt
```

## Built With 🚀
* [pyTelegramBotAPI - PyPI](https://pypi.org/project/pyTelegramBotAPI/)
* [pandas - Python Data Analysis Library](https://pandas.pydata.org/) 
* [schedule - PyPI](https://pypi.org/project/schedule/)
* [python-binance - Python Binance Library](https://python-binance.readthedocs.io/en/latest/)
* [ccxt · PyPI](https://pypi.org/project/ccxt/)
* [ta - PyPI](https://pypi.org/project/ta/)
* [stock-pandas - Inherits and extends pandas.DataFrame](https://stock-pandas.readthedocs.io/en/latest/README.html)

## Create user configuration 🔑

All of the options provided in `config.py` should be configured.

**The configuration file consists of the following fields:**

-   **BINANCE_API_KEY** - Binance API key generated in the Binance account setup stage.
-   **BINANCE_SECRET_KEY** - Binance secret key generated in the Binance account setup stage.
-   **TELEGRAM_API_KEY** - Telegram API key generated in the Binance account setup stage.
-   **TELEGRAM_CHAT_ID** - Telegram Chat ID generated in the Binance account setup stage.

```
BINANCE_API_KEY = 'Your Binance Api Key goes here'
BINANCE_SECRET_KEY = 'Your Binance Api Secret goes here'
TELEGRAM_API_KEY = "Your Telegram Api Key goes here" 
TELEGRAM_CHAT_ID = xxx
```

After configuration is being made, save file `Ctrl+S` and exit.

## Deploy Bot 🤖

Run the following line in the project directory: 

```
python main.py
```
Exit at any time with `Ctrl+C`.

## Disclaimer ✔

This software is for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. I ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

Always start by running a trading bot in PAPER-TRADING and do not engage money before you understand how it works and what profit/loss you should expect.

I strongly recommend you to have coding and Python knowledge. Do not hesitate to read the source code and understand the mechanism of this bot.
