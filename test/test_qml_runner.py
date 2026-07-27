# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from testqml.runner import count_tests, resolve_jobs


@pytest.mark.parametrize(
    ("requested", "shard_count", "platform", "expected"),
    [
        ("4", 51, "linux", 4),
        ("4", 2, "linux", 2),
        ("1", 51, "linux", 1),
        ("auto", 1, "linux", 1),
        ("4", 51, "win32", 1),
        ("auto", 51, "win32", 1),
    ],
)
def test_resolve_jobs(requested: str, shard_count: int, platform: str, expected: int):
    assert resolve_jobs(requested, shard_count, platform=platform) == expected


@pytest.mark.parametrize("requested", ["banana", "0", "-2", "", "2.5"])
def test_resolve_jobs_rejects(requested: str):
    with pytest.raises(SystemExit):
        resolve_jobs(requested, 51, platform="linux")


def test_count_tests_reads_totals():
    output = "PASS   : some::test()\nTotals: 38 passed, 1 failed, 0 skipped, 0 blacklisted, 6473ms\n"
    assert count_tests(output) == 38


def test_count_tests_without_totals():
    assert count_tests("qrc:/qt/qml/Foo.qml:3:1: Syntax error\n") == 0
