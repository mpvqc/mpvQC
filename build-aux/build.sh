#!/usr/bin/env bash

# Execute from repository root

source .venv/bin/activate

just clean
just build-develop
