# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from typing import Any, Protocol

logger = logging.getLogger(__name__)


class CommentsProvider(Protocol):
    def comments(self) -> list[dict[str, Any]]: ...


class CommentsService:
    def __init__(self) -> None:
        self._provider: CommentsProvider | None = None

    def initialize(self, provider: CommentsProvider) -> None:
        logger.debug("Registering comments provider: %s", provider)
        self._provider = provider

    def comments(self) -> list[dict[str, Any]]:
        if self._provider is None:
            msg = "CommentsService: provider has not been initialized"
            raise RuntimeError(msg)
        return self._provider.comments()
