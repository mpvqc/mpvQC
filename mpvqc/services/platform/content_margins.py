# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Protocol


class ContentMarginsApplier(Protocol):
    def apply_content_margins(self, margin: int) -> None: ...


class NoContentMarginsApplier:
    """For platforms whose window content never reserves margins."""

    def apply_content_margins(self, margin: int) -> None:
        pass
