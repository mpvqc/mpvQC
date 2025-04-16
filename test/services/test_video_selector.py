# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import SettingsService, VideoSelectorService
from test.mocks import MockedMessageBox

CHOICE = SettingsService.ImportWhenVideoLinkedInDocument

EXISTING_1 = Path.home() / "Videos" / "some-existing-video-1.mp4"
EXISTING_2 = Path.home() / "Videos" / "some-existing-video-2.mp4"
EXISTING_3 = Path.home() / "Videos" / "some-existing-video-3.mp4"


@pytest.fixture(scope="module")
def service():
    return VideoSelectorService()


@pytest.fixture(scope="module")
def make_select_video(service):
    selected_video: Path | None = None

    def set_selected_video(video):
        nonlocal selected_video
        selected_video = video

    def get_selected_video() -> Path | None:
        return selected_video

    def _make_select_video(
        existing_videos_dropped: list[Path],
        existing_videos_from_documents: list[Path],
    ) -> Callable[[], Path | None]:
        service.select_video_from(
            on_video_selected=lambda video: set_selected_video(video),
            video_found_dialog_factory=MagicMock(),
            existing_videos_dropped=existing_videos_dropped,
            existing_videos_from_documents=existing_videos_from_documents,
        )

        return get_selected_video

    return _make_select_video


def mock_user_choice(choice: CHOICE):
    mock = MagicMock()
    mock.import_video_when_video_linked_in_document = choice

    def config(binder: inject.Binder):
        binder.bind(SettingsService, mock)

    inject.configure(config, clear=True)


@pytest.mark.parametrize(
    ("videos_dropped", "videos_from_documents", "expected"),
    [
        ([EXISTING_1], [], EXISTING_1),
        ([EXISTING_2, EXISTING_3, EXISTING_1], [], EXISTING_2),
    ],
)
def test_existing_video_dropped(make_select_video, expected, videos_dropped, videos_from_documents):
    video_getter = make_select_video(
        existing_videos_dropped=videos_dropped,
        existing_videos_from_documents=videos_from_documents,
    )
    assert video_getter() == expected


@pytest.mark.parametrize(
    ("videos_dropped", "videos_from_documents", "expected"),
    [
        ([EXISTING_1], [EXISTING_2], EXISTING_1),
        ([], [], None),
        ([], [EXISTING_2], None),
    ],
)
def test_user_never_wants_to_import_video(make_select_video, expected, videos_dropped, videos_from_documents):
    mock_user_choice(CHOICE.NEVER)
    video_getter = make_select_video(
        existing_videos_dropped=videos_dropped,
        existing_videos_from_documents=videos_from_documents,
    )
    assert video_getter() == expected


@pytest.mark.parametrize(
    ("videos_dropped", "videos_from_documents", "expected"),
    [
        ([EXISTING_1], [], EXISTING_1),
        ([], [], None),
        ([EXISTING_1], [EXISTING_2], EXISTING_1),
        ([], [EXISTING_3], EXISTING_3),
    ],
)
def test_user_always_wants_to_import_video(make_select_video, expected, videos_dropped, videos_from_documents):
    mock_user_choice(CHOICE.ALWAYS)
    video_getter = make_select_video(
        existing_videos_dropped=videos_dropped,
        existing_videos_from_documents=videos_from_documents,
    )
    assert video_getter() == expected


def test_user_will_be_asked(service, make_select_video):
    mock_user_choice(CHOICE.ASK_EVERY_TIME)
    video_getter = make_select_video(
        existing_videos_dropped=[EXISTING_1],
        existing_videos_from_documents=[EXISTING_2],
    )
    assert video_getter() == EXISTING_1

    #

    selected_video: Path | None = None

    def set_selected_video(video):
        nonlocal selected_video
        selected_video = video

    user_selection = MagicMock()
    user_selection.createObject.return_value = MockedMessageBox()
    service.select_video_from(
        existing_videos_dropped=[],
        existing_videos_from_documents=[EXISTING_3],
        on_video_selected=lambda video: set_selected_video(video),
        video_found_dialog_factory=user_selection,
    )
    user_selection.createObject.return_value.accepted.emit()
    assert selected_video == EXISTING_3

    #

    selected_video = None
    service.select_video_from(
        existing_videos_dropped=[],
        existing_videos_from_documents=[EXISTING_3],
        on_video_selected=lambda video: set_selected_video(video),
        video_found_dialog_factory=user_selection,
    )
    user_selection.createObject.return_value.rejected.emit()
    assert selected_video is None
