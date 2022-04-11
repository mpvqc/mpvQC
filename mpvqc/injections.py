#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject

from mpvqc.impl import BuildInfoExtractor, ResourceFileReader, FileReader
from mpvqc.services import OsService, ResourceService, WindowIconService, BuildInfoService, AppEnvironmentService, \
    FileService, FileStartupService, SettingsService, SettingsInitializerService, TranslationService, PlayerService, \
    QcManagerService, TimeFormatterService


# noinspection DuplicatedCode
def bindings(binder: inject.Binder):
    # Services
    binder.bind_to_constructor(AppEnvironmentService, lambda: AppEnvironmentService())
    binder.bind_to_constructor(BuildInfoService, lambda: BuildInfoService())
    binder.bind_to_constructor(FileService, lambda: FileService())
    binder.bind_to_constructor(FileStartupService, lambda: FileStartupService())
    binder.bind_to_constructor(OsService, lambda: OsService())
    binder.bind_to_constructor(PlayerService, lambda: PlayerService())
    binder.bind_to_constructor(QcManagerService, lambda: QcManagerService())
    binder.bind_to_constructor(ResourceService, lambda: ResourceService())
    binder.bind_to_constructor(SettingsService, lambda: SettingsService())
    binder.bind_to_constructor(SettingsInitializerService, lambda: SettingsInitializerService())
    binder.bind_to_constructor(TimeFormatterService, lambda: TimeFormatterService())
    binder.bind_to_constructor(TranslationService, lambda: TranslationService())
    binder.bind_to_constructor(WindowIconService, lambda: WindowIconService())

    # Tasks
    binder.bind_to_constructor(BuildInfoExtractor, lambda: BuildInfoExtractor())
    binder.bind_to_constructor(FileReader, lambda: FileReader())
    binder.bind_to_constructor(ResourceFileReader, lambda: ResourceFileReader())


def configure_injections():
    inject.configure(bindings, bind_in_runtime=False)
