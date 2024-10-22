# mpvQC
#
# Copyright (C) 2024 mpvQC developers
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

from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

import inject

from mpvqc.services import TypeMapperService


@dataclass(frozen=True)
class ImportChange:
    documents: list[Path]
    video: Path or None

    @property
    def only_video_imported(self) -> bool:
        return self.video and not self.documents

    @property
    def exactly_one_document_imported(self) -> bool:
        return len(self.documents) == 1

    @property
    def imported_document(self) -> Path:
        return self.documents[0]


@dataclass(frozen=True)
class ApplicationState:
    document: Path or None
    video: Path or None
    saved: bool

    def find_video(self, change: ImportChange) -> Path or None:
        return change.video if change.video else self.video

    def handle_save(self, document: Path) -> "ApplicationState":
        return OtherState(document, self.video, saved=True)

    @abstractmethod
    def handle_import(self, change: ImportChange) -> "ApplicationState":
        pass

    def handle_change(self) -> "ApplicationState":
        return OtherState(self.document, self.video, saved=False)

    def handle_reset(self) -> "ApplicationState":
        return InitialState.new(video=self.video)


@dataclass(frozen=True)
class InitialState(ApplicationState):
    document = None
    video = None
    saved = True

    @classmethod
    def new(cls, video: Path or None = None):
        return cls(document=None, video=video, saved=True)

    def handle_import(self, change: ImportChange) -> ApplicationState:
        if change.only_video_imported:
            return InitialState.new(video=change.video)
        video = self.find_video(change)
        if change.exactly_one_document_imported:
            return OtherState(document=change.imported_document, video=video, saved=True)
        else:
            return OtherState(document=None, video=video, saved=False)


@dataclass(frozen=True)
class OtherState(ApplicationState):
    """"""

    def handle_import(self, change: ImportChange) -> ApplicationState:
        def imported_is_currently_loaded_video():
            mapper: TypeMapperService = inject.instance(TypeMapperService)
            imported = mapper.map_path_to_str(change.video)
            current = mapper.map_path_to_str(self.video)
            return imported == current

        if self.video and change.only_video_imported and imported_is_currently_loaded_video():
            return OtherState(document=self.document, video=self.video, saved=self.saved)
        else:
            return OtherState(document=None, video=self.find_video(change), saved=False)
