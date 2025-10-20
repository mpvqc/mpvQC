// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

ListModel {
    ListElement {
        name: "inject"
        url: "https://github.com/ivankorobkov/python-inject"
        licence: "Apache-2.0"
        version: "@@pypi-inject@@"
        os: "linux, windows"
    }
    ListElement {
        name: "jinja2"
        url: "https://github.com/pallets/jinja/"
        licence: "BSD-3-Clause"
        version: "@@pypi-jinja2@@"
        os: "linux, windows"
    }
    ListElement {
        name: "loguru"
        url: "https://github.com/Delgan/loguru"
        licence: "MIT"
        version: "@@pypi-loguru@@"
        os: "linux, windows"
    }
    ListElement {
        name: "python-mpv"
        url: "https://github.com/jaseg/python-mpv"
        licence: "GPL-3.0"
        version: "@@pypi-mpv@@"
        os: "linux, windows"
    }
    ListElement {
        name: "PySide6"
        url: "https://wiki.qt.io/Qt_for_Python"
        licence: "LGPL-3.0"
        version: "@@pypi-pyside6-essentials@@"
        os: "linux, windows"
    }
    ListElement {
        name: "pywin32"
        url: "https://github.com/mhammond/pywin32"
        licence: "PSF"
        version: "@@pypi-pywin32@@"
        os: "windows"
    }
    ListElement {
        name: "pytest"
        url: "https://github.com/pytest-dev/pytest"
        licence: "MIT"
        version: "@@pypi-pytest@@"
        os: "linux, windows"
    }
}
