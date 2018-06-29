CREATE DATABASE IF NOT EXISTS binance DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
USE binance;

CREATE TABLE IF NOT EXISTS aggTrade (
  eventTime BIGINT UNSIGNED,
  tickerSymbol VARCHAR(8),
  aggregateTradeId INT UNSIGNED,
  price DECIMAL(14, 8) UNSIGNED,
  quantity INT UNSIGNED,
  firstTradeId INT UNSIGNED,
  lastTradeId INT UNSIGNED,
  tradeTime BIGINT UNSIGNED,
  isMarketMaker TINYINT(1) UNSIGNED,
  INDEX(tickerSymbol, eventTime)
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS trade (
  eventTime BIGINT UNSIGNED,
  tickerSymbol VARCHAR(8),
  tradeId INT UNSIGNED,
  price DECIMAL(14, 8) UNSIGNED,
  quantity INT UNSIGNED,
  buyerOrderId INT UNSIGNED,
  sellerOrderId INT UNSIGNED,
  tradeTime BIGINT UNSIGNED,
  isMarketMaker TINYINT(1) UNSIGNED,
  INDEX(tickerSymbol, eventTime)
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS kline (
  eventTime BIGINT UNSIGNED,
  tickerSymbol VARCHAR(8),
  klineStartTime BIGINT UNSIGNED,
  klineCloseTime BIGINT UNSIGNED,
  klineInterval VARCHAR(4),
  firstTradeId INT UNSIGNED,
  lastTradeId INT UNSIGNED,
  openPrice DECIMAL(14, 8) UNSIGNED,
  closePrice DECIMAL(14, 8) UNSIGNED,
  highPrice DECIMAL(14, 8) UNSIGNED,
  lowPrice DECIMAL(14, 8) UNSIGNED,
  baseAssetVolume INT UNSIGNED,
  numberOfTrades INT UNSIGNED,
  isKlineClosed TINYINT(1) UNSIGNED,
  quoteAssetVolume DECIMAL(14, 8) UNSIGNED,
  takerBuyBaseAssetVolume INT UNSIGNED,
  takerBuyQuoteAssetVolume DECIMAL(14, 8) UNSIGNED,
  INDEX(tickerSymbol, eventTime)
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ticker_24hr (
  eventTime BIGINT UNSIGNED,
  tickerSymbol VARCHAR(8),
  priceChange DECIMAL(14, 8),
  priceChangePercent DECIMAL(14, 2),
  weightedAveragePrice DECIMAL(14, 8),
  previousDayClosePrice DECIMAL(14, 8),
  currentDayClosePrice DECIMAL(14, 8),
  closeTradeQuantity INT,
  bestBidPrice DECIMAL(14, 8) UNSIGNED,
  bestBidQuantity INT UNSIGNED,
  bestAskPrice DECIMAL(14, 8) UNSIGNED,
  bestAskQuantity INT UNSIGNED,
  openPrice DECIMAL(14, 8),
  highPrice DECIMAL(14, 8),
  lowPrice DECIMAL(14, 8),
  totalTradedBaseAssetVolume INT UNSIGNED,
  totalTradedQuoteAssetVolume INT UNSIGNED,
  statisticsOpenTime BIGINT UNSIGNED,
  statisticsCloseTime BIGINT UNSIGNED,
  firstTradeId INT UNSIGNED,
  lastTradeId INT UNSIGNED,
  totalNumberOfTrades INT UNSIGNED
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

/*
CREATE TABLE IF NOT EXISTS alltickers (

) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS miniticker (

) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
*/
