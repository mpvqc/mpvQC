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


class SettingsService:
    """Access to all settings"""

    def __init__(self):
        import mpvqc.impl.settings as settings

        self._config_input = \
            settings.MpvqcInputConf()
        self._config_mpv = \
            settings.MpvqcMpvConf()

    #
    # Config input
    #

    @property
    def config_input(self) -> str:
        return self._config_input.get()

    @config_input.setter
    def config_input(self, value: str) -> None:
        self._config_input.set(value)

    #
    # Config mpv
    #

    @property
    def config_mpv(self) -> str:
        return self._config_mpv.get()

    @config_mpv.setter
    def config_mpv(self, value: str) -> None:
        self._config_mpv.set(value)
