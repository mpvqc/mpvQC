# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mpvqc.datamodels import Comment, SearchResult

logger = logging.getLogger(__name__)


class CommentsProvider(Protocol):
    def rowCount(self) -> int: ...
    def comments(self) -> list[dict[str, Any]]: ...
    def clear_comments(self) -> None: ...
    def import_comments(self, comments: Sequence[Comment]) -> None: ...
    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchResult: ...


class CommentsService:
    def __init__(self) -> None:
        self._provider: CommentsProvider | None = None

    @property
    def _registered_provider(self) -> CommentsProvider:
        if self._provider is None:
            msg = "CommentsProvider has not been registered"
            raise RuntimeError(msg)
        return self._provider

    def register(self, provider: CommentsProvider) -> None:
        logger.debug("Registering comments provider: %s", provider)
        self._provider = provider

    @property
    def count(self) -> int:
        return self._registered_provider.rowCount()

    def comments(self) -> list[dict[str, Any]]:
        return self._registered_provider.comments()

    def reset(self) -> None:
        self._registered_provider.clear_comments()

    def import_comments(self, comments: Sequence[Comment]) -> None:
        self._registered_provider.import_comments(comments)

    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchResult:
        return self._registered_provider.search(query, include_current_row=include_current_row, top_down=top_down)
