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
        name: 'inject'
        url: 'https://github.com/ivankorobkov/python-inject'
        licence: 'Apache-2.0'
        version: '@@pypi-inject@@'
        os: 'linux, windows'
    }
    ListElement {
        name: 'jinja2'
        url: 'https://github.com/pallets/jinja/'
        licence: 'BSD-3-Clause'
        version: '@@pypi-Jinja2@@'
        os: 'linux, windows'
    }
    ListElement {
        name: 'python-mpv'
        url: 'https://github.com/jaseg/python-mpv'
        licence: 'GPL-3.0'
        version: '@@pypi-mpv@@'
        os: 'linux, windows'
    }
    ListElement {
        name: 'PySide6'
        url: 'https://wiki.qt.io/Qt_for_Python'
        licence: 'LGPL-3.0'
        version: '@@pypi-PySide6@@'
        os: 'linux, windows'
    }
    ListElement {
        name: 'pywin32'
        url: 'https://github.com/mhammond/pywin32'
        licence: 'PSF'
        version: '@@pypi-pywin32@@'
        os: 'windows'
    }

    // Tests
    ListElement {
        name: 'parameterized'
        url: 'https://github.com/wolever/parameterized'
        licence: 'BSD'
        version: '@@pypi-parameterized@@'
        os: 'linux, windows'
    }
}
