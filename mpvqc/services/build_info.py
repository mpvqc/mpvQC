# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.build import Dependency, get_build_info


class BuildInfoService:
    def __init__(self):
        self._build_info = get_build_info()

    @property
    def name(self) -> str:
        return self._build_info.application.name

    @property
    def organization(self) -> str:
        return self._build_info.application.organization

    @property
    def domain(self) -> str:
        return self._build_info.application.domain

    @property
    def version(self) -> str:
        return self._build_info.application.version

    @property
    def commit(self) -> str:
        return self._build_info.application.commit

    @property
    def build_date(self) -> str:
        return self._build_info.application.build_date

    @property
    def is_release(self) -> bool:
        return self._build_info.application.is_release

    @property
    def dependencies(self) -> tuple[Dependency, ...]:
        return self._build_info.dependencies

    @property
    def dev_dependencies(self) -> tuple[Dependency, ...]:
        return self._build_info.dev_dependencies

    @property
    def combined_version_info(self) -> str:
        if self.is_release:
            return f"{self.version} - {self.commit}"
        return f"dev build - {self.commit}"
