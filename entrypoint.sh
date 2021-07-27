#!/bin/sh -l

echo "Test"
echo "Running Krypto at dir $1"

krypto run .

# poetry install --no-dev
# poetry -V

# poetry run krypto run .