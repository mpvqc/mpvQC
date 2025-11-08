# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import tomllib
from dataclasses import dataclass
from functools import cache


@dataclass(frozen=True)
class ApplicationInfo:
    name: str
    organization: str
    domain: str
    version: str
    commit: str
    is_release: bool


@dataclass(frozen=True)
class Dependency:
    name: str
    package: str
    version: str
    url: str
    licence: str
    platforms: list[str]


@dataclass(frozen=True)
class BuildInfo:
    application: ApplicationInfo
    dependencies: tuple[Dependency, ...]
    dev_dependencies: tuple[Dependency, ...]


@cache
def get_build_info() -> BuildInfo:
    from PySide6.QtCore import QFile, QIODevice

    file = QFile(":/data/build-info.toml")
    if not file.open(QIODevice.OpenModeFlag.ReadOnly):
        msg = "Failed to open build-info.toml from resources"
        raise RuntimeError(msg)

    try:
        content = file.readAll().data().decode("utf-8")
    finally:
        file.close()

    current_platform = sys.platform

    data = tomllib.loads(content)
    app = data["application"]
    application_info = ApplicationInfo(
        name=app["name"],
        organization=app["organization"],
        domain=app["domain"],
        version=app["version"],
        commit=app["commit"],
        is_release=app["is_release"],
    )

    dependencies = [
        Dependency(
            name=dep["name"],
            package=dep["package"],
            version=dep["version"],
            url=dep["url"],
            licence=dep["licence"],
            platforms=dep["platforms"],
        )
        for dep in data["dependency"]
        if current_platform in dep["platforms"]
    ]

    dev_dependencies = [
        Dependency(
            name=dep["name"],
            package=dep["package"],
            version=dep["version"],
            url=dep["url"],
            licence=dep["licence"],
            platforms=dep["platforms"],
        )
        for dep in data["dev_dependency"]
        if current_platform in dep["platforms"]
    ]

    return BuildInfo(
        application=application_info,
        dependencies=tuple(dependencies),
        dev_dependencies=tuple(dev_dependencies),
    )
