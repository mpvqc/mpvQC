# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def test_import_invalid_documents(
    service,
    document_invalid_1,
    document_invalid_2,
):
    result = service.read([document_invalid_1, document_invalid_2])

    assert not result.valid_documents
    assert len(result.invalid_documents) == 2
    assert document_invalid_1 in result.invalid_documents
    assert document_invalid_2 in result.invalid_documents
