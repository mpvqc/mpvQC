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

import inject

from mpvqc.services import ResourceService, ApplicationEnvironmentService, ApplicationPathsService, \
    DocumentBackupService, FileStartupService, PlayerService, ResourceReaderService, ReverseTranslatorService, \
    OperatingSystemZoomDetectorService, FontLoaderService, SettingsService, DocumentExportService, \
    DocumentRenderService


def bindings(binder: inject.Binder):
    binder.bind_to_constructor(ApplicationEnvironmentService, lambda: ApplicationEnvironmentService())
    binder.bind_to_constructor(ApplicationPathsService, lambda: ApplicationPathsService())
    binder.bind_to_constructor(DocumentBackupService, lambda: DocumentBackupService())
    binder.bind_to_constructor(DocumentExportService, lambda: DocumentExportService())
    binder.bind_to_constructor(DocumentRenderService, lambda: DocumentRenderService())
    binder.bind_to_constructor(FileStartupService, lambda: FileStartupService())
    binder.bind_to_constructor(FontLoaderService, lambda: FontLoaderService())
    binder.bind_to_constructor(PlayerService, lambda: PlayerService())
    binder.bind_to_constructor(ResourceService, lambda: ResourceService())
    binder.bind_to_constructor(ResourceReaderService, lambda: ResourceReaderService())
    binder.bind_to_constructor(ReverseTranslatorService, lambda: ReverseTranslatorService())
    binder.bind_to_constructor(OperatingSystemZoomDetectorService, lambda: OperatingSystemZoomDetectorService())
    binder.bind_to_constructor(SettingsService, lambda: SettingsService())


def configure_injections():
    inject.configure(bindings, bind_in_runtime=False)
