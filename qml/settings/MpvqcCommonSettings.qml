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

import QtCore
import QtQuick

import models


Item {
    id: root

    readonly property MpvqcLanguageModel _languageModel: MpvqcLanguageModel {}

    property var uiLanguages: Qt.locale().uiLanguages

    property alias language: _settings.language
    property alias commentTypes: _settings.commentTypes
    property alias location: _settings.location

    function _defaultLanguage(): string {
        return _languageModel.identifiers()
            .find(language => uiLanguages.includes(language)) ?? 'en-US'
    }

    function getDefaultCommentTypes(): list<string> {
        return ['Translation', 'Spelling', 'Punctuation', 'Phrasing', 'Timing', 'Typeset', 'Note']
    }

    Settings {
        id: _settings
        category: 'Common'
        property string language: root._defaultLanguage()
        property list <string> commentTypes: getDefaultCommentTypes()
    }

}
