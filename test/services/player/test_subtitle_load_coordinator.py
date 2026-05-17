# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.services.player.coordinators import SubtitleLoadCoordinator

S1 = Path.home() / "one.srt"
S2 = Path.home() / "two.srt"
S3 = Path.home() / "three.srt"


def test_attach_or_queue_loads_directly_when_video_loaded() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.attach_or_queue((S1,), video_loaded=True)

    assert added == [(S1,)]
    coord.flush()
    assert added == [(S1,)]


def test_attach_or_queue_keeps_pending_when_no_video() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.attach_or_queue((S1,), video_loaded=False)

    assert added == []
    coord.flush()
    assert added == [(S1,)]


def test_attach_or_queue_no_op_for_empty_subtitles() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.attach_or_queue((), video_loaded=False)
    coord.attach_or_queue((), video_loaded=True)
    coord.flush()

    assert added == []


def test_queue_for_next_load_accumulates_across_calls() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.queue_for_next_load((S1,))
    coord.queue_for_next_load((S2,))
    coord.queue_for_next_load((S3,))
    coord.flush()

    assert added == [(S1, S2, S3)]


def test_queue_for_next_load_deduplicates() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.queue_for_next_load((S1, S2))
    coord.queue_for_next_load((S2, S3))
    coord.flush()

    assert added == [(S1, S2, S3)]


def test_flush_clears_pending() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.queue_for_next_load((S1,))
    coord.flush()
    coord.flush()

    assert added == [(S1,)]


def test_flush_without_pending_is_noop() -> None:
    added: list[tuple[Path, ...]] = []
    coord = SubtitleLoadCoordinator(on_add=added.append)

    coord.flush()

    assert added == []
