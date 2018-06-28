import json
from typing import Dict

from aio_pika import ExchangeType
import websockets

from . import binance, config, rabbitmq, util

logger = util.get_logger("app")

rmq = None
exchange = None


async def configure(rabbitmq_conf: dict) -> None:
    global rmq, exchange
    rmq = rabbitmq.RabbitMQ(rabbitmq_conf)
    await rmq.configure()
    exchange = await rmq.create_exchange('binance', type=ExchangeType.FANOUT, durable=True)
    for name in ('mysql', 'elasticsearch'):
        queue = await rmq.create_queue(name, durable=True)
        await queue.bind(exchange)


async def wss(endpoint: str, mapping: dict) -> None:
    """
    Connect and consume data
    :param endpoint: Web socket stream endpoint
    :param mapping: map for reading json document
    :return:
    """
    global exchange
    async with websockets.connect(endpoint) as websocket:
        logger.info("Connected to %s", endpoint)
        while True:
            msg = await websocket.recv()
            data = flatten(json.loads(msg), mapping)
            logger.debug(data)
            await exchange.publish(rmq.to_rmq_message(data), routing_key='')


def flatten(js: Dict, mapping: Dict) -> Dict:

    def helper(d: Dict, mutable: Dict = {}) -> Dict:
        for k, v in d.items():
            if isinstance(v, dict):
                helper(v)
            else:
                mutable[mapping[k]] = v
        return mutable

    return helper(js)
