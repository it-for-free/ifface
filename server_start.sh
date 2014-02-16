#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)+/server
python3 ./server/iff-tornado.py
