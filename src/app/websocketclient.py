import asyncio
import websockets

from . import util


class WebsocketClient:

    logger = util.get_logger("app.websocketclient.WebsocketClient")

    reconnect_time = 20

    @classmethod
    async def connect(cls, uri):
        ws_client = WebsocketClient(uri)
        await ws_client._connect()
        return ws_client

    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self.consumer = None

    async def _connect(self):
        self.logger.info("connecting to %s", self.uri)
        self.ws = await websockets.connect(self.uri)

    async def _recv(self):
        while True:
            data = await self.ws.recv()
            self.logger.debug(data)
            if self.consumer is not None:
                await self.consumer(data)

    async def recv(self, consumer=None):
        if consumer is not None:
            self.consumer = consumer
        while True:
            try:
                await self._recv()
            except websockets.ConnectionClosed:
                self.logger.warning("connection closed, reconnecting in %d seconds", self.reconnect_time)
                await asyncio.sleep(self.reconnect_time)
                await self._connect()
