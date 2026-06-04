// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root

    required property var viewModel

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    spacing: 20

    MpvqcWizardStepHeader {
        //: Subtitles step prompt above the subtitles list
        text: qsTranslate("ImportWizardDialog", "Which subtitles should be loaded?")

        CheckBox {
            id: _selectAll
            objectName: "selectAll"

            anchors.top: parent.top
            anchors.bottom: parent.bottom

            visible: _listView.count > 1
            //: Tri-state "Select all" checkbox in the subtitles step header
            text: qsTranslate("ImportWizardDialog", "Select all")
            tristate: true
            hoverEnabled: false

            onClicked: root.viewModel.toggleSelectAll()
        }

        Binding {
            target: _selectAll
            property: "checkState"
            value: root.viewModel.selectAllTriState
        }
    }

    ListView {
        id: _listView
        objectName: "subtitleList"

        Layout.fillWidth: true
        Layout.fillHeight: true

        model: root.viewModel.subtitles
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height
        spacing: 0

        delegate: ItemDelegate {
            id: _delegate

            required property int index
            required property string filename
            required property bool isChecked

            width: ListView.view.width
            verticalPadding: 16
            leftInset: root.isMirrored ? _scrollBar.visibleWidth : 0
            rightInset: root.isMirrored ? 0 : _scrollBar.visibleWidth
            leftPadding: leftInset + 16
            rightPadding: rightInset + 16

            contentItem: RowLayout {
                spacing: 12

                CheckBox {
                    id: _checkbox
                    objectName: "checkbox"

                    padding: 0
                    hoverEnabled: false
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
                    Layout.alignment: Qt.AlignVCenter

                    onClicked: root.viewModel.toggle(_delegate.index)
                }

                Binding {
                    target: _checkbox
                    property: "checked"
                    value: _delegate.isChecked
                }

                Label {
                    objectName: "label"

                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter

                    text: _delegate.filename
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Text.Wrap
                    maximumLineCount: 2
                    elide: Text.ElideRight
                }
            }

            onClicked: root.viewModel.toggle(_delegate.index)
        }

        ScrollBar.vertical: ScrollBar {
            id: _scrollBar

            readonly property bool isShown: _listView.contentHeight > _listView.height
            readonly property real visibleWidth: isShown ? width : 0

            policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }
    }
}
