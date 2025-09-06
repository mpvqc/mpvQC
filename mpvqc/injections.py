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

import mpvqc.services as s


def bindings(binder: inject.Binder):
    binder.bind_to_constructor(s.ApplicationEnvironmentService, lambda: s.ApplicationEnvironmentService())
    binder.bind_to_constructor(s.ApplicationPathsService, lambda: s.ApplicationPathsService())
    binder.bind_to_constructor(s.CommentTypeValidatorService, lambda: s.CommentTypeValidatorService())
    binder.bind_to_constructor(s.DocumentBackupService, lambda: s.DocumentBackupService())
    binder.bind_to_constructor(s.DocumentExportService, lambda: s.DocumentExportService())
    binder.bind_to_constructor(s.DocumentImporterService, lambda: s.DocumentImporterService())
    binder.bind_to_constructor(s.DocumentRenderService, lambda: s.DocumentRenderService())
    binder.bind_to_constructor(s.FileStartupService, lambda: s.FileStartupService())
    binder.bind_to_constructor(s.FontLoaderService, lambda: s.FontLoaderService())
    binder.bind_to_constructor(s.FramelessWindowService, lambda: s.FramelessWindowService())
    binder.bind_to_constructor(s.InternationalizationService, lambda: s.InternationalizationService())
    binder.bind_to_constructor(s.KeyCommandGeneratorService, lambda: s.KeyCommandGeneratorService())
    binder.bind_to_constructor(s.MimetypeProviderService, lambda: s.MimetypeProviderService())
    binder.bind_to_constructor(s.OperatingSystemZoomDetectorService, lambda: s.OperatingSystemZoomDetectorService())
    binder.bind_to_constructor(s.PlayerService, lambda: s.PlayerService())
    binder.bind_to_constructor(s.ResourceReaderService, lambda: s.ResourceReaderService())
    binder.bind_to_constructor(s.ResourceService, lambda: s.ResourceService())
    binder.bind_to_constructor(s.ReverseTranslatorService, lambda: s.ReverseTranslatorService())
    binder.bind_to_constructor(s.SettingsService, lambda: s.SettingsService())
    binder.bind_to_constructor(s.TimeFormatterService, lambda: s.TimeFormatterService())
    binder.bind_to_constructor(s.TypeMapperService, lambda: s.TypeMapperService())
    binder.bind_to_constructor(s.VersionCheckerService, lambda: s.VersionCheckerService())


def configure_injections():
    inject.configure(bindings, bind_in_runtime=False, clear=True)
