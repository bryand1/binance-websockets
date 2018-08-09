# Binance Python Web Sockets

Capture Binance websocket streams in Docker containers.

## Objective

Create lightweight, asynchronous Python code to capture one or a combination of Binance web socket streams.

## Getting Started

```bash
git clone https://github.com/bryand1/binance-websockets
cd binance-websockets
pip install -r requirements.txt
```

Set environment variables:

```bash
vi binance.env
export BINANCE_APIKEY=[YOUR KEY]
export BINANCE_SECRET=[YOUR KEY]
```

After setting environment variables, determine which database to use.
Edit *src/config.py*, find the variable *database*.

Run the script:

```bash
./docker-run.sh [container-name] [endpoint]
```
