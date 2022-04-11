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


from PySide6.QtCore import QFile, QIODevice


class ResourceFileReader:

    def read_from(self, file_path: str):
        resource_path = self._make_resource_path_from(file_path)
        return self._read_from(resource_path)

    @staticmethod
    def _make_resource_path_from(file_path: str) -> str:
        if file_path.startswith(':/'):
            return file_path
        if file_path.startswith('/'):
            return ':' + file_path
        return ':/' + file_path

    @staticmethod
    def _read_from(resource_path: str) -> str:
        file = QFile(resource_path)

        # noinspection PyBroadException
        try:
            opened = file.open(QIODevice.ReadOnly)
            if not opened:
                raise FileNotFoundError()
            return file.readAll().data().decode('utf-8')
        except FileNotFoundError:
            # todo logger
            print(f"Can not find resource file '{resource_path}'")
            raise
        except Exception:
            # todo logger
            print(f"Can not read resource file '{resource_path}'")
            raise
        finally:
            if file:
                file.close()
