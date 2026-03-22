#!/usr/bin/env bash

# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

set -euo pipefail

find . -type f -name 'tst_*' -delete

just set-build-info

MPVQC_COMPILE_QML=true just build

find build/release -type d -name "__pycache__" -print0 | xargs -0 rm -rf
