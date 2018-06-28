import json
from typing import Dict

from aio_pika import ExchangeType

from . import binance, config, rabbitmq, util, websocketclient

logger = util.get_logger("app")

exchange = None


async def configure(rabbitmq_conf: dict) -> None:
    global exchange
    rmq = await rabbitmq.RabbitMQ.connect(rabbitmq_conf)
    exchange = await rmq.create_exchange('binance', type=ExchangeType.FANOUT, durable=True)
    for name in ('mysql', 'elasticsearch'):
        queue = await rmq.create_queue(name, durable=True)
        await queue.bind(exchange)


async def wss(endpoint: str, mapping: dict) -> None:
    """
    Connect websocketclient and attach data consumer
    :param endpoint: Web socket stream endpoint
    :param mapping: map for reading json document
    :return:
    """
    global exchange

    async def consumer(msg):
        data = flatten(json.loads(msg), mapping)
        await exchange.publish(rabbitmq.RabbitMQ.to_rmq_message(data), routing_key='')

    ws = await websocketclient.WebsocketClient.connect(endpoint)
    await ws.recv(consumer=consumer)


def flatten(js: Dict, mapping: Dict) -> Dict:

    def helper(d: Dict, mutable: Dict = {}) -> Dict:
        for k, v in d.items():
            if isinstance(v, dict):
                helper(v)
            else:
                mutable[mapping[k]] = v
        return mutable

    return helper(js)
