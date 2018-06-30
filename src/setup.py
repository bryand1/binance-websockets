#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configure databases to accept binance rates

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

import app

logger = app.util.get_logger("setup")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


async def mysql():
    raise NotImplementedError


async def es():
    db = app.storage.es.Database(conf['elasticsearch'])

    info = await db.client.info()
    print(info)

    # async def consumer(message: IncomingMessage):
    #     entry = json.loads(message.body.decode('utf-8')
    #     await db.save(entry)
    #     message.ack()

    # queue['elasticsearch'].consume(callback=consumer)

    await db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", type=str, default="es")
    args = parser.parse_args()

    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(locals()[args.store]())
    loop.close()
