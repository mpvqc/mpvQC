# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, Protocol

from PySide6.QtCore import QObject, QThreadPool, Signal, Slot

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class JobExecutor(Protocol):
    """Runs a callable off the GUI thread."""

    def execute(self, work: Callable[[], None]) -> None: ...


class ThreadPoolJobExecutor:
    def execute(self, work: Callable[[], None]) -> None:
        QThreadPool.globalInstance().start(work)


@dataclass(frozen=True)
class Ok[T]:
    value: T


@dataclass(frozen=True)
class Err:
    error: Exception


type Result[T] = Ok[T] | Err


@dataclass(frozen=True)
class _Job[T]:
    work: Callable[[], T]
    on_result: Callable[[Result[T]], None] | None

    def execute(self) -> partial[None]:
        try:
            outcome: Result[T] = Ok(self.work())
        except Exception as e:
            if self.on_result is None:
                logger.exception("Background job failed")
            outcome = Err(e)
        return partial(self._deliver, outcome)

    def _deliver(self, outcome: Result[T]) -> None:
        if self.on_result is not None:
            self.on_result(outcome)


def _deliver_abandoned() -> None:
    logger.critical("Background job interrupted before delivering a result")


class SerialJobRunner(QObject):
    _completed = Signal(partial)

    def __init__(self, executor: JobExecutor | None = None) -> None:
        super().__init__()
        self._executor = executor if executor is not None else ThreadPoolJobExecutor()
        self._queue: deque[_Job[Any]] = deque()
        self._current: _Job[Any] | None = None
        self._completed.connect(self._finish)

    def run[T](
        self,
        work: Callable[[], T],
        on_result: Callable[[Result[T]], None] | None = None,
    ) -> None:
        """Runs work off the GUI thread and calls on_result back on the GUI thread."""
        self._queue.append(_Job(work, on_result))
        if self._current is None:
            self._start_next()

    def _start_next(self) -> None:
        job = self._queue.popleft()
        self._current = job

        def _work() -> None:
            try:
                deliver = job.execute()
            except BaseException:
                self._completed.emit(partial(_deliver_abandoned))
                raise
            self._completed.emit(deliver)

        self._executor.execute(_work)

    @Slot(partial)
    def _finish(self, deliver: Callable[[], None]) -> None:
        try:
            deliver()
        finally:
            self._current = None
            if self._queue:
                self._start_next()
