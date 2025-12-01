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

    readonly property MpvqcWindowButtons windowButtons: MpvqcWindowButtons {}

    readonly property alias menuBarWidth: _menuBar.width
    readonly property alias menuBarHeight: _menuBar.height

    readonly property int minTitleSpacing: 32
    readonly property int separatorMargin: 8
    readonly property int leftContentWidth: menuBarWidth + _separator.width + _toolBar.width

    // *********************************************************
    // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
    // Once bug is resolved, we can remove ids from the menus
    readonly property alias isAnyMenuVisible: _menuBar.isAnyMenuVisible
    // *********************************************************

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

        MpvqcHeaderMenuBar {
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

            Layout.preferredWidth: Math.max(root.minTitleSpacing + 16, root.width / 2 - root.leftContentWidth - _title.implicitWidth / 2)
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

        Row {
            id: _windowButtons

            Layout.preferredHeight: root.menuBarHeight

            ToolButton {
                id: _minimizeButton

                visible: root.windowButtons.showMinimizeButton
                height: root.menuBarHeight
                focusPolicy: Qt.NoFocus
                icon.width: 20
                icon.height: 20
                icon.source: "qrc:/data/icons/minimize_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

                onClicked: {
                    root.viewModel.requestMinimize();
                }
            }

            ToolButton {
                id: _maximizeButton

                readonly property url iconMaximize: "qrc:/data/icons/open_in_full_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                readonly property url iconNormalize: "qrc:/data/icons/close_fullscreen_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"

                visible: root.windowButtons.showMaximizeButton
                height: root.menuBarHeight
                focusPolicy: Qt.NoFocus
                icon.width: 18
                icon.height: 18
                icon.source: MpvqcWindowUtility.isMaximized ? iconNormalize : iconMaximize

                onClicked: {
                    root.viewModel.requestToggleMaximize();
                }
            }

            ToolButton {
                id: _closeButton

                visible: root.windowButtons.showCloseButton
                height: root.menuBarHeight
                focusPolicy: Qt.NoFocus

                icon {
                    width: 18
                    height: 18
                    source: "qrc:/data/icons/close_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    color: {
                        if (root.viewModel.isWindows && _closeButton.hovered) {
                            return "#FFFFFD";
                        } else if (_closeButton.hovered) {
                            return MpvqcTheme.background;
                        } else {
                            return MpvqcTheme.foreground;
                        }
                    }
                }

                onClicked: {
                    root.viewModel.requestClose();
                }

                Binding {
                    when: true
                    target: _closeButton.background
                    property: "color"
                    value: root.viewModel.isWindows ? "#C42C1E" : MpvqcTheme.control
                    restoreMode: Binding.RestoreNone
                }
            }
        }
    }
}
