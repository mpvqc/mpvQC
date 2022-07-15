/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import pyobjects


Item {
    id: current
    property alias configInput: configInput.file_content
    property alias configMpv: configMpv.file_content

    MpvqcFileInterfacePyObject {
        id: configInput
        file_path: MpvqcFilePathsPyObject.input_conf
    }

    MpvqcFileInterfacePyObject {
        id: configMpv
        file_path: MpvqcFilePathsPyObject.mpv_conf
    }

}
