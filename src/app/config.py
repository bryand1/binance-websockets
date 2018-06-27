# -*- coding: utf-8 -*-

base_endpoint = 'wss://stream.binance.com:9443'
ticker = 'bnbbtc'
stream = 'aggTrade'

logfmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

database = {
    'connector': '',
    'credentials': {
    }
}

tickers = {
    'bnbbtc',
    'ethbtc'
}

coins = {
    'btc': 'Bitcoin',
    'eth': 'Ethereum',
    'ltc': 'Litecoin',
    'bnb': 'Binance Coin',
}
