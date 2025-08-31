/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    required property string errorMessage
    required property int errorLine

    title: qsTranslate("MessageBoxes", "Export Error")
    text: errorLine ?
    //: %1 will be the line nr of the error, %2 will be the error message (probably in English)
    qsTranslate("MessageBoxes", "Error at line %1: %2").arg(errorLine).arg(errorMessage) : errorMessage

    standardButtons: Dialog.Ok
}
