# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Any


class Immutable[T]:
    _obj: T

    def __init__(self, obj: T) -> None:
        object.__setattr__(self, "_obj", obj)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._obj, name)

    def __setattr__(self, name: str, value: Any) -> None:
        msg = f"Cannot set {name}={value!r} in immutable instance"
        raise AttributeError(msg)

    def __new__(cls, obj: T) -> T:  # type: ignore[misc]
        _ = obj  # Needed for type signature
        return object.__new__(cls)  # type: ignore[return-value]
