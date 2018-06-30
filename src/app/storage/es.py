from typing import Dict

from elasticsearch_async import AsyncElasticsearch

from app import util


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
