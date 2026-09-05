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

    required property bool windowActive
    required property real windowWidth

    readonly property MpvqcPlayerViewModel _playerViewModel: MpvqcPlayerViewModel {}

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

    MpvqcShellHeaderViewModel {
        id: _headerViewModel
    }

    MpvqcShellMenuBarViewModel {
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
        onDialogRequested: kind => _overlayController.openDialog(kind)
        onFileDialogRequested: kind => _overlayController.openFileDialog(kind)
        onCustomExportRequested: template => _overlayController.openCustomExportFileDialog(template)
        onMessageBoxRequested: kind => _overlayController.openMessageBox(kind)
        onResizeVideoRequested: _layout.recalculateSizes()
    }

    MpvqcLayout {
        id: _layout

        focus: true
        anchors.fill: parent

        header: _header
        layoutOrientation: _menuBarViewModel.layoutOrientation
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
        id: _overlayController

        viewModel: _menuBarViewModel

        onFocusWanted: _layout.focusCommentTable()
    }

    MpvqcContentKeyHandler {
        id: _keyHandler

        onOpenCommentMenuRequested: _commentMenu.popup()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onForwardKeyToPlayerRequested: (key, modifiers) => root._playerViewModel.forwardKey(key, modifiers)
    }
}
