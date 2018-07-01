# -*- coding: utf-8 -*-
import logging
import os

appdir = os.path.dirname(os.path.abspath(__file__))
srcdir = os.path.dirname(appdir)

base_endpoint = 'wss://stream.binance.com:9443'
ticker = 'bnbbtc'
stream = 'aggTrade'

loglvl = logging.INFO
logfmt = "%(asctime)s:%(levelname)s:binance-websockets:%(name)s:%(filename)s:%(lineno)d:%(message)s"
datefmt = "%Y-%m-%dT%H:%M:%SZ"

tickers = {
    'ethbtc',
    'ethusdt',
    'ltceth',
    'ltcusdt',
    'btcusdt'
}

coins = {
    'btc': 'Bitcoin',
    'eth': 'Ethereum',
    'ltc': 'Litecoin',
    'bnb': 'Binance Coin',
    'usdt': 'Tether'
}
