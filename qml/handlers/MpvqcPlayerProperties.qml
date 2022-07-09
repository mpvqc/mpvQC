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


pragma Singleton
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import pyobjects


MpvPlayerPropertiesPyObject {

    Component.onCompleted: {
        subscribe(properties())
    }

    function properties() {
        const properties = []
        for (const p in this)
            if (typeof this[p] != "function")
                properties.push(p)
        return properties
    }

    property bool path

    property string mpv_version
    property string ffmpeg_version

    property real duration
    property real percent_pos
    property real time_pos
    property real time_remaining

}
