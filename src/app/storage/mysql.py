from typing import Dict
from aiomysql import create_pool
from app import util
import sys
import traceback


class Database:
    logger = util.get_logger('app.storage.mysql.Database')

    # Convert 24hrTicker to avoid leading number in table name
    table_conv = {
        '24hrTicker': 'ticker_24hr',
    }

    @classmethod
    async def connect(cls, config):
        db = Database(config)
        await db.init_pool()
        return db

    def __init__(self, config: Dict):
        self.config = config
        self.pool = None

    async def init_pool(self):
        self.pool = await create_pool(use_unicode=True, charset="utf8", **self.config)

    async def save(self, entry: Dict):
        if '_ignore' in entry:
            del entry['_ignore']
        table = self.table_conv.get(entry['eventType']) or entry['eventType']
        del entry['eventType']
        sql = "INSERT INTO {} ({}) VALUES ({})".format(
            table,
            ', '.join(entry.keys()),
            ', '.join(['%s'] * len(entry))
        )
        args = tuple(entry.values())
        async with self.pool.acquire() as conn:
            try:
                cursor = await conn.cursor()
                await cursor.execute(sql, args)
                await conn.commit()
            except Exception:
                self.logger.error(
                    "MySQL Database Error:%s",
                    traceback.format_exception(*sys.exc_info()))

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()
