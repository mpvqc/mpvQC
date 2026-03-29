# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


class CommentsService:
    def __init__(self) -> None:
        self._provider: Callable[[], list[dict[str, Any]]] | None = None

    def register(self, provider: Callable[[], list[dict[str, Any]]]) -> None:
        logger.debug("Registering comments provider: %s", provider)
        self._provider = provider

    def comments(self) -> list[dict[str, Any]]:
        if self._provider is None:
            logger.error("comments() called but no provider has been registered")
            return []
        return self._provider()
