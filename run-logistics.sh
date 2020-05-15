#!/bin/bash

cd examples/logistics

mkdir -p logs
mkdir -p db

echo "Starting merchant..."
python merchant_agent.py &>logs/merchant.log &

echo "Starting labeler..."
python labeler_agent.py &>logs/labeler.log &

echo "Starting wrapper..."
python wrapper_agent.py &>logs/wrapper.log &

echo "Starting packer..."
python packer_agent.py &>logs/packer.log &

echo "Press Ctrl-D to terminate servers..."
cat >/dev/null
