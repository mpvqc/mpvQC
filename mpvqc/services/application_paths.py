# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QStandardPaths


class ApplicationEnvironment:
    def __init__(self, executing_directory: Path | None = None) -> None:
        self._executing_directory = executing_directory or Path(sys.argv[0]).parent

    @property
    def is_portable(self) -> bool:
        return self._executing_directory.joinpath("portable").is_file()

    @property
    def executing_directory(self) -> Path:
        return self._executing_directory


@dataclass(frozen=True)
class _Directories:
    backup: Path
    config: Path
    screenshots: Path
    export_templates: Path


def _portable_directories(executing_directory: Path) -> _Directories:
    return _Directories(
        backup=executing_directory / "appdata" / "backups",
        config=executing_directory / "appdata",
        screenshots=executing_directory / "appdata" / "screenshots",
        export_templates=executing_directory / "appdata" / "export-templates",
    )


def _xdg_directories() -> _Directories:
    appname = QCoreApplication.applicationName()
    config = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
    return _Directories(
        backup=Path(config) / appname / "backups",
        config=Path(config) / appname,
        screenshots=Path(config) / appname / "screenshots",
        export_templates=Path(config) / appname / "export-templates",
    )


def _resolve_directories(app: ApplicationEnvironment) -> _Directories:
    if app.is_portable:
        return _portable_directories(app.executing_directory)
    return _xdg_directories()


class ApplicationPathsService:
    def __init__(self, app_environment: ApplicationEnvironment | None = None) -> None:
        app = ApplicationEnvironment() if app_environment is None else app_environment
        self._dirs = _resolve_directories(app)

    @property
    def dir_backup(self) -> Path:
        return self._dirs.backup

    @property
    def dir_config(self) -> Path:
        return self._dirs.config

    @property
    def dir_screenshots(self) -> Path:
        return self._dirs.screenshots

    @property
    def dir_export_templates(self) -> Path:
        return self._dirs.export_templates

    @property
    def file_input_conf(self) -> Path:
        return self.dir_config / "input.conf"

    @property
    def file_mpv_conf(self) -> Path:
        return self.dir_config / "mpv.conf"

    @property
    def file_settings(self) -> Path:
        return self.dir_config / "settings.ini"

    @property
    def files_export_templates(self) -> tuple[Path, ...]:
        return tuple(self.dir_export_templates.glob("*.jinja"))
