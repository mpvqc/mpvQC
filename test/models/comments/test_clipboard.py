# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from mpvqc.datamodels import Comment


def test_copy_to_clipboard(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=[
            Comment(time=100, comment_type="Phrasing", comment="Comment Content 1"),
            Comment(time=200, comment_type="Translation", comment="Comment Content 2"),
            Comment(time=300, comment_type="Spelling", comment="Comment Content 3"),
        ],
        set_player_time=0,
    )

    assert model.get_clipboard_content(0) == "[00:01:40] [Phrasing] Comment Content 1"
    assert model.get_clipboard_content(1) == "[00:03:20] [Translation] Comment Content 2"
    assert model.get_clipboard_content(2) == "[00:05:00] [Spelling] Comment Content 3"
