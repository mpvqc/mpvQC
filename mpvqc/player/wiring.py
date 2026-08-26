# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    from mpvqc.player.services import KeyCommandGeneratorService, MpvPlayerHandle, PlayerService

    def player_service() -> PlayerService:
        return PlayerService(MpvPlayerHandle())

    binder.bind_to_constructor(KeyCommandGeneratorService, KeyCommandGeneratorService)
    binder.bind_to_constructor(PlayerService, player_service)


def register_qml_types() -> None:
    import mpvqc.player.viewmodels  # ruff: ignore[unused-import]
    import mpvqc.player.views  # ruff: ignore[unused-import]
