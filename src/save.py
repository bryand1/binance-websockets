#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Binance rates

@author Bryan Andrade <bryand1@gmail.com>
@version 0.0.1

Save data from RabbitMQ to permanent storage
"""
import argparse
import asyncio
import json
import os
import sys
import traceback

from aio_pika import ExchangeType, IncomingMessage
from elasticsearch_async import AsyncElasticsearch

import app

logger = app.util.get_logger("save")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

queue = dict()


async def configure() -> None:
    global queue
    rmq = await app.rabbitmq.RabbitMQ.connect(conf['rabbitmq'])
    exchange = await rmq.create_exchange('binance', type=ExchangeType.FANOUT, durable=True)
    for name in ('mysql', 'elasticsearch'):
        queue[name] = await rmq.create_queue(name, durable=True)
        await queue[name].bind(exchange)


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

    queue['mysql'].consume(callback=consumer)


async def es():
    global queue

    client = AsyncElasticsearch(hosts=conf['elasticsearch']['hosts'])

    while True:
        try:
            message = await queue['elasticsearch'].get(timeout=1)
        except TimeoutError:
            continue
        entry = json.loads(message.body.decode('utf-8'))
        if '_ignore' in entry:
            del entry['_ignore']
        index = app.storage.es.index_conv.get(entry['eventType'], entry['eventType'])
        await client.index(index, doc_type='_doc', body=entry)
        message.ack()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=str)
    args = parser.parse_args()
    dst = args.destination if args.destination else "mysql"

    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(configure())
    loop.run_until_complete(locals()[dst]())
    loop.run_forever()
