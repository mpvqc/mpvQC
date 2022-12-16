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


/**
 * @param texts {Array<string>}
 * @param parent {QtObject}
 * @param parent
 */
function calculateWidthFor(texts, parent) {
    const textMetric = Application.os === 'windows'
        ? Qt.createQmlObject('import QtQuick; TextMetrics { font.pixelSize: 16 }', parent)
        : Qt.createQmlObject('import QtQuick; TextMetrics { }', parent)
    let width = 0
    for (const text of texts) {
        textMetric.text = text
        width = Math.max(width, textMetric.tightBoundingRect.width)
    }
    textMetric.destroy()
    return width
}
