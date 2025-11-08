# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

import mpvqc.services as s


def bindings(binder: inject.Binder):
    binder.bind_to_constructor(s.ApplicationEnvironmentService, s.ApplicationEnvironmentService)
    binder.bind_to_constructor(s.ApplicationPathsService, s.ApplicationPathsService)
    binder.bind_to_constructor(s.BuildInfoService, s.BuildInfoService)
    binder.bind_to_constructor(s.CommentTypeValidatorService, s.CommentTypeValidatorService)
    binder.bind_to_constructor(s.DocumentBackupService, s.DocumentBackupService)
    binder.bind_to_constructor(s.DocumentExportService, s.DocumentExportService)
    binder.bind_to_constructor(s.DocumentImporterService, s.DocumentImporterService)
    binder.bind_to_constructor(s.DocumentRenderService, s.DocumentRenderService)
    binder.bind_to_constructor(s.ExportService, s.ExportService)
    binder.bind_to_constructor(s.FileStartupService, s.FileStartupService)
    binder.bind_to_constructor(s.FontLoaderService, s.FontLoaderService)
    binder.bind_to_constructor(s.FramelessWindowService, s.FramelessWindowService)
    binder.bind_to_constructor(s.HostIntegrationService, s.HostIntegrationService)
    binder.bind_to_constructor(s.ImporterService, s.ImporterService)
    binder.bind_to_constructor(s.InternationalizationService, s.InternationalizationService)
    binder.bind_to_constructor(s.KeyCommandGeneratorService, s.KeyCommandGeneratorService)
    binder.bind_to_constructor(s.LabelWidthCalculatorService, s.LabelWidthCalculatorService)
    binder.bind_to_constructor(s.MimetypeProviderService, s.MimetypeProviderService)
    binder.bind_to_constructor(s.PlayerService, s.PlayerService)
    binder.bind_to_constructor(s.QuitService, s.QuitService)
    binder.bind_to_constructor(s.ResetService, s.ResetService)
    binder.bind_to_constructor(s.ResourceReaderService, s.ResourceReaderService)
    binder.bind_to_constructor(s.ResourceService, s.ResourceService)
    binder.bind_to_constructor(s.ReverseTranslatorService, s.ReverseTranslatorService)
    binder.bind_to_constructor(s.SettingsService, s.SettingsService)
    binder.bind_to_constructor(s.StateService, s.StateService)
    binder.bind_to_constructor(s.SubtitleImporterService, s.SubtitleImporterService)
    binder.bind_to_constructor(s.ThemeService, s.ThemeService)
    binder.bind_to_constructor(s.TimeFormatterService, s.TimeFormatterService)
    binder.bind_to_constructor(s.TypeMapperService, s.TypeMapperService)
    binder.bind_to_constructor(s.VersionCheckerService, s.VersionCheckerService)
    binder.bind_to_constructor(s.WindowPropertiesService, s.WindowPropertiesService)


def configure_injections():
    inject.configure(bindings, bind_in_runtime=False, clear=True)
