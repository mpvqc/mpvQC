# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from testqml.runner import count_tests, resolve_jobs


class ResolveJobsCase(NamedTuple):
    requested: str
    shard_count: int
    platform: str
    expected: int


@pytest.mark.parametrize(
    ("requested", "shard_count", "platform", "expected"),
    [
        ResolveJobsCase(requested="4", shard_count=51, platform="linux", expected=4),
        ResolveJobsCase(requested="4", shard_count=2, platform="linux", expected=2),
        ResolveJobsCase(requested="1", shard_count=51, platform="linux", expected=1),
        ResolveJobsCase(requested="auto", shard_count=1, platform="linux", expected=1),
        ResolveJobsCase(requested="4", shard_count=51, platform="win32", expected=1),
        ResolveJobsCase(requested="auto", shard_count=51, platform="win32", expected=1),
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
