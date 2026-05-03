// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Views.Header
import io.github.mpvqc.mpvQC.Views.Player

Item {
    id: root

    readonly property MpvqcAppViewModel viewModel: MpvqcAppViewModel {}

    required property bool windowActive
    required property real windowWidth

    property bool _initialFocusDone: false

    signal closeRequested
    signal minimizeRequested
    signal toggleMaximizeRequested
    signal startSystemMoveRequested
    signal toggleFullScreenRequested
    signal disableFullScreenRequested
    signal appWindowSizeRequested(width: int, height: int)

    onWindowActiveChanged: {
        if (windowActive && !_initialFocusDone) {
            _initialFocusDone = true;
            _layout.focusCommentTable();
        }
    }

    Keys.onEscapePressed: root.disableFullScreenRequested()
    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    MpvqcHeaderViewModel {
        id: _headerViewModel
    }

    MpvqcMenuBarViewModel {
        id: _menuBarViewModel
    }

    MpvqcHeaderView {
        id: _header

        viewModel: _headerViewModel
        menuBarViewModel: _menuBarViewModel
        width: root.windowWidth

        onWindowDragRequested: root.startSystemMoveRequested()
        onMinimizeRequested: root.minimizeRequested()
        onToggleMaximizeRequested: root.toggleMaximizeRequested()
        onCloseRequested: root.closeRequested()
    }

    MpvqcLayout {
        id: _layout

        focus: true
        anchors.fill: parent
        anchors.margins: root.viewModel.windowBorder

        header: _header
        layoutOrientation: root.viewModel.layoutOrientation
        windowBorder: root.viewModel.windowBorder
        headerHeight: _header.height

        onAppWindowSizeRequested: (width, height) => root.appWindowSizeRequested(width, height)
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onAddNewCommentMenuRequested: _commentMenu.popup()
    }

    MpvqcFileDropArea {
        anchors.fill: _layout
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.disableFullScreenRequested();
            _layout.addComment(commentType);
        }
    }

    MpvqcNewCommentMenuClickGuard {
        menu: _commentMenu
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: undefined
        propagateComposedEvents: true

        onPressed: event => {
            event.accepted = false;
            _layout.focusCommentTable();
        }
    }

    MpvqcOverlayController {
        viewModel: _menuBarViewModel

        onFocusWanted: _layout.focusCommentTable()
        onCloseAppRequested: root.closeRequested()
        onResizeVideoRequested: _layout.recalculateSizes()
    }

    MpvqcContentKeyHandler {
        id: _keyHandler

        onOpenCommentMenuRequested: _commentMenu.popup()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onForwardKeyToPlayerRequested: (key, modifiers) => root.viewModel.forwardKeyToPlayer(key, modifiers)
    }
}
