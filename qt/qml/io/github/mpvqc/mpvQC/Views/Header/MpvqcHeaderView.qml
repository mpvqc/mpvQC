// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root
    objectName: "headerView"

    required property MpvqcShellHeaderViewModel viewModel
    required property MpvqcShellMenuBarViewModel menuBarViewModel

    readonly property alias menuBarWidth: _menuBar.width
    readonly property alias menuBarHeight: _menuBar.height

    readonly property int minTitleSpacing: 32
    readonly property int titleEdgeMargin: 8
    readonly property int leftContentWidth: menuBarWidth + _toolBar.width

    signal windowDragRequested
    signal minimizeRequested
    signal toggleMaximizeRequested
    signal closeRequested
    signal dialogRequested(kind: int)
    signal fileDialogRequested(kind: int)
    signal customExportRequested(template: url)
    signal messageBoxRequested(kind: int)
    signal resizeVideoRequested

    height: menuBarHeight
    visible: !MpvqcWindowUtility.isFullscreen

    Rectangle {
        anchors.fill: parent
        color: MpvqcAppearance.palette.headerBackground
        topLeftRadius: MpvqcWindowUtility.windowRadius
        topRightRadius: MpvqcWindowUtility.windowRadius
    }

    DragHandler {
        target: null
        grabPermissions: TapHandler.CanTakeOverFromAnything

        onActiveChanged: {
            if (active) {
                root.windowDragRequested();
            }
        }
    }

    TapHandler {
        onDoubleTapped: {
            root.toggleMaximizeRequested();
        }
    }

    RowLayout {
        width: root.width
        spacing: 0

        MpvqcMenuBar {
            id: _menuBar

            viewModel: root.menuBarViewModel

            onDialogRequested: kind => root.dialogRequested(kind)
            onFileDialogRequested: kind => root.fileDialogRequested(kind)
            onCustomExportRequested: template => root.customExportRequested(template)
            onMessageBoxRequested: kind => root.messageBoxRequested(kind)
            onCloseRequested: root.closeRequested()
            onResizeVideoRequested: root.resizeVideoRequested()
        }

        MpvqcToolBarView {
            id: _toolBar

            Layout.preferredHeight: root.menuBarHeight
            Layout.preferredWidth: width
        }

        Item {
            id: _leftTitleSpacer

            Layout.preferredWidth: Math.max(root.minTitleSpacing + root.titleEdgeMargin * 2, root.width / 2 - root.leftContentWidth - _title.implicitWidth / 2)
            Layout.preferredHeight: root.menuBarHeight
        }

        Label {
            id: _title

            text: root.viewModel.windowTitle
            elide: Text.ElideLeft
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter

            Layout.fillWidth: true
            Layout.preferredHeight: root.menuBarHeight
            Layout.rightMargin: root.minTitleSpacing
        }

        MpvqcHeaderWindowButtons {
            Layout.preferredHeight: root.menuBarHeight

            onMinimizeRequested: root.minimizeRequested()
            onToggleMaximizeRequested: root.toggleMaximizeRequested()
            onCloseRequested: root.closeRequested()
        }
    }
}
