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
from app import binance, config, util
import json
import sys
import traceback
import websockets

logger = util.get_logger("main")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception:%s", traceback.format_exception(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


async def wss(url):
    """
    Connect and consume data
    :param url: Binance web socket stream endpoint
    :return:
    """
    async with websockets.connect(url) as websocket:
        logger.debug("Connected to %s", url)
        while True:
            msg = await websocket.recv()
            await consume(msg)


async def consume(msg):
    data = {mapping[k]: v for k, v in json.loads(msg).items()}
    logger.info(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', type=str, default=config.base_endpoint)
    parser.add_argument('--ticker', type=str, default=config.ticker)
    parser.add_argument('--stream', type=str, default=config.stream)
    args = parser.parse_args()

    stream_url = "{}/ws/{}@{}".format(args.endpoint, args.ticker, args.stream)
    mapping = binance.wss.get_map(args.stream)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wss(stream_url))
    loop.close()
