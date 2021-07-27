#!/bin/sh -l

echo "Test"
echo "Running Krypto at dir $1"

poetry install --no-dev
poetry -V
pip install --upgrade pip


ls -l

pip install .
krypto run .
