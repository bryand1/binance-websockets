#!/usr/bin/env bash

curl -XPUT localhost:9200/_template/logstash_template -H 'Content-Type: application/json' -d @logstash-template.json

