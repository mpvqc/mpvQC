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


import locale
from abc import abstractmethod
from os import environ
from typing import TypeVar, Generic

Type = TypeVar('Type')


class Default(Generic[Type]):

    @abstractmethod
    def get(self) -> Type:
        pass


class DefaultValue(Default):

    def __init__(self, value: any):
        self._value = value

    def get(self):
        return self._value


class DefaultLanguage(Default):

    def get(self) -> str:
        loc_default = locale.getdefaultlocale()[0]
        if loc_default.startswith("de"):
            return "de"
        if loc_default.startswith("es"):
            return "es"
        if loc_default.startswith("he"):
            return "he"
        if loc_default.startswith("it"):
            return "it"
        return "en"


class DefaultNickname(Default):

    def get(self) -> str:
        return environ.get("USERNAME") or environ.get('USER') or "nick"
