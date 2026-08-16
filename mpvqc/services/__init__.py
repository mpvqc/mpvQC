# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .application_paths import ApplicationPathsService as ApplicationPathsService
from .build_info import BuildInfoService as BuildInfoService
from .desktop import DesktopService as DesktopService
from .file_startup import FileStartupService as FileStartupService
from .font_loader import FontLoaderService as FontLoaderService
from .formatter_time import TimeFormatterService as TimeFormatterService
from .i18n import InternationalizationService as InternationalizationService
from .key_command import KeyCommandGeneratorService as KeyCommandGeneratorService
from .label_width_calculator import LabelWidthCalculatorService as LabelWidthCalculatorService
from .player import PlayerService as PlayerService
from .quit import QuitService as QuitService
from .resource import ResourceService as ResourceService
from .settings import SettingsService as SettingsService
from .settings_file import SettingsFileService as SettingsFileService
from .state import StateService as StateService
from .version_checker import VersionCheckerService as VersionCheckerService
from .video_resize import VideoResizeService as VideoResizeService
from .video_resize import ViewDimensions as ViewDimensions
