# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
    binder.bind_to_constructor(s.ImporterService, lambda: s.ImporterService())
    binder.bind_to_constructor(s.InternationalizationService, lambda: s.InternationalizationService())
    binder.bind_to_constructor(s.KeyCommandGeneratorService, lambda: s.KeyCommandGeneratorService())
    binder.bind_to_constructor(s.LabelWidthCalculatorService, lambda: s.LabelWidthCalculatorService())
    binder.bind_to_constructor(s.MimetypeProviderService, lambda: s.MimetypeProviderService())
    binder.bind_to_constructor(s.OperatingSystemZoomDetectorService, lambda: s.OperatingSystemZoomDetectorService())
    binder.bind_to_constructor(s.PlayerService, lambda: s.PlayerService())
    binder.bind_to_constructor(s.ResourceReaderService, lambda: s.ResourceReaderService())
    binder.bind_to_constructor(s.ResourceService, lambda: s.ResourceService())
    binder.bind_to_constructor(s.ReverseTranslatorService, lambda: s.ReverseTranslatorService())
    binder.bind_to_constructor(s.SettingsService, lambda: s.SettingsService())
    binder.bind_to_constructor(s.StateService, lambda: s.StateService())
    binder.bind_to_constructor(s.SubtitleImporterService, lambda: s.SubtitleImporterService())
    binder.bind_to_constructor(s.ThemeService, lambda: s.ThemeService())
    binder.bind_to_constructor(s.TimeFormatterService, lambda: s.TimeFormatterService())
    binder.bind_to_constructor(s.TypeMapperService, lambda: s.TypeMapperService())
    binder.bind_to_constructor(s.VersionCheckerService, lambda: s.VersionCheckerService())
    binder.bind_to_constructor(s.VideoSelectorService, lambda: s.VideoSelectorService())


def configure_injections():
    inject.configure(bindings, bind_in_runtime=False, clear=True)
