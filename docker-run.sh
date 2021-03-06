#!/usr/bin/env bash

# Binance websocket endpoints:
# wss://stream.binance.com:9443/ws/ethbtc@aggTrade
# wss://stream.binance.com:9443/ws/ethbtc@trade
# wss://stream.binance.com:9443/ws/ethbtc@kline_1m  (1m, 3m, 5m, 15m, 30m)
# wss://stream.binance.com:9443/ws/ethbtc@kline_1h  (1h, 2h, 4h, 6h, 8h, 12h)
# wss://stream.binance.com:9443/ws/ethbtc@kline_1d  (1d, 3d, 1w, 1M)
# wss://stream.binance.com:9443/ws/ethbtc@ticker

# Tickers:
# ethbtc
# ethusdt
# ltceth
# ltcusdt
# btcusdt

if [[ -z "$2" ]]; then
  printf "usage: ./docker-run.sh container-name endpoint\n\n"
  printf "Binance websocket endpoint example:\n"
  printf "wss://stream.binance.com:9443/ws/ethbtc@aggTrade\n\n"
  exit 1
fi

cd "$(dirname "${BASH_SOURCE[0]}")"
source ./binance.env

sudo docker run -d --name "$1" --rm --net crypto --mount type=bind,src="$(pwd)"/src,dst=/usr/src \
  -e BINANCE_APIKEY="${BINANCE_APIKEY}" \
  -e BINANCE_SECRET="${BINANCE_SECRET}" \
  -e RABBITMQ_ERLANG_COOKIE="${RABBITMQ_ERLANG_COOKIE}" \
  -e ENDPOINT="$2" \
  python:3.6.5 sh -c 'cd /usr/src; pip install --quiet --no-cache-dir -r requirements.txt && python main.py'
