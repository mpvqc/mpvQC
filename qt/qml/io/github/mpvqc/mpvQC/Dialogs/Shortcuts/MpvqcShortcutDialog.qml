// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "shortcutsDialog"

    title: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")

    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: Math.min(720, MpvqcWindowUtility.appHeight * 0.65)
    standardButtons: Dialog.Close

    contentItem: ColumnLayout {
        spacing: 0

        TextField {
            id: _searchField
            objectName: "searchField"

            focus: true
            selectByMouse: true
            //: Placeholder text for search entry
            placeholderText: qsTranslate("ShortcutsDialog", "Search")
            horizontalAlignment: Text.AlignLeft

            Layout.fillWidth: true
            Layout.topMargin: 10
            Layout.bottomMargin: 20

            ContextMenu.menu: null
        }

        ListView {
            id: _listView
            objectName: "shortcutsListView"

            readonly property int spaceBetweenItemAndScrollbar: 4
            readonly property int scrollBarSpace: _scrollBar.width + spaceBetweenItemAndScrollbar
            readonly property int scrollBarOffset: LayoutMirroring.enabled ? scrollBarSpace : 0

            spacing: 0
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            Layout.fillWidth: true
            Layout.fillHeight: true

            model: MpvqcShortcutsModel {
                query: _searchField.text
            }

            delegate: Item {
                id: _delegate

                required property var model
                required property int index

                width: parent ? parent.width : 0
                height: _row.height

                MpvqcShortcutRow {
                    id: _row

                    label: _delegate.model.label
                    sequences: _delegate.model.sequences
                    note: _delegate.model.note
                    striped: _delegate.index % 2 === 1

                    x: _listView.scrollBarOffset
                    width: Math.max(0, _delegate.width - _listView.scrollBarSpace)
                }
            }

            section {
                property: "category"

                delegate: MpvqcHeader {
                    objectName: "sectionHeader"

                    required property string section

                    text: section
                    color: MpvqcTheme.palette.accent
                    width: parent ? parent.width : 0
                    font.pointSize: 12
                    topPadding: 24
                    leftPadding: 8
                    rightPadding: 8
                }
            }

            ScrollBar.vertical: ScrollBar {
                id: _scrollBar

                readonly property bool isShown: _listView.contentHeight > _listView.height

                policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
            }

            Column {
                objectName: "emptyState"

                visible: _listView.count === 0
                spacing: 8

                anchors.centerIn: parent

                MpvqcIconLabel {
                    icon.source: MpvqcIcons.search
                    icon.width: 32
                    icon.height: 32
                    iconColor: MpvqcTheme.palette.hint

                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Label {
                    //: Shown in the keyboard shortcut dialog when the search matches no shortcut
                    text: qsTranslate("ShortcutsDialog", "No shortcuts found")
                    color: MpvqcTheme.palette.hint

                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }
    }
}
