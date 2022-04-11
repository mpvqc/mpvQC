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


import configparser
import io


class BuildInfoExtractor:
    SECTION = 'build_info'
    TAG = 'tag'
    COMMIT_ID = 'commit'

    def __init__(self):
        self._parser = configparser.ConfigParser()

    @property
    def tag(self):
        return self._parser.get(section=self.SECTION, option=self.TAG)

    @property
    def commit_id(self):
        return self._parser.get(section=self.SECTION, option=self.COMMIT_ID)

    def extract_from(self, configuration_file_content: str) -> None:
        buffer = io.StringIO(configuration_file_content)
        self._parser.read_file(buffer)
