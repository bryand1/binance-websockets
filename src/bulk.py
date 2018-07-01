#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Binance rates

@author Bryan Andrade <bryand1@gmail.com>
@version 0.0.1

Save data from RabbitMQ to elasticsearch
"""
import asyncio
import json
import os
import sys
import time
import traceback

from aio_pika import ExchangeType
from elasticsearch import Elasticsearch
from elasticsearch import helpers

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
    logger.info("Configuring RabbitMQ")
    rmq = await app.rabbitmq.RabbitMQ.connect(conf['rabbitmq'])
    exchange = await rmq.create_exchange('binance', type=ExchangeType.FANOUT, durable=True)
    queue = await rmq.create_queue('elasticsearch', durable=True)
    await queue.bind(exchange)


async def es():
    global queue
    logger.info("Creating bulk actions")
    actions = []
    for _ in range(20000):
        try:
            message = await queue.get(timeout=1)
        except TimeoutError:
            break
        entry = json.loads(message.body.decode('utf-8'))
        if '_ignore' in entry:
            del entry['_ignore']
        index = app.storage.es.index_conv.get(entry['eventType'], entry['eventType'])
        action = {
            '_index': index,
            '_type': '_doc',
            '_source': entry
        }
        message.ack()
        actions.append(action)
    return actions


if __name__ == '__main__':

    start_time = time.time()
    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(configure())
    actions = loop.run_until_complete(es())
    loop.close()
    logger.info("%d actions retrieved", len(actions))

    logger.info("Connecting to elasticsearch")
    client = Elasticsearch(hosts=['elasticsearch'])
    ret = helpers.bulk(client, actions)
    logger.info("%r", ret)
    logger.info("Execution time: %.2f seconds", time.time() - start_time)
