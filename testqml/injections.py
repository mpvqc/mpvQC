# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import shutil
import tempfile
import typing
from pathlib import Path

import inject
from PySide6.QtCore import QUrl

from mpvqc.injections import bindings as original_bindings
from mpvqc.services import (
    ApplicationPathsService,
    DesktopService,
    ExportService,
    HostIntegrationService,
    PlayerService,
    SettingsService,
    VersionCheckerService,
    VideoResizeService,
    WindowPropertiesService,
)
from mpvqc.services.application_paths import ApplicationEnvironment
from mpvqc.services.video_resize import ResizeResult, ViewDimensions

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEMP_ROOT = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
TEMP_SAVES_DIR = TEMP_ROOT / "saves"
TEMP_SAVES_DIR.mkdir()


class WindowPropertiesServiceOverride(WindowPropertiesService):
    def __init__(self) -> None:
        super().__init__(bind_window=False, width=1280, height=720)


class HostIntegrationServiceOverride(HostIntegrationService):
    def __init__(self) -> None:
        super().__init__(detect_configuration=False)


class ApplicationPathsServiceOverride(ApplicationPathsService):
    def __init__(self) -> None:
        base = Path(tempfile.mkdtemp(prefix="paths-", dir=str(TEMP_ROOT)))
        shutil.copytree(FIXTURES_DIR / "portable-root", base, dirs_exist_ok=True)
        super().__init__(ApplicationEnvironment(executing_directory=base))


class SettingsServiceOverride(SettingsService):
    def __init__(self) -> None:
        super().__init__()
        # pyrefly: ignore [missing-override-decorator]
        self.last_directory_documents = QUrl.fromLocalFile(str(FIXTURES_DIR))


class PlayerServiceOverride(PlayerService):
    def __init__(self) -> None:
        super().__init__()
        self.opened_video: Path | None = None
        self.opened_subtitles: tuple[Path, ...] = ()

    @typing.override
    def open_video(self, video: Path) -> None:
        self.opened_video = video

    @typing.override
    def is_video_loaded(self, video: Path) -> bool:
        return self.opened_video is not None and self.opened_video.resolve() == video.resolve()

    @typing.override
    def open_subtitles(self, subtitles: Iterable[Path]) -> None:
        self.opened_subtitles = tuple(subtitles)

    @typing.override
    def pause(self) -> None:
        pass

    @typing.override
    def move_mouse(self, x: int, y: int) -> None:
        pass

    @typing.override
    def press_key(self, command: str) -> None:
        pass

    @typing.override
    def press_mouse_left(self) -> None:
        pass

    @typing.override
    def release_mouse_left(self) -> None:
        pass

    @typing.override
    def press_mouse_middle(self) -> None:
        pass

    @typing.override
    def press_mouse_back(self) -> None:
        pass

    @typing.override
    def press_mouse_forward(self) -> None:
        pass

    @typing.override
    def scroll_up(self) -> None:
        pass

    @typing.override
    def scroll_down(self) -> None:
        pass


class ExportServiceOverride(ExportService):
    @typing.override
    def generate_file_path_proposal(self) -> Path:
        return TEMP_SAVES_DIR / "qc_proposal.txt"


class VideoResizeServiceOverride(VideoResizeService):
    @typing.override
    def compute_resize(self, dimensions: ViewDimensions) -> ResizeResult | None:
        return ResizeResult(window_width=800, window_height=600, table_width=200, table_height=200)


class VersionCheckerServiceOverride(VersionCheckerService):
    @typing.override
    def check_for_new_version(self) -> tuple[str, str]:
        return "stub-title", "stub-text"


class DesktopServiceOverride(DesktopService):
    def __init__(self) -> None:
        self.opened_urls: list[QUrl] = []

    @typing.override
    def open_app_data_folder(self) -> None:
        self.opened_urls.append(QUrl("mpvqc-test://app-data-folder"))

    @typing.override
    def open_backup_folder(self) -> None:
        self.opened_urls.append(QUrl("mpvqc-test://backup-folder"))

    @typing.override
    def open_url(self, url: QUrl) -> None:
        self.opened_urls.append(url)


def configure_injections() -> None:
    def test_bindings(binder: inject.Binder) -> None:
        original_bindings(binder)
        binder.bind_to_constructor(ApplicationPathsService, ApplicationPathsServiceOverride)
        binder.bind_to_constructor(DesktopService, DesktopServiceOverride)
        binder.bind_to_constructor(ExportService, ExportServiceOverride)
        binder.bind_to_constructor(HostIntegrationService, HostIntegrationServiceOverride)
        binder.bind_to_constructor(PlayerService, PlayerServiceOverride)
        binder.bind_to_constructor(SettingsService, SettingsServiceOverride)
        binder.bind_to_constructor(VersionCheckerService, VersionCheckerServiceOverride)
        binder.bind_to_constructor(VideoResizeService, VideoResizeServiceOverride)
        binder.bind_to_constructor(WindowPropertiesService, WindowPropertiesServiceOverride)

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)
