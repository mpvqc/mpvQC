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
    rejected_paths = [r.path for r in result.rejected_documents]
    assert rejected_paths == [document_invalid_1, document_invalid_2]


def test_import_unreadable_documents(
    document_with_invalid_encoding,
    document_missing,
):
    result = read_documents([document_with_invalid_encoding, document_missing])

    assert not result.valid_documents
    rejected_paths = [r.path for r in result.rejected_documents]
    assert document_with_invalid_encoding in rejected_paths
    assert document_missing in rejected_paths


def test_import_documents_with_utf8_bom(tmp_path):
    classic = tmp_path / "classic.txt"
    classic.write_text("[FILE]\n\n[DATA]\n[00:00:10] [Translation] first\n", encoding="utf-8-sig")
    v1 = tmp_path / "document.json"
    v1.write_text('{"version": 1, "comments": []}', encoding="utf-8-sig")

    result = read_documents([classic, v1])

    assert set(result.valid_documents) == {classic, v1}
    assert result.rejected_documents == ()
