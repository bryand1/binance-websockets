import json
import websockets

from . import binance, config, rabbitmq, util

logger = util.get_logger("app")

rmq = None
exchange = None


async def configure(rabbitmq_conf: dict) -> None:
    global rmq, exchange
    rmq = rabbitmq.RabbitMQ(rabbitmq_conf)
    await rmq.configure()
    exchange = await rmq.create_exchange('binance', type='fanout', durable=True)
    for name in ('mysql', 'elasticsearch'):
        queue = await rmq.create_queue(name, durable=True)
        await queue.bind(exchange)


async def wss(url: str, mapping: dict) -> None:
    """
    Connect and consume data
    :param url: Binance web socket stream endpoint
    :param mapping: map for reading json document
    :return:
    """
    global exchange
    async with websockets.connect(url) as websocket:
        logger.info("Connected to %s", url)
        while True:
            msg = await websocket.recv()
            data = {mapping[k]: v for k, v in json.loads(msg).items()}
            await exchange.publish(rmq.to_rmq_message(data))
