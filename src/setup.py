#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configure databases to accept binance rates

@author Bryan Andrade <bryand1@gmail.com>
@version 0.0.1

Save data from RabbitMQ to permanent storage
"""
import asyncio
import json
import os
import sys
import traceback

from elasticsearch_async import AsyncElasticsearch

import app

logger = app.util.get_logger("setup")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


async def main():
    client = AsyncElasticsearch(hosts=conf['elasticsearch']['hosts'])
    for index in conf['elasticsearch']['indices']:
        await client.indices.create(index, body=app.storage.es.body.get(index))
    await client.transport.close()

if __name__ == '__main__':
    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
