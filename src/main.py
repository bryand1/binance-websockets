#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Binance web sockets streams

@author Bryan Andrade <bryand1@gmail.com>
@version 0.0.1

Connect to Binance and capture streaming data
"""
import argparse
import asyncio
import json
import os
import sys
import traceback

import app

logger = app.util.get_logger("main")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', type=str, default=app.config.base_endpoint)
    parser.add_argument('--ticker', type=str, default=app.config.ticker)
    parser.add_argument('--stream', type=str, default=app.config.stream)
    args = parser.parse_args()

    with open(os.path.join(app.config.srcdir, 'config.json')) as fp:
        conf = json.load(fp)['rabbitmq']

    # wss://stream.binance.com:9443/ws/bnbbtc@aggTrade
    endpoint_from_args = "{}/ws/{}@{}".format(args.endpoint, args.ticker, args.stream)
    endpoint = os.environ.get('ENDPOINT', '') or endpoint_from_args
    stream = endpoint[endpoint.rfind('@') + 1:]
    index = stream.find('_')
    stream = stream[:index] if index > -1 else stream
    logger.info("endpoint = %r", endpoint)
    logger.info("stream = %r", stream)

    mapping = app.binance.wss.get_map(stream)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.configure(conf))
    loop.run_until_complete(app.wss(endpoint, mapping))
    loop.close()
