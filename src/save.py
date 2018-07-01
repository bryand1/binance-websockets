#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Binance rates

@author Bryan Andrade <bryand1@gmail.com>
@version 0.0.1

Save data from RabbitMQ to MySQL
"""
import asyncio
import json
import os
import sys
import traceback

from aio_pika import ExchangeType, IncomingMessage

import app

logger = app.util.get_logger("save")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

queue = None


async def configure() -> None:
    global queue
    rmq = await app.rabbitmq.RabbitMQ.connect(conf['rabbitmq'])
    exchange = await rmq.create_exchange('binance', type=ExchangeType.FANOUT, durable=True)
    queue = await rmq.create_queue('mysql', durable=True)
    await queue.bind(exchange)


async def mysql():
    import pymysql.err
    import warnings
    warnings.simplefilter("ignore", pymysql.err.Warning)

    global queue

    db = await app.storage.mysql.Database.connect(conf['database'])

    async def consumer(message: IncomingMessage):
        entry = json.loads(message.body.decode('utf-8'))
        await db.save(entry)
        message.ack()

    queue.consume(callback=consumer)


if __name__ == '__main__':
    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(configure())
    loop.run_until_complete(mysql())
    loop.run_forever()
