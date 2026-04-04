# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .application_paths import ApplicationPathsService as ApplicationPathsService
from .build_info import BuildInfoService as BuildInfoService
from .comment_type_validator import CommentTypeValidatorService as CommentTypeValidatorService
from .comments import CommentsService as CommentsService
from .document_exporter import DocumentBackupService as DocumentBackupService
from .document_exporter import DocumentExportService as DocumentExportService
from .document_exporter import DocumentRenderService as DocumentRenderService
from .document_importer import DocumentImporterService as DocumentImporterService
from .exporter import ExportService as ExportService
from .file_startup import FileStartupService as FileStartupService
from .font_loader import FontLoaderService as FontLoaderService
from .formatter_time import TimeFormatterService as TimeFormatterService
from .frameless import FramelessWindowService as FramelessWindowService
from .frameless import get_frameless_window_service as get_frameless_window_service
from .host_integration import HostIntegrationService as HostIntegrationService
from .host_integration import WindowButtonPreference as WindowButtonPreference
from .i18n import InternationalizationService as InternationalizationService
from .importer import ImporterService as ImporterService
from .key_command import KeyCommandGeneratorService as KeyCommandGeneratorService
from .label_width_calculator import LabelWidthCalculatorService as LabelWidthCalculatorService
from .main_window import MainWindowService as MainWindowService
from .mimetype_provider import MimetypeProviderService as MimetypeProviderService
from .player import PlayerService as PlayerService
from .quit import QuitService as QuitService
from .resetter import ResetService as ResetService
from .resource import ResourceService as ResourceService
from .reverse_translator import ReverseTranslatorService as ReverseTranslatorService
from .settings import SettingsService as SettingsService
from .state import StateService as StateService
from .subtitle_importer import SubtitleImporterService as SubtitleImporterService
from .theme import ThemeService as ThemeService
from .type_mapper import TypeMapperService as TypeMapperService
from .version_checker import VersionCheckerService as VersionCheckerService
from .window_properties import WindowPropertiesService as WindowPropertiesService
