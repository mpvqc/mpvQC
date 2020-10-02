# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from typing import NamedTuple


class Metadata(NamedTuple):
    dir_program: str
    app_name: str
    app_version: str


class _Holder:
    md: Metadata


def get_metadata() -> Metadata:
    return _Holder.md


def set_metadata(dir_program: str, app_version: str, app_name: str):
    _Holder.md = Metadata(
        dir_program=dir_program,
        app_name=app_name,
        app_version=app_version
    )
