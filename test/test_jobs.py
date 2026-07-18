# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from PySide6.QtCore import QThread, QThreadPool

from mpvqc.jobs import Err, Ok, SerialJobRunner

if TYPE_CHECKING:
    from mpvqc.jobs import Result
    from test.conftest import ManualJobExecutor


@pytest.fixture
def runner(manual_executor: ManualJobExecutor) -> SerialJobRunner:
    return SerialJobRunner(manual_executor)


def test_gives_the_executor_one_job_at_a_time(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
) -> None:
    events: list[str] = []

    for index in (1, 2, 3):
        runner.run(
            work=lambda i=index: events.append(f"work-{i}"),
            on_result=lambda _result, i=index: events.append(f"done-{i}"),
        )

    assert len(manual_executor.pending) == 1

    for expected_pending in (1, 1, 0):
        manual_executor.run_next()
        assert len(manual_executor.pending) == expected_pending

    assert events == ["work-1", "done-1", "work-2", "done-2", "work-3", "done-3"]


def test_on_result_receives_ok(runner: SerialJobRunner, manual_executor: ManualJobExecutor) -> None:
    received: list[Result[int]] = []

    runner.run(work=lambda: 42, on_result=received.append)
    manual_executor.drain()

    assert received == [Ok(42)]


def test_on_result_receives_err_and_the_next_job_still_runs(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
    caplog: pytest.LogCaptureFixture,
) -> None:
    events: list[object] = []
    failure = ValueError("job exploded")

    def failing_work() -> None:
        raise failure

    runner.run(work=failing_work, on_result=events.append)
    runner.run(work=lambda: None, on_result=lambda _result: events.append("done-2"))
    manual_executor.drain()

    assert events == [Err(failure), "done-2"]
    assert "Background job failed" not in caplog.text


def test_error_without_on_result_is_logged(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
    caplog: pytest.LogCaptureFixture,
) -> None:
    def failing_work() -> None:
        msg = "job exploded"
        raise ValueError(msg)

    runner.run(work=failing_work)
    manual_executor.drain()

    assert "Background job failed" in caplog.text


def test_on_result_can_add_a_new_job(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
) -> None:
    events: list[str] = []
    pending_during_delivery: list[int] = []

    def add_new_job(_result: Result[None]) -> None:
        events.append("done-1")
        runner.run(work=lambda: events.append("work-2"), on_result=lambda _r: events.append("done-2"))
        pending_during_delivery.append(len(manual_executor.pending))

    runner.run(work=lambda: events.append("work-1"), on_result=add_new_job)
    manual_executor.drain()

    assert events == ["work-1", "done-1", "work-2", "done-2"]
    assert pending_during_delivery == [0]


def test_error_in_on_result_does_not_stop_the_queue(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
) -> None:
    events: list[str] = []

    def raising_on_result(_result: Result[None]) -> None:
        msg = "on_result exploded"
        raise RuntimeError(msg)

    runner.run(work=lambda: None, on_result=raising_on_result)
    runner.run(work=lambda: events.append("work-2"), on_result=lambda _r: events.append("done-2"))
    manual_executor.drain()

    assert events == ["work-2", "done-2"]

    runner.run(work=lambda: events.append("work-3"))
    manual_executor.drain()

    assert events == ["work-2", "done-2", "work-3"]


def test_interrupt_in_work_does_not_stop_the_queue(
    runner: SerialJobRunner,
    manual_executor: ManualJobExecutor,
) -> None:
    events: list[str] = []

    def interrupted_work() -> None:
        raise KeyboardInterrupt

    runner.run(work=interrupted_work)
    runner.run(work=lambda: events.append("work-2"))

    with pytest.raises(KeyboardInterrupt):
        manual_executor.run_next()
    manual_executor.drain()

    assert events == ["work-2"]


def test_threadpool_executor_calls_on_result_on_the_gui_thread(qt_app) -> None:
    runner = SerialJobRunner()

    gui_thread = QThread.currentThread()
    work_threads: list[QThread] = []
    deliveries: list[tuple[Result[None], QThread]] = []

    def work() -> None:
        work_threads.append(QThread.currentThread())

    def failing_work() -> None:
        msg = "job exploded"
        raise ValueError(msg)

    def on_result(result: Result[None]) -> None:
        deliveries.append((result, QThread.currentThread()))

    runner.run(work, on_result)
    runner.run(failing_work, on_result)

    QThreadPool.globalInstance().waitForDone()
    qt_app.processEvents()
    QThreadPool.globalInstance().waitForDone()
    qt_app.processEvents()

    assert work_threads == [work_threads[0]]
    assert work_threads[0] is not gui_thread
    assert [type(result) for result, _thread in deliveries] == [Ok, Err]
    assert all(thread is gui_thread for _result, thread in deliveries)
