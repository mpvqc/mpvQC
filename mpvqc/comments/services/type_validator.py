# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from PySide6.QtCore import QCoreApplication

from .translator import reverse_translate_comment_type

_FORBIDDEN_CHARACTERS = "[]"
_FORBIDDEN_CHARACTERS_PATTERN = re.compile(f"[{re.escape(_FORBIDDEN_CHARACTERS)}]")


def validate_new_comment_type(new_comment_type: str, existing_comment_types: list[str]) -> str | None:
    if not new_comment_type:
        return QCoreApplication.translate("CommentTypesDialog", "A comment type must not be blank")
    if _FORBIDDEN_CHARACTERS_PATTERN.search(new_comment_type):
        message = QCoreApplication.translate("CommentTypesDialog", "Characters '{}' not allowed")
        return message.format(_FORBIDDEN_CHARACTERS)
    if _already_exists(new_comment_type, existing_comment_types):
        return QCoreApplication.translate("CommentTypesDialog", "Comment type already exists")
    return None


def _already_exists(new_comment_type: str, existing_comment_types: list[str]) -> bool:
    translated = reverse_translate_comment_type(new_comment_type)
    return new_comment_type in existing_comment_types or translated in existing_comment_types
