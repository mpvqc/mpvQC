# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re

import inject
from PySide6.QtCore import QCoreApplication

from .reverse_translator import ReverseTranslatorService


class CommentTypeValidatorService:
    _reverse_translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)

    _forbidden_characters = re.compile(r"[\[\]]")

    def validate_new_comment_type(self, new_comment_type: str, existing_comment_types: list[str]) -> str | None:
        if not new_comment_type:
            return self._must_not_be_blank()
        if self._contains_forbidden_characters(new_comment_type):
            return self._must_not_contain_forbidden_characters()
        if self._already_exists(new_comment_type, existing_comment_types):
            return self._must_not_already_exist()
        return None

    def _contains_forbidden_characters(self, new_comment_type: str) -> bool:
        return bool(self._forbidden_characters.search(new_comment_type))

    def _already_exists(self, new_comment_type: str, existing_comment_types: list[str]):
        translated = self._reverse_translator.lookup(new_comment_type)
        return new_comment_type in existing_comment_types or translated in existing_comment_types

    def validate_editing_of_comment_type(
        self, new_comment_type: str, comment_type_being_edited: str, existing_comment_types: list[str]
    ):
        if not new_comment_type:
            return self._must_not_be_blank()
        if self._contains_forbidden_characters(new_comment_type):
            return self._must_not_contain_forbidden_characters()

        comment_types = existing_comment_types.copy()
        if (translated := self._reverse_translator.lookup(comment_type_being_edited)) in comment_types:
            comment_types.remove(translated)
        if self._already_exists(new_comment_type, comment_types):
            return self._must_not_already_exist()

        return None

    @staticmethod
    def _must_not_be_blank():
        return QCoreApplication.translate("CommentTypesDialog", "A comment type must not be blank")

    @staticmethod
    def _must_not_contain_forbidden_characters():
        return QCoreApplication.translate("CommentTypesDialog", "Characters '{}' not allowed").format("[]")

    @staticmethod
    def _must_not_already_exist():
        return QCoreApplication.translate("CommentTypesDialog", "Comment type already exists")
