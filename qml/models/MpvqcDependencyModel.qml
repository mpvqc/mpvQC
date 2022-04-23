/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick


ListModel {
    ListElement {
        name: "mpv"
        url: "https://mpv.io/"
        licence: "GPL-2.0+"
    }
    ListElement {
        name: "libmpv"
        url: "https://mpv.io/installation/"
        licence: "GPL-3.0"
    }
    ListElement {
        name: "python-mpv"
        url: "https://github.com/jaseg/python-mpv"
        licence: "AGPL-3.0"
    }
    ListElement {
        name: "PySide6"
        url: "https://wiki.qt.io/Qt_for_Python"
        licence: "LGPL-3.0"
    }
    ListElement {
        name: "python-inject"
        url: "https://github.com/ivankorobkov/python-inject"
        licence: "Apache-2.0"
    }
    ListElement {
        name: "material-design-icons"
        url: "https://github.com/google/material-design-icons"
        licence: "Apache-2.0"
    }
}
