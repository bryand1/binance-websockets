CREATE DATABASE IF NOT EXISTS binance DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
USE binance;

CREATE TABLE IF NOT EXISTS aggTrade (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  eventTime DATETIME,
  tickerSymbol VARCHAR(8),
  aggregateTradeId INT UNSIGNED,
  price DECIMAL(14, 8) UNSIGNED,
  quantity INT,
  firstTradeId INT,
  lastTradeId INT,
  tradeTime DATETIME,
  isMarketMaker TINYINT(1) UNSIGNED,
  INDEX(eventTime, tickerSymbol)
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS trade (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  eventTime DATETIME,
  tickerSymbol VARCHAR(8),
  tradeId INT UNSIGNED,
  price DECIMAL(14, 8) UNSIGNED,
  quantity INT,
  buyerOrderId INT,
  sellerOrderId INT,
  tradeTime DATETIME,
  isMarketMaker TINYINT(1) UNSIGNED,
  INDEX(eventTime, tickerSymbol)
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS kline (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  eventTime DATETIME,
  tickerSymbol VARCHAR(8),
  klineStartTime DATETIME,
  klineCloseTime DATETIME,
  klineTickerSymbol VARCHAR(8),
  klineInterval VARCHAR(4),
  klineFirstTradeId INT UNSIGNED,
  klineLastTradeId INT UNSIGNED,
  klineOpenPrice DECIMAL(14, 8) UNSIGNED,
  klineClosePrice DECIMAL(14, 8) UNSIGNED,
  klineHighPrice DECIMAL(14, 8) UNSIGNED,
  klineLowPrice DECIMAL(14, 8) UNSIGNED,
  klineBaseAssetVol INT UNSIGNED,
  klineNumberOfTrades INT UNSIGNED,
  klineIsClosed TINYINT(1) UNSIGNED,
  klineQuoteAssetVol DECIMAL(14, 8) UNSIGNED,
  klineTakerBuyBaseAssetVol INT UNSIGNED,
  klineTakerBuyQuoteAssetVol DECIMAL(14, 8) UNSIGNED
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ticker (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  tickerSymbol VARCHAR(8),
  priceChange DECIMAL(14, 8),
  priceChangePct DECIMAL(14, 2),
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
  totalTradedBaseAssetVol INT UNSIGNED,
  totalTradedQuoteAssetVol INT UNSIGNED,
  statisticsOpenTime INT UNSIGNED,
  statisticsCloseTime INT UNSIGNED,
  firstTradeId INT UNSIGNED,
  lastTradeId INT UNSIGNED,
  totalNumberOfTrades INT UNSIGNED
) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS alltickers (

) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS miniticker (

) ENGINE=INNODB
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


