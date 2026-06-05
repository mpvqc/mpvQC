# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.services.importer.reader import read_documents


def test_import_invalid_documents(
    document_invalid_1,
    document_invalid_2,
):
    result = read_documents([document_invalid_1, document_invalid_2])

    assert not result.valid_documents
    assert len(result.invalid_documents) == 2
    assert document_invalid_1 in result.invalid_documents
    assert document_invalid_2 in result.invalid_documents


def test_import_unreadable_documents(
    document_with_invalid_encoding,
    document_missing,
):
    result = read_documents([document_with_invalid_encoding, document_missing])

    assert not result.valid_documents
    assert document_with_invalid_encoding in result.invalid_documents
    assert document_missing in result.invalid_documents
