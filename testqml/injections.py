# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Literal, NamedTuple, override

import inject
from PySide6.QtCore import QSettings, QUrl
from PySide6.QtGui import QGuiApplication

from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.exporting.services import ExportService, ExportSettingsService
from mpvqc.exporting.viewmodels import MpvqcExportBackupTimerViewModel
from mpvqc.importing.services import ImportSettingsService
from mpvqc.injections import bindings as original_bindings
from mpvqc.player.services import PlayerService
from mpvqc.shell.services import CheckOutcome, DesktopService, UpToDate, VersionCheckerService
from mpvqc.window.services import (
    MainWindowService,
    NoEmbeddedPlayerTracker,
    NoSurfaceHandler,
    NoWindowConfigurator,
    NoWindowRevealer,
    PlatformBackend,
    PlatformCapabilities,
    PlatformService,
    QtWindowStateHandler,
    ResizeResult,
    StaticWindowButtons,
    VideoResizeService,
    ViewDimensions,
    linux_desktop_capabilities,
    linux_tiling_capabilities,
    windows_capabilities,
)
from test.player.recording import RecordingPlayerHandle


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


def _platform_capabilities(name: str) -> PlatformCapabilities:
    match name:
        case "windows":
            return windows_capabilities()
        case "linux-desktop":
            return linux_desktop_capabilities()
        case "linux-tiling" | "headless":
            return linux_tiling_capabilities()
        case _:
            msg = f"Unknown platform: {name!r}"
            raise ValueError(msg)


def _headless_platform_backend(capabilities: PlatformCapabilities) -> PlatformBackend:
    return PlatformBackend(
        capabilities=capabilities,
        window_state=QtWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=StaticWindowButtons(),
    )


class _CurrentPlatform:
    def __init__(self) -> None:
        self._service: PlatformService | None = None

    def switch(self, name: str) -> None:
        self._service = PlatformService(_headless_platform_backend(_platform_capabilities(name)))

    def service(self) -> PlatformService:
        if (service := self._service) is None:
            msg = "No platform switched in yet: configure_injections() must run first"
            raise RuntimeError(msg)
        return service


current_platform = _CurrentPlatform()


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


class InstantLoadPlayerHandle(RecordingPlayerHandle):
    @override
    def command(self, name: str, *args: object) -> None:
        super().command(name, *args)
        if name == "loadfile":
            path = str(args[0])
            self.push_property("path", path)
            self.push_property("filename", Path(path).name)
            self.push_file_loaded()


class RecordedPlayer(NamedTuple):
    """The service and the handle it is built over, as one: a push through the handle reaches
    nothing until the service has registered its observers."""

    handle: InstantLoadPlayerHandle
    service: PlayerService


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
    def open_url(self, url: QUrl) -> None:
        self.opened_urls.append(url)


def _export_settings_service_override() -> ExportSettingsServiceOverride:
    return ExportSettingsServiceOverride(inject.instance(QSettings))


def _import_settings_service_override() -> ImportSettingsServiceOverride:
    return ImportSettingsServiceOverride(inject.instance(QSettings))


def _recorded_player() -> RecordedPlayer:
    handle = InstantLoadPlayerHandle()
    return RecordedPlayer(handle=handle, service=PlayerService(handle))


def _player_service() -> PlayerService:
    return inject.instance(RecordedPlayer).service


def configure_injections() -> None:
    MpvqcExportBackupTimerViewModel.MIN_INTERVAL_MS = 50

    current_platform.switch("windows" if sys.platform == "win32" else "headless")

    def test_bindings(binder: inject.Binder) -> None:
        original_bindings(binder)
        binder.bind_to_constructor(ApplicationPathsService, ApplicationPathsServiceOverride)
        binder.bind_to_constructor(DesktopService, DesktopServiceOverride)
        binder.bind_to_constructor(ExportService, ExportServiceOverride)
        binder.bind_to_constructor(ExportSettingsService, _export_settings_service_override)
        binder.bind_to_constructor(ImportSettingsService, _import_settings_service_override)
        binder.bind_to_provider(PlatformService, current_platform.service)
        binder.bind_to_constructor(RecordedPlayer, _recorded_player)
        binder.bind_to_constructor(PlayerService, _player_service)
        binder.bind_to_constructor(VersionCheckerService, VersionCheckerServiceOverride)
        binder.bind_to_constructor(VideoResizeService, VideoResizeServiceOverride)

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)


def rebind_main_window() -> None:
    # The Quick Test runner owns the engine; its first window hosts the TestCase.
    test_window = QGuiApplication.topLevelWindows()[0]
    inject.instance(MainWindowService).initialize(test_window)
