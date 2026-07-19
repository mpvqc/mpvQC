# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal, override

import inject
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication

from mpvqc.injections import bindings as original_bindings
from mpvqc.services import (
    ApplicationPathsService,
    DesktopService,
    ExportService,
    MainWindowService,
    PlatformService,
    PlayerService,
    SettingsService,
    VersionCheckerService,
    VideoResizeService,
)
from mpvqc.services.platform.backend import PlatformBackend
from mpvqc.services.platform.content_margins import NoContentMarginsApplier
from mpvqc.services.platform.embedded_player import NoEmbeddedPlayerTracker
from mpvqc.services.platform.fullscreen import QtFullscreenHandler
from mpvqc.services.platform.window_buttons import StaticWindowButtons
from mpvqc.services.platform.window_configuration import NoWindowConfigurator
from mpvqc.services.platform.window_reveal import NoWindowRevealer
from mpvqc.services.version_checker import CheckOutcome, UpToDate
from mpvqc.services.video_resize import ResizeResult, ViewDimensions
from mpvqc.viewmodels import MpvqcBackupTimerViewModel

if TYPE_CHECKING:
    from collections.abc import Iterable

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEMP_ROOT = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
TEMP_SAVES_DIR = TEMP_ROOT / "saves"
TEMP_SAVES_DIR.mkdir()


def _headless_platform_backend() -> PlatformBackend:
    return PlatformBackend(
        root_qml_url="qrc:/qt/qml/MpvqcApplicationLinux.qml",
        # Tests load bare components, not the shadowed shell, so there is no margin.
        draws_own_shadow=False,
        owns_window_geometry=False,
        fullscreen=QtFullscreenHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        content_margins=NoContentMarginsApplier(),
        window_buttons=StaticWindowButtons(),
    )


class PlatformServiceOverride(PlatformService):
    def __init__(self) -> None:
        super().__init__(_headless_platform_backend())


class ApplicationPathsServiceOverride(ApplicationPathsService):
    def __init__(self) -> None:
        base = Path(tempfile.mkdtemp(prefix="paths-", dir=str(TEMP_ROOT)))
        shutil.copytree(FIXTURES_DIR / "portable-root", base, dirs_exist_ok=True)
        super().__init__(base)


class SettingsServiceOverride(SettingsService):
    def __init__(self) -> None:
        super().__init__()
        # pyrefly: ignore [missing-override-decorator]
        self.last_directory_documents = QUrl.fromLocalFile(str(FIXTURES_DIR))
        # pyrefly: ignore [missing-override-decorator]
        self.backup_interval = 0


class PlayerServiceOverride(PlayerService):
    def __init__(self) -> None:
        super().__init__()
        self.opened_video: Path | None = None
        self.opened_subtitles: tuple[Path, ...] = ()

    @override
    def is_any_video_loaded(self, videos: Iterable[Path]) -> bool:
        if self.opened_video is None:
            return False
        current = self.opened_video.resolve()
        return any(current == video.resolve() for video in videos)

    @override
    def open_media(self, *, video: Path | None, subtitles: tuple[Path, ...]) -> None:
        if video is not None:
            self.opened_video = video
        if subtitles:
            self.opened_subtitles = subtitles

    @override
    def pause(self) -> None:
        pass

    @override
    def move_mouse(self, x: int, y: int) -> None:
        pass

    @override
    def press_key(self, command: str) -> None:
        pass

    @override
    def press_mouse_left(self) -> None:
        pass

    @override
    def release_mouse_left(self) -> None:
        pass

    @override
    def press_mouse_middle(self) -> None:
        pass

    @override
    def press_mouse_back(self) -> None:
        pass

    @override
    def press_mouse_forward(self) -> None:
        pass

    @override
    def scroll_up(self) -> None:
        pass

    @override
    def scroll_down(self) -> None:
        pass


class ExportServiceOverride(ExportService):
    def __init__(self) -> None:
        super().__init__()
        self.write_count = 0
        self.max_writes = 1

    @override
    def generate_file_path_proposal(self, suffix: Literal["json", "txt"]) -> Path:
        return TEMP_SAVES_DIR / f"qc_proposal.{suffix}"

    @override
    def backup(self) -> None:
        if self.write_count >= self.max_writes:
            return
        super().backup()
        self.write_count += 1


class VideoResizeServiceOverride(VideoResizeService):
    @override
    def compute_resize(self, dimensions: ViewDimensions) -> ResizeResult | None:
        return ResizeResult(window_width=800, window_height=600, table_width=200, table_height=200)


class VersionCheckerServiceOverride(VersionCheckerService):
    @override
    def check_for_new_version(self) -> CheckOutcome:
        return UpToDate()


class DesktopServiceOverride(DesktopService):
    def __init__(self) -> None:
        self.opened_urls: list[QUrl] = []

    @override
    def open_app_data_folder(self) -> None:
        self.opened_urls.append(QUrl("mpvqc-test://app-data-folder"))

    @override
    def open_backup_folder(self) -> None:
        self.opened_urls.append(QUrl("mpvqc-test://backup-folder"))

    @override
    def open_url(self, url: QUrl) -> None:
        self.opened_urls.append(url)


def configure_injections() -> None:
    MpvqcBackupTimerViewModel.MIN_INTERVAL_MS = 50

    def test_bindings(binder: inject.Binder) -> None:
        original_bindings(binder)
        binder.bind_to_constructor(ApplicationPathsService, ApplicationPathsServiceOverride)
        binder.bind_to_constructor(DesktopService, DesktopServiceOverride)
        binder.bind_to_constructor(ExportService, ExportServiceOverride)
        binder.bind_to_constructor(PlatformService, PlatformServiceOverride)
        binder.bind_to_constructor(PlayerService, PlayerServiceOverride)
        binder.bind_to_constructor(SettingsService, SettingsServiceOverride)
        binder.bind_to_constructor(VersionCheckerService, VersionCheckerServiceOverride)
        binder.bind_to_constructor(VideoResizeService, VideoResizeServiceOverride)

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)


def rebind_main_window() -> None:
    # The Quick Test runner owns the engine; its first window hosts the TestCase.
    test_window = QGuiApplication.topLevelWindows()[0]
    inject.instance(MainWindowService).initialize(test_window)
