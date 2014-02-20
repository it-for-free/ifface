#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/server
cd ./server
python3 ./iff-tornado.py
