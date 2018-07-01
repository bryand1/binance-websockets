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
  "e": "eventType",
  "E": "eventTime",
  "s": "tickerSymbol",
  "a": "aggregateTradeId",
  "p": "price",
  "q": "quantity",
  "f": "firstTradeId",
  "l": "lastTradeId",
  "T": "tradeTime",
  "m": "isMarketMaker",
  "M": "_ignore"
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
    "e": "eventType",
    "E": "eventTime",
    "s": "tickerSymbol",
    "t": "tradeID",
    "p": "price",
    "q": "quantity",
    "b": "buyerOrderId",
    "a": "sellerOrderID",
    "T": "tradeTime",
    "m": "isMarketMaker",
    "M": "_ignore"
}

"""
Kline/Candlestick Streams

The Kline/Candlestick Stream push updates to the current klines/candlestick every second.

Kline/Candlestick chart intervals:

m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

1m
3m
5m
15m
30m
1h
2h
4h
6h
8h
12h
1d
3d
1w
1M
Stream Name: <symbol>@kline_<interval>

Payload:

{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
"""
kline = {
    "e": "eventType",
    "E": "eventTime",
    "s": "tickerSymbol",
    "t": "klineStartTime",
    "T": "klineCloseTime",
    "i": "klineInterval",
    "f": "firstTradeId",
    "L": "lastTradeId",
    "o": "openPrice",
    "c": "closePrice",
    "h": "highPrice",
    "l": "lowPrice",
    "v": "baseAssetVolume",
    "n": "numberOfTrades",
    "x": "isKlineClosed",
    "q": "quoteAssetVolume",
    "V": "takerBuyBaseAssetVolume",
    "Q": "takerBuyQuoteAssetVolume",
    "B": "_ignore"
}

"""
Individual symbol ticker streams

24hr Ticker statistics for a single symbol pushed every second

Stream Name: <symbol>@ticker

Payload:

{
  "Q": "10",          // Close trade's quantity
  "b": "0.0024",      // Best bid price
  "B": "10",          // Best bid quantity
  "a": "0.0026",      // Best ask price
  "A": "100",         // Best ask quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 86400000,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}
"""
ticker = {
  "e": "eventType",
  "E": "eventTime",
  "s": "tickerSymbol",
  "p": "priceChange",
  "P": "priceChangePercent",
  "w": "weightedAveragePrice",
  "x": "previousDayClosePrice",
  "c": "currentDayClosePrice",
  "Q": "closeTradeQuantity",
  "b": "bestBidPrice",
  "B": "bestBidQuantity",
  "a": "bestAskPrice",
  "A": "bestAskQuantity",
  "o": "openPrice",
  "h": "highPrice",
  "l": "lowPrice",
  "v": "totalTradedBaseAssetVolume",
  "q": "totalTradedQuoteAssetVolume",
  "O": "statisticsOpenTime",
  "C": "statisticsCloseTime",
  "F": "firstTradeId",
  "L": "lastTradeId",
  "n": "totalNumberOfTrades"
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
        'kline': kline,
        'ticker': ticker,
    }[stream_name]
