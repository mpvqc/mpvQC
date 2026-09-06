# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from contextlib import suppress
from enum import IntEnum
from typing import TYPE_CHECKING, Protocol, overload

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import QSettings


class SettingsOwner(Protocol):
    @property
    def qsettings(self) -> QSettings: ...


class Setting[Owner: SettingsOwner, T]:
    def __init__(
        self,
        key: str,
        *,
        default: Callable[[], T],
        decode: Callable[[object, T], T],
        encode: Callable[[T], object] = lambda value: value,
        notify: Callable[[Owner, T], None] | None = None,
    ) -> None:
        self.key = key
        self._default = default
        self._decode = decode
        self._encode = encode
        self._notify = notify

    @overload
    def __get__(self, instance: None, owner: type[Owner] | None = None) -> Setting[Owner, T]: ...

    @overload
    def __get__(self, instance: Owner, owner: type[Owner] | None = None) -> T: ...

    def __get__(self, instance: Owner | None, owner: type[Owner] | None = None) -> Setting[Owner, T] | T:
        if instance is None:
            return self
        return self._decode(instance.qsettings.value(self.key), self._default())

    def __set__(self, instance: Owner, value: T) -> None:
        if self._notify is not None and self.__get__(instance) == value:
            return
        instance.qsettings.setValue(self.key, self._encode(value))
        if self._notify is not None:
            self._notify(instance, value)


# A later run reads INI text, not the native value QSettings caches for its writer.
def read_bool(stored: object, default: bool) -> bool:
    if isinstance(stored, bool):
        return stored
    if isinstance(stored, str) and stored.lower() in {"true", "false"}:
        return stored.lower() == "true"
    return default


def read_int(stored: object, default: int) -> int:
    if isinstance(stored, bool):
        return default
    if isinstance(stored, int):
        return stored
    if isinstance(stored, str):
        with suppress(ValueError):
            return int(stored)
    return default


def read_member[M: IntEnum](stored: object, of: type[M], default: M) -> M:
    # QSettings' type=int coercion turns corrupt text into 0, which may name a valid member.
    with suppress(ValueError):
        return of(read_int(stored, default.value))
    return default
