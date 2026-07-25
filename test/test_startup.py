# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import time

from mpvqc.startup import log_startup_time


def test_startup_time_logged_at_info(caplog):
    with caplog.at_level(logging.INFO):
        log_startup_time(time.perf_counter() - 0.5)

    [record] = [r for r in caplog.records if "Startup took" in r.getMessage()]
    assert record.levelno == logging.INFO
    assert record.args[0] >= 500
