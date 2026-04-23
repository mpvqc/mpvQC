// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../../utility"

Item {
    id: root

    required property MpvqcHeaderViewModel viewModel
    required property MpvqcMenuBarViewModel menuBarViewModel

    readonly property alias menuBarWidth: _menuBar.width
    readonly property alias menuBarHeight: _menuBar.height

    readonly property int minTitleSpacing: 32
    readonly property int separatorMargin: 8
    readonly property int leftContentWidth: menuBarWidth + _separator.width + _toolBar.width

    height: menuBarHeight
    visible: !MpvqcWindowUtility.isFullscreen

    DragHandler {
        target: null
        grabPermissions: TapHandler.CanTakeOverFromAnything

        onActiveChanged: {
            if (active) {
                root.viewModel.requestWindowDrag();
            }
        }
    }

    TapHandler {
        onDoubleTapped: {
            root.viewModel.requestToggleMaximize();
        }
    }

    RowLayout {
        width: root.width
        spacing: 0

        MpvqcMenuBar {
            id: _menuBar

            viewModel: root.menuBarViewModel
        }

        ToolSeparator {
            id: _separator

            visible: _toolBar.anyButtonVisible

            Layout.preferredHeight: 32
        }

        MpvqcToolBarView {
            id: _toolBar

            Layout.preferredHeight: root.menuBarHeight
            Layout.preferredWidth: width
        }

        Item {
            id: _leftTitleSpacer

            Layout.preferredWidth: Math.max(root.minTitleSpacing + root.separatorMargin * 2, root.width / 2 - root.leftContentWidth - _title.implicitWidth / 2)
            Layout.preferredHeight: root.menuBarHeight
        }

        Label {
            id: _title

            Layout.fillWidth: true
            Layout.preferredHeight: root.menuBarHeight
            Layout.rightMargin: root.minTitleSpacing
            text: root.viewModel.windowTitle
            elide: Text.ElideLeft
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }

        MpvqcHeaderWindowButtons {
            Layout.preferredHeight: root.menuBarHeight

            onMinimizeRequested: root.viewModel.requestMinimize()
            onToggleMaximizeRequested: root.viewModel.requestToggleMaximize()
            onCloseRequested: root.viewModel.requestClose()
        }
    }
}
