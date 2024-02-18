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

from .application_environment import ApplicationEnvironmentService
from .application_paths import ApplicationPathsService
from .backup import BackupService
from .document_exporter import DocumentExporterService
from .file_startup import FileStartupService
from .font_loader import FontLoaderService
from .operating_system_zoom_detector import OperatingSystemZoomDetectorService
from .player import PlayerService, SubtitleCacher
from .resource import ResourceService
from .resource_reader import ResourceReaderService
from .reverse_translator import ReverseTranslatorService
from .settings import SettingsService
