# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


@dataclass(frozen=True)
class Dependency:
    name: str
    package: str
    version: str
    url: str
    licence: str


@dataclass(frozen=True)
class BuildInfo:
    name: str
    app_id: str
    organization: str
    domain: str
    version: str
    commit: str
    is_release: bool
    origin: str
    offers_update_check: bool
    dependencies: tuple[Dependency, ...]
    dev_dependencies: tuple[Dependency, ...]

    @property
    def version_label(self) -> str:
        version = self.version if self.is_release else "dev build"
        return f"{version} ({self.commit}) {self.origin}"


@cache
def get_build_info() -> BuildInfo:
    from PySide6.QtCore import QFile, QIODevice

    file = QFile(":/data/build-info.toml")
    if not file.open(QIODevice.OpenModeFlag.ReadOnly):
        msg = "Failed to open build-info.toml from resources"
        raise RuntimeError(msg)

    try:
        content = bytes(file.readAll().data()).decode("utf-8")
    finally:
        file.close()

    data = tomllib.loads(content)
    app = data["application"]
    return BuildInfo(
        name=app["name"],
        app_id=app["app_id"],
        organization=app["organization"],
        domain=app["domain"],
        version=app["version"],
        commit=app["commit"],
        is_release=app["is_release"],
        origin=determine_build_origin(
            channel=app.get("channel", ""),
            app_id=app["app_id"],
            flatpak_id=os.environ.get("FLATPAK_ID"),
        ),
        offers_update_check=app.get("offers_update_check", False),
        dependencies=_read_dependencies(data["dependency"], platform=sys.platform),
        dev_dependencies=_read_dependencies(data["dev_dependency"], platform=sys.platform),
    )


def _read_dependencies(tables: list[dict[str, Any]], *, platform: str) -> tuple[Dependency, ...]:
    return tuple(
        Dependency(
            name=dep["name"],
            package=dep["package"],
            version=dep["version"],
            url=dep["url"],
            licence=dep["licence"],
        )
        for dep in tables
        if platform in dep["platforms"]
    )


def determine_build_origin(channel: str, app_id: str, flatpak_id: str | None) -> str:
    if not channel:
        return "unofficial"
    if flatpak_id is not None and flatpak_id != app_id:
        return "unofficial"
    return channel
