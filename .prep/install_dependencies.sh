#!/bin/bash

sudo apt-get install python3-pip libffi-dev build-essential  -y  --no-install-recommends && \
python3 -m pip install --upgrade pip setuptools wheel && \
python3 -m pip install poetry && \
python3 -m poetry install --no-dev
