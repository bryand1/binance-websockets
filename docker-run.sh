#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
source ./binance.env

docker run -d --rm --net crypto --mount type=bind,src="$(pwd)"/src,dst=/usr/src \
  -e BINANCE_APIKEY="${BINANCE_APIKEY}" \
  -e BINANCE_SECRET="${BINANCE_SECRET}" \
  python:3.6.5 sh -c 'cd /usr/src; pip install --no-cache-dir -r requirements.txt && python main.py'
