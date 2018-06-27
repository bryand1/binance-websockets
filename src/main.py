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

    stream_url = "{}/ws/{}@{}".format(args.endpoint, args.ticker, args.stream)
    logger.info("stream_url = %r", stream_url)

    mapping = app.binance.wss.get_map(args.stream)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.configure(conf))
    loop.run_until_complete(app.wss(stream_url, mapping))
    loop.close()
