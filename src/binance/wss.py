# -*- coding: utf-8 -*-
"""
Map abbreviated key from web socket streams to full key name
@author Bryan Andrade <bryand1@gmail.com>

https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md
"""

"""
Aggregated Trade Streams

The Aggregate Trade Streams push trade information that is aggregated for a single taker order.

Stream Name: <symbol>@aggTrade

Payload:

{
  "e": "aggTrade",  // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "a": 12345,       // Aggregate trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "f": 100,         // First trade ID
  "l": 105,         // Last trade ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore.
}

"""
agg_trade = {
  'e': 'eventType',
  'E': 'eventTime',
  's': 'tickerSymbol',
  'a': 'aggregateTradeID',
  'p': 'price',
  'q': 'quantity',
  'f': 'firstTradeID',
  'l': 'lastTradeID',
  'T': 'tradeTime',
  'm': 'isMarketMaker',
  'M': '_ignore'
}

"""
Trade Streams

The Trade Streams push raw trade information; each trade has a unique buyer and seller.

Stream Name: <symbol>@trade

Payload:

{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order Id
  "a": 50,          // Seller order Id
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore.
}
"""
trade = {
    'e': 'eventType',
    'E': 'eventTime',
    's': 'tickerSymbol',
    't': 'tradeID',
    'p': 'price',
    'q': 'quantity',
    'b': 'buyerOrderId',
    'a': 'sellerOrderID',
    'T': 'tradeTime',
    'm': 'isMarketMaker',
    'M': '_ignore'
}


def get_map(stream_name):
    """
    Return abbreviated key mapping
    :param stream_name: aggTrade | trade
    :return: dict
    """
    return {
        'aggTrade': agg_trade,
        'trade': trade,
    }[stream_name]
