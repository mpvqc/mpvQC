# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal, override

import inject
from PySide6.QtCore import QSettings, QUrl
from PySide6.QtGui import QGuiApplication

from mpvqc.exporting.services import ExportService, ExportSettingsService
from mpvqc.exporting.viewmodels import MpvqcExportBackupTimerViewModel
from mpvqc.importing.services import ImportSettingsService
from mpvqc.injections import bindings as original_bindings
from mpvqc.services import (
    ApplicationPathsService,
    DesktopService,
    PlayerService,
    SettingsFileService,
    VersionCheckerService,
    VideoResizeService,
)
from mpvqc.services.player.state import OBSERVED_PROPERTIES, make_observer
from mpvqc.services.version_checker import CheckOutcome, UpToDate
from mpvqc.services.video_resize import ResizeResult, ViewDimensions
from mpvqc.window.services import (
    MainWindowService,
    NoEmbeddedPlayerTracker,
    NoSurfaceHandler,
    NoWindowConfigurator,
    NoWindowRevealer,
    PlatformBackend,
    PlatformService,
    QtWindowStateHandler,
    StaticWindowButtons,
    linux_tiling_capabilities,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


def _temp_root() -> Path:
    # The parallel runner hands out the directories and deletes them once the processes are gone.
    configured = os.environ.get("MPVQC_TEST_TEMP_ROOT")
    if configured:
        root = Path(configured)
        root.mkdir(parents=True, exist_ok=True)
        return root
    return Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))


FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEMP_ROOT = _temp_root()
TEMP_SAVES_DIR = TEMP_ROOT / "saves"
TEMP_SAVES_DIR.mkdir()


def _headless_platform_backend() -> PlatformBackend:
    return PlatformBackend(
        capabilities=linux_tiling_capabilities(),
        window_state=QtWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
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


class ExportSettingsServiceOverride(ExportSettingsService):
    def __init__(self, qsettings: QSettings) -> None:
        super().__init__(qsettings)
        # pyrefly: ignore [missing-override-decorator]
        self.backup_interval = 0


class ImportSettingsServiceOverride(ImportSettingsService):
    def __init__(self, qsettings: QSettings) -> None:
        super().__init__(qsettings)
        self.last_directory_documents = QUrl.fromLocalFile(str(FIXTURES_DIR))


class PlayerServiceOverride(PlayerService):
    def __init__(self) -> None:
        super().__init__()
        self.opened_video: Path | None = None
        self.opened_subtitles: tuple[Path, ...] = ()
        self._observers = {spec.name: make_observer(spec, self._apply_property_update) for spec in OBSERVED_PROPERTIES}

    def load_video(
        self,
        path: str,
        *,
        duration: float,
        time_pos: float,
        time_remaining: float,
        percent_pos: float,
    ) -> None:
        for name, raw in (
            ("path", path),
            ("duration", duration),
            ("time-pos", time_pos),
            ("time-remaining", time_remaining),
            ("percent-pos", percent_pos),
        ):
            self._observers[name](name, raw)

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


def _export_settings_service_override() -> ExportSettingsServiceOverride:
    return ExportSettingsServiceOverride(inject.instance(SettingsFileService).qsettings)


def _import_settings_service_override() -> ImportSettingsServiceOverride:
    return ImportSettingsServiceOverride(inject.instance(SettingsFileService).qsettings)


def configure_injections() -> None:
    MpvqcExportBackupTimerViewModel.MIN_INTERVAL_MS = 50

    def test_bindings(binder: inject.Binder) -> None:
        original_bindings(binder)
        binder.bind_to_constructor(ApplicationPathsService, ApplicationPathsServiceOverride)
        binder.bind_to_constructor(DesktopService, DesktopServiceOverride)
        binder.bind_to_constructor(ExportService, ExportServiceOverride)
        binder.bind_to_constructor(ExportSettingsService, _export_settings_service_override)
        binder.bind_to_constructor(ImportSettingsService, _import_settings_service_override)
        binder.bind_to_constructor(PlatformService, PlatformServiceOverride)
        binder.bind_to_constructor(PlayerService, PlayerServiceOverride)
        binder.bind_to_constructor(VersionCheckerService, VersionCheckerServiceOverride)
        binder.bind_to_constructor(VideoResizeService, VideoResizeServiceOverride)

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)


def rebind_main_window() -> None:
    # The Quick Test runner owns the engine; its first window hosts the TestCase.
    test_window = QGuiApplication.topLevelWindows()[0]
    inject.instance(MainWindowService).initialize(test_window)
