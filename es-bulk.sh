#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
source ./binance.env

qsize=$(
  sudo docker run --rm --net crypto -e RABBITMQ_ERLANG_COOKIE=${RABBITMQ_ERLANG_COOKIE} \
    rabbitmq:3.7-management sh -c 'rabbitmqctl -n rabbit@my-rabbit -p /crypto list_queues' \
  | grep elasticsearch | awk '{print$2}')

if [[ ${qsize} -gt 1000 ]]; then
  sudo docker run --rm --net crypto -e RABBITMQ_ERLANG_COOKIE=${RABBITMQ_ERLANG_COOKIE} \
    --mount type=bind,src="$(pwd)"/src,dst=/usr/src \
    python:3.6.5 sh -c 'cd /usr/src; pip install --no-cache-dir --quiet -r requirements.txt && python bulk.py'
fi
