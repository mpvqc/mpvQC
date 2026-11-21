# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .desktop import DesktopService as DesktopService
from .quit import QuitService as QuitService
from .settings import ShellSettingsService as ShellSettingsService
from .version_checker import HOME_URL as HOME_URL
from .version_checker import CheckOutcome as CheckOutcome
from .version_checker import NewVersionAvailable as NewVersionAvailable
from .version_checker import ServerError as ServerError
from .version_checker import ServerNotReachable as ServerNotReachable
from .version_checker import UpToDate as UpToDate
from .version_checker import VersionCheckerService as VersionCheckerService
from .video_resize import ResizeResult as ResizeResult
from .video_resize import VideoResizeService as VideoResizeService
from .video_resize import ViewDimensions as ViewDimensions
from .video_resize import calculate_horizontal_layout_sizes as calculate_horizontal_layout_sizes
from .video_resize import calculate_vertical_layout_sizes as calculate_vertical_layout_sizes
from .vocabulary import TimeDisplayMode as TimeDisplayMode
from .vocabulary import WindowTitleFormat as WindowTitleFormat
