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

QtObject {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcApplicationPathsPyObject: mpvqcApplication.mpvqcApplicationPathsPyObject
    readonly property var settingsFile: mpvqcApplicationPathsPyObject.settings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    readonly property MpvqcLanguageModel _languageModel: MpvqcLanguageModel {}

    // Backup

    readonly property Settings _backupSettings: Settings {
        property alias enabled: root.backupEnabled
        property alias interval: root.backupInterval

        category: "Backup"
        location: root.settingsFile
    }

    property bool backupEnabled: true
    property int backupInterval: 60

    // Common

    readonly property Settings _commonSettings: Settings {
        property alias language: root.language
        property alias commentTypes: root.commentTypes

        category: "Common"
        location: root.settingsFile
    }
    property string language: _languageModel.systemLanguage
    property list<string> commentTypes: root.getDefaultCommentTypes()

    function getDefaultCommentTypes(): list<string> {
        return ["Translation", "Spelling", "Punctuation", "Phrasing", "Timing", "Typeset", "Note"];
    }

    readonly property list<string> forTranslationTool: [
        qsTranslate("CommentTypes", "Translation"),
        qsTranslate("CommentTypes", "Spelling"),
        qsTranslate("CommentTypes", "Punctuation"),
        qsTranslate("CommentTypes", "Phrasing"),
        qsTranslate("CommentTypes", "Timing"),
        qsTranslate("CommentTypes", "Typeset"),
        qsTranslate("CommentTypes", "Note"),
    ]

    // Export

    readonly property Settings _exportSettings: Settings {
        property alias nickname: root.nickname
        property alias writeHeaderDate: root.writeHeaderDate
        property alias writeHeaderGenerator: root.writeHeaderGenerator
        property alias writeHeaderNickname: root.writeHeaderNickname
        property alias writeHeaderVideoPath: root.writeHeaderVideoPath

        category: "Export"
        location: root.settingsFile
    }

    property string nickname: root.mpvqcUtilityPyObject.getEnvironmentVariable("USERNAME") || root.mpvqcUtilityPyObject.getEnvironmentVariable("USER") || "nickname"
    property bool writeHeaderDate: true
    property bool writeHeaderGenerator: true
    property bool writeHeaderNickname: false
    property bool writeHeaderVideoPath: true

    // Statusbar

    enum TimeFormat {
        EMPTY,
        CURRENT_TIME,
        REMAINING_TIME,
        CURRENT_TOTAL_TIME
    }

    readonly property Settings _statusBarSettings: Settings {
        property alias statusbarPercentage: root.statusbarPercentage
        property alias timeFormat: root.timeFormat

        category: "StatusBar"
        location: root.settingsFile
    }

    property bool statusbarPercentage: true
    property int timeFormat: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME

    // Import

    enum ImportWhenVideoLinkedInDocument {
        ALWAYS,
        ASK_EVERY_TIME,
        NEVER
    }

    readonly property Settings _importSettings: Settings {
        property alias lastDirectoryVideo: root.lastDirectoryVideo
        property alias lastDirectoryDocuments: root.lastDirectoryDocuments
        property alias lastDirectorySubtitles: root.lastDirectorySubtitles
        property alias importWhenVideoLinkedInDocument: root.importWhenVideoLinkedInDocument

        category: "Import"
        location: root.settingsFile
    }

    property string lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
    property string lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
    property string lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
    property int importWhenVideoLinkedInDocument: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME

    // Splitview

    readonly property Settings _splitViewSettings: Settings {
        property alias layoutOrientation: root.layoutOrientation

        category: "SplitView"
        location: root.settingsFile
    }

    property int layoutOrientation: Qt.Vertical

    // Theme

    readonly property Settings _themeSettings: Settings {
        property alias themeIdentifier: root.themeIdentifier
        property alias themeColorOption: root.themeColorOption

        category: "Theme"
        location: root.settingsFile
    }

    property string themeIdentifier: "Material You Dark"
    property int themeColorOption: 16

    // Window Title

    enum WindowTitleFormat {
        DEFAULT,
        FILE_NAME,
        FILE_PATH
    }

    readonly property Settings _windowSettings: Settings {
        property alias titleFormat: root.windowTitleFormat

        category: "Window"
        location: root.settingsFile
    }

    property int windowTitleFormat: MpvqcSettings.WindowTitleFormat.DEFAULT
}
