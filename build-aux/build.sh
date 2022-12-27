#!/usr/bin/env bash

# Execute from repository root

source venv/bin/activate

make develop-clean
make develop-build
