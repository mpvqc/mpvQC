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


Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcWidthCalculatorLabel: mpvqcApplication.mpvqcWidthCalculatorLabel

    readonly property int defaultPadding: 8
    property int maxWidth

    function recalculateMaxWidth(): void {
        const commentTypes = mpvqcSettings.commentTypes.items().map(english => qsTranslate("CommentTypes", english))
        const width = mpvqcWidthCalculatorLabel.calculateWidthFor(commentTypes, root)
        maxWidth = width
    }

    Connections {
        target: root.mpvqcSettings

        function onCommentTypesChanged() { root.recalculateMaxWidth() }
        function onLanguageChanged() { root.recalculateMaxWidth() }
    }

    Component.onCompleted: {
        recalculateMaxWidth()
    }

}
