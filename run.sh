#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"
source ./binance.env
cd "src"
python3 main.py
