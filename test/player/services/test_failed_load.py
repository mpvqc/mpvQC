# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

import mpv
import pytest
from mpv import MpvEventEndFile

from mpvqc.player.services import MpvPlayerHandle

if TYPE_CHECKING:
    from collections.abc import Callable


class FakeMpv:
    def __init__(self) -> None:
        self.event_callbacks: dict[str, Callable] = {}

    def event_callback(self, *event_types: str) -> Callable[[Callable], Callable]:
        def register(callback: Callable) -> Callable:
            for event_type in event_types:
                self.event_callbacks[event_type] = callback
            return callback

        return register


@pytest.fixture
def fake_mpv(monkeypatch) -> FakeMpv:
    fake = FakeMpv()
    monkeypatch.setattr(mpv, "MPV", lambda **_args: fake)
    return fake


def end_file(reason: int) -> SimpleNamespace:
    return SimpleNamespace(data=MpvEventEndFile(reason=reason))


REASONS_THAT_ARE_NOT_A_FAILED_LOAD = {
    "eof": MpvEventEndFile.EOF,
    "restarted": MpvEventEndFile.RESTARTED,
    "aborted": MpvEventEndFile.ABORTED,
    "quit": MpvEventEndFile.QUIT,
    "redirect": MpvEventEndFile.REDIRECT,
}


def test_an_end_file_on_an_error_reports_a_failed_load(fake_mpv):
    failed_loads: list[None] = []
    handle = MpvPlayerHandle()
    handle.on_file_load_failed(lambda: failed_loads.append(None))
    handle.open({})

    fake_mpv.event_callbacks["end-file"](end_file(MpvEventEndFile.ERROR))

    assert len(failed_loads) == 1


@pytest.mark.parametrize(
    "reason",
    REASONS_THAT_ARE_NOT_A_FAILED_LOAD.values(),
    ids=REASONS_THAT_ARE_NOT_A_FAILED_LOAD.keys(),
)
def test_an_end_file_for_any_other_reason_is_not_a_failed_load(fake_mpv, reason):
    failed_loads: list[None] = []
    handle = MpvPlayerHandle()
    handle.on_file_load_failed(lambda: failed_loads.append(None))
    handle.open({})

    fake_mpv.event_callbacks["end-file"](end_file(reason))

    assert not failed_loads
