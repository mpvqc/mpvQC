# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from test.player.recording import RecordingPlayerHandle


def test_a_pushed_failed_load_reaches_its_observer():
    failed_loads: list[None] = []
    handle = RecordingPlayerHandle()
    handle.on_file_load_failed(lambda: failed_loads.append(None))

    handle.push_file_load_failed()

    assert len(failed_loads) == 1


def test_a_failed_load_nothing_observes_is_refused():
    handle = RecordingPlayerHandle()

    with pytest.raises(RuntimeError, match="Nothing observes"):
        handle.push_file_load_failed()
