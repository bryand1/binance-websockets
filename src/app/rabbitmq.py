"""
RabbitMQ
"""
import aio_pika
import asyncio
import json
from typing import Dict

from .util import json_converter


class RabbitMQ:

    timeout = 5

    @classmethod
    async def connect(cls, config: Dict, prefetch_count: int = 0):
        rmq = RabbitMQ(config)
        await rmq._connect()
        await rmq._set_qos(prefetch_count=prefetch_count)
        return rmq

    def __init__(self, config: Dict):
        self.config = config
        self.conn = None
        self.channel = None

    async def _connect(self):
        self.conn = await asyncio.wait_for(aio_pika.connect(**self.config), timeout=RabbitMQ.timeout)
        self.channel = await self.conn.channel()

    async def _set_qos(self, prefetch_count: int = 0, prefetch_size: int = 0,
                       all_channels: bool = False, timeout: int = None):
        await self.channel.set_qos(prefetch_count=prefetch_count,
                                   prefetch_size=prefetch_size,
                                   all_channels=all_channels,
                                   timeout=timeout)

    async def create_exchange(self, name, **kwargs):
        return await self.channel.declare_exchange(name=name, **kwargs)

    async def create_queue(self, name, **kwargs):
        return await self.channel.declare_queue(name=name, **kwargs)

    @staticmethod
    def to_rmq_message(data, headers=None):
        if isinstance(data, bytes):
            return aio_pika.Message(data, headers=headers)
        else:
            json_data = json.dumps(data, default=json_converter)
            return aio_pika.Message(bytes(json_data, 'utf-8'), headers=headers)
