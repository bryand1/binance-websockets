from typing import Dict

from elasticsearch_async import AsyncElasticsearch

from app import util

index_conv = {
    "aggTrade": "aggtrade",
    '24hrTicker': 'ticker_24hr',
}

body = {
    "aggTrade": {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "eventType": {"type": "keyword"},
                    "eventTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "tickerSymbol": {"type": "keyword"},
                    "aggregateTradeId": {"type": "integer"},
                    "price": {"type": "double"},
                    "quantity": {"type": "integer"},
                    "firstTradeId": {"type": "integer"},
                    "lastTradeId": {"type": "integer"},
                    "tradeTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "isMarketMaker": {"type": "boolean"}
                }
            }
        }
    },
    "trade": {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "eventType": {"type": "keyword"},
                    "eventTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "tickerSymbol": {"type": "keyword"},
                    "tradeId": {"type": "integer"},
                    "price": {"type": "double"},
                    "quantity": {"type": "integer"},
                    "buyerOrderId": {"type": "integer"},
                    "sellerOrderId": {"type": "integer"},
                    "tradeTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "isMarketMaker": {"type": "boolean"}
                }
            }
        }
    },
    "kline": {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "eventType": {"type": "keyword"},
                    "eventTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "tickerSymbol": {"type": "keyword"},
                    "klineStartTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "klineCloseTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "klineInterval": "term",
                    "firstTradeId": {"type": "integer"},
                    "lastTradeId": {"type": "integer"},
                    "openPrice": {"type": "double"},
                    "closePrice": {"type": "double"},
                    "highPrice": {"type": "double"},
                    "lowPrice": {"type": "double"},
                    "quantity": {"type": "integer"},
                    "baseAssetVolume": {"type": "integer"},
                    "numberOfTrades": {"type": "integer"},
                    "isKlineClosed": {"type": "boolean"},
                    "quoteAssetVolume": {"type": "double"},
                    "takerBuyBaseAssetVolume": {"type": "integer"},
                    "takerBuyQuoteAssetVolume": {"type": "double"}
                }
            }
        }
    },
    "ticker_24hr": {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "_doc": {
                "properties": {
                    "eventType": {"type": "keyword"},
                    "eventTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "tickerSymbol": {"type": "keyword"},
                    "priceChange": {"type": "double"},
                    "priceChangePercent": {"type": "double"},
                    "weightedAveragePrice": {"type": "double"},
                    "previousDayClosePrice": {"type": "double"},
                    "currentDayClosePrice": {"type": "double"},
                    "closeTradeQuantity": {"type": "integer"},
                    "bestBidPrice": {"type": "double"},
                    "bestBidQuantity": {"type": "integer"},
                    "bestAskPrice": {"type": "double"},
                    "bestAskQuantity": {"type": "integer"},
                    "openPrice": {"type": "double"},
                    "highPrice": {"type": "double"},
                    "lowPrice": {"type": "double"},
                    "totalTradedBaseAssetVolume": {"type": "integer"},
                    "totalTradedQuoteAssetVolume": {"type": "integer"},
                    "statisticsOpenTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "statisticsCloseTime": {
                        "type": "date",
                        "format": "epoch_millis"
                    },
                    "firstTradeId": {"type": "integer"},
                    "lastTradeId": {"type": "integer"},
                    "totalNumberOfTrades": {"type": "integer"}
                }
            }
        }
    }
}


class Database:
    logger = util.get_logger('app.storage.es.Database')

    def __init__(self, config: Dict):
        self.client = AsyncElasticsearch(hosts=config['hosts'])

    async def save(self, entry: Dict):
        if '_ignore' in entry:
            del entry['_ignore']
        # Select index based on eventType
        del entry['eventType']
        # Store in elasticsearch

    async def close(self):
        await self.client.transport.close()
