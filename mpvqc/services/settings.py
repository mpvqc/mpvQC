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


MISSING = object()


class SettingsOwner(Protocol):
    @property
    def qsettings(self) -> QSettings: ...


class Setting[Owner: SettingsOwner, T]:
    def __init__(
        self,
        key: str,
        *,
        default: Callable[[], T],
        decode: Callable[[object, Callable[[], T]], T],
        read: Callable[[QSettings, str], object] = lambda store, key: store.value(key),
        encode: Callable[[T], object] = lambda value: value,
        notify: Callable[[Owner, T], None] | None = None,
    ) -> None:
        self.key = key
        self._default = default
        self._decode = decode
        self._read = read
        self._encode = encode
        self._notify = notify

    @overload
    def __get__(self, instance: None, owner: type[Owner] | None = None) -> Setting[Owner, T]: ...

    @overload
    def __get__(self, instance: Owner, owner: type[Owner] | None = None) -> T: ...

    def __get__(self, instance: Owner | None, owner: type[Owner] | None = None) -> Setting[Owner, T] | T:
        if instance is None:
            return self
        stored = self._read(instance.qsettings, self.key) if instance.qsettings.contains(self.key) else MISSING
        return self._decode(stored, self._default)

    def __set__(self, instance: Owner, value: T) -> None:
        if self._notify is not None and self.__get__(instance) == value:
            return
        instance.qsettings.setValue(self.key, self._encode(value))
        if self._notify is not None:
            self._notify(instance, value)


def stored_text(store: QSettings, key: str) -> object:
    return store.value(key, type=str)


# A later run reads INI text, not the native value QSettings caches for its writer.
def read_bool(stored: object, default: Callable[[], bool]) -> bool:
    if isinstance(stored, bool):
        return stored
    if isinstance(stored, str) and stored.lower() in {"true", "false"}:
        return stored.lower() == "true"
    return default()


def read_int(stored: object, default: Callable[[], int]) -> int:
    if isinstance(stored, bool):
        return default()
    if isinstance(stored, int):
        return stored
    if isinstance(stored, str):
        with suppress(ValueError):
            return int(stored)
    return default()


def read_member[M: IntEnum](stored: object, of: type[M], default: Callable[[], M]) -> M:
    # QSettings' type=int coercion turns corrupt text into 0, which may name a valid member.
    with suppress(ValueError):
        return of(read_int(stored, lambda: default().value))
    return default()
