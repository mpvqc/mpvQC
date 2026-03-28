# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.datamodels import Comment


def test_registers_with_comments_service_on_instantiation(make_model):
    comments = (
        Comment(time=1, comment_type="Type", comment="Hello"),
        Comment(time=2, comment_type="Type", comment="World"),
    )
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=comments)

    import inject

    from mpvqc.services import CommentsService

    service = inject.instance(CommentsService)
    assert service.comments() == model.comments()
