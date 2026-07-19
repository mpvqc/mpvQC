# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from PySide6.QtCore import QObject, Qt, Signal, Slot

if TYPE_CHECKING:
    from collections.abc import Callable

type Handler[**P] = Callable[P, None]


class Event(NamedTuple):
    handler: Handler[...]
    args: tuple
    kwargs: dict

    def dispatch(self) -> None:
        self.handler(*self.args, **self.kwargs)


class EventMarshal(QObject):
    """Carries event streams from foreign threads onto the GUI thread."""

    _posted = Signal(Event)

    def __init__(self) -> None:
        super().__init__()
        self._posted.connect(self._dispatch, Qt.ConnectionType.QueuedConnection)

    @Slot(Event)
    def _dispatch(self, event: Event) -> None:
        event.dispatch()

    def channel[**P](self, handler: Handler[P]) -> Handler[P]:
        """Returns a callable that runs the handler on the GUI thread, in post order."""

        def post(*args: P.args, **kwargs: P.kwargs) -> None:
            self._posted.emit(Event(handler, args, kwargs))

        return post
