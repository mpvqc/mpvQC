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
import settings
import "MpvqcLabelWidthCalculator.js" as Calculator


QtObject {
    id: object

    readonly property var commentTypes: MpvqcSettings.commentTypes
    property int width: 0

    Component.onCompleted: {
        MpvqcSettings.onLanguageChanged.connect(calculateMaxWidth)
    }

    onCommentTypesChanged: {
        calculateMaxWidth()
    }

    function calculateMaxWidth() {
        const texts = MpvqcSettings.commentTypes.items().map(english => qsTranslate("CommentTypes", english))
        const width = Calculator.calculateWidthFor(texts, object)
        object.width = width + 8
    }

}
