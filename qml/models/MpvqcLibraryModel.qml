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


ListModel {
    ListElement {
        name: 'glfw'
        url: 'https://github.com/glfw/glfw'
        licence: 'Zlib'
        version: '@@pypi-glfw@@'
    }
    ListElement {
        name: 'Inject'
        url: 'https://github.com/ivankorobkov/python-inject'
        licence: 'Apache-2.0'
        version: '@@pypi-Inject@@'
    }
    ListElement {
        name: 'PyOpenGL'
        url: 'https://github.com/mcfletch/pyopengl'
        licence: 'PyOpenGL License'
        version: '@@pypi-PyOpenGL@@'
    }
    ListElement {
        name: 'PySide6'
        url: 'https://wiki.qt.io/Qt_for_Python'
        licence: 'LGPL-3.0'
        version: '@@pypi-PySide6@@'
    }
    ListElement {
        name: 'pytest'
        url: 'https://github.com/pytest-dev/pytest'
        licence: 'MIT'
        version: '@@pypi-pytest@@'
    }
    ListElement {
        name: 'python-mpv'
        url: 'https://github.com/jaseg/python-mpv'
        licence: 'AGPL-3.0'
        version: '@@pypi-python-mpv@@'
    }
}
