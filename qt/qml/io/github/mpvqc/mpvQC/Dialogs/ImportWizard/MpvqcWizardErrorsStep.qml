// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ColumnLayout {
    id: root

    required property var viewModel

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    spacing: 20

    MpvqcWizardStepHeader {
        objectName: "errorsHeader"
        //: Header above the list of QC documents the importer rejected
        text: qsTranslate("ImportWizardDialog", "%Ln QC document(s) could not be imported:", "", _listView.count)
    }

    ListView {
        id: _listView
        objectName: "errorList"

        Layout.fillWidth: true
        Layout.fillHeight: true

        model: root.viewModel.documents
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height
        spacing: 0

        delegate: ItemDelegate {
            id: _delegate

            required property string filename
            required property string fullPath
            required property string reason

            readonly property int iconSize: 24

            width: ListView.view.width
            verticalPadding: 12
            leftInset: root.isMirrored ? _scrollBar.visibleWidth : 0
            rightInset: root.isMirrored ? 0 : _scrollBar.visibleWidth
            leftPadding: leftInset + 16
            rightPadding: rightInset + 16

            contentItem: RowLayout {
                spacing: 12

                MpvqcIconLabel {
                    Layout.preferredWidth: _delegate.iconSize
                    Layout.preferredHeight: _delegate.iconSize

                    iconColor: MpvqcTheme.palette.error
                    icon.source: MpvqcIcons.error
                    icon.width: _delegate.iconSize
                    icon.height: _delegate.iconSize
                }

                ColumnLayout {
                    Layout.fillWidth: true

                    spacing: 2

                    Label {
                        objectName: "filenameLabel"

                        Layout.fillWidth: true

                        text: _delegate.filename
                        horizontalAlignment: Text.AlignLeft
                        elide: Text.ElideRight
                    }

                    Label {
                        objectName: "reasonLabel"

                        Layout.fillWidth: true

                        text: _delegate.reason
                        color: MpvqcTheme.palette.hint
                        horizontalAlignment: Text.AlignLeft
                        elide: Text.ElideRight
                    }
                }
            }

            ToolTip.text: _delegate.fullPath
            ToolTip.visible: hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay
        }

        ScrollBar.vertical: ScrollBar {
            id: _scrollBar

            readonly property bool isShown: _listView.contentHeight > _listView.height
            readonly property real visibleWidth: isShown ? width : 0

            policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }
    }
}
