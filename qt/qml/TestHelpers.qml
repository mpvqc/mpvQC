// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import pyobjects

import "app"

QtObject {
    id: root

    required property TestCase testCase

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}
    readonly property MpvqcTestSettings settings: MpvqcTestSettings {}

    readonly property Component _contentComponent: Component {
        MpvqcApplicationContent {
            anchors.fill: parent
            windowActive: true
            windowWidth: root.testCase.width
        }
    }

    readonly property Component _signalSpy: Component {
        SignalSpy {}
    }

    function resetState(): void {
        root.bridge.resetState();
    }

    function makeControl(): MpvqcApplicationContent {
        const control = root.testCase.createTemporaryObject(root._contentComponent, root.testCase);
        root.testCase.verify(control);
        return control;
    }

    function makeSpy(target, signalName: string): SignalSpy {
        const spy = root.testCase.createTemporaryObject(root._signalSpy, root.testCase, {
            target: target,
            signalName: signalName
        });
        root.testCase.verify(spy);
        return spy;
    }

    readonly property var menu: QtObject {
        function trigger(control: Item, menuName: string, itemName: string): void {
            const menu = root.testCase.findChild(control, menuName);
            root.testCase.verify(menu, `${menuName} not found`);
            menu.open();
            root.testCase.tryVerify(() => menu.opened);

            const item = root.testCase.findChild(menu, itemName);
            root.testCase.verify(item, `${itemName} not found`);
            root.testCase.mouseClick(item);
            root.testCase.tryVerify(() => !menu.opened);
        }

        function triggerSubItem(control: Item, parentMenuName: string, submenuName: string, itemObjectName: string): void {
            _triggerSubItemMatching(control, parentMenuName, submenuName, c => c?.objectName === itemObjectName, itemObjectName);
        }

        function triggerSubItemByText(control: Item, parentMenuName: string, submenuName: string, itemText: string): void {
            _triggerSubItemMatching(control, parentMenuName, submenuName, c => c?.text === itemText, itemText);
        }

        function openNewCommentMenu(control: Item): QtObject {
            const tableView = root.find.tableView(control);
            tableView.forceActiveFocus();
            root.testCase.keyClick(Qt.Key_E);
            return _waitForNewCommentMenu(control);
        }

        function openNewCommentMenuViaRightClick(control: Item): QtObject {
            const inputArea = root.testCase.findChild(control, "playerInputArea");
            root.testCase.verify(inputArea, "playerInputArea not found");
            root.testCase.tryVerify(() => inputArea.width > 0 && inputArea.height > 0);
            root.testCase.mouseClick(inputArea, inputArea.width / 2, inputArea.height / 2, Qt.RightButton);
            return _waitForNewCommentMenu(control);
        }

        function _waitForNewCommentMenu(control: Item): QtObject {
            const menu = root.testCase.findChild(control, "newCommentMenu");
            root.testCase.verify(menu, "newCommentMenu not found");
            root.testCase.tryVerify(() => menu.opened);
            return menu;
        }

        function _triggerSubItemMatching(control: Item, parentMenuName: string, submenuName: string, predicate: var, description: string): void {
            const parent = root.testCase.findChild(control, parentMenuName);
            root.testCase.verify(parent, `${parentMenuName} not found`);
            parent.open();
            root.testCase.tryVerify(() => parent.opened);

            const submenu = root.testCase.findChild(parent, submenuName);
            root.testCase.verify(submenu, `${submenuName} not found`);
            submenu.open();
            root.testCase.tryVerify(() => submenu.opened);

            let item = null;
            for (let i = 0; i < submenu.count; i++) {
                const candidate = submenu.itemAt(i);
                if (predicate(candidate)) {
                    item = candidate;
                    break;
                }
            }
            root.testCase.verify(item, `${description} not found`);
            root.testCase.mouseClick(item);
            root.testCase.tryVerify(() => !submenu.opened);
        }
    }

    readonly property var dialog: QtObject {
        function accept(dialog: QtObject): void {
            dialog.accepted();
            dialog.close();
            root.bridge.waitForBackgroundJobs();
        }
    }

    readonly property var comment: QtObject {
        function add(control: Item, commentType: string, text: string): void {
            const tableView = root.find.tableView(control);
            const before = tableView.commentCount;
            tableView.addNewComment(commentType);
            root.testCase.tryVerify(() => root.find.commentTextArea(control));
            root.find.commentTextArea(control).text = text;
            root.testCase.findChild(control, "editCommentPopup").close();
            root.testCase.tryVerify(() => tableView.commentCount === before + 1);
            root.testCase.wait(root.bridge.delayMs); // TODO: replace with a deterministic wait, model state propagation is async
        }
    }

    readonly property var find: QtObject {
        function tableView(control: Item): Item {
            const tv = root.testCase.findChild(control, "tableView");
            root.testCase.verify(tv, "tableView not found");
            return tv;
        }

        function commentTextArea(control: Item): Item {
            return root.testCase.findChild(control, "commentTextArea");
        }

        function dialogLoader(control: Item): Item {
            return root.testCase.findChild(control, "dialogLoader");
        }

        function fileDialogLoader(control: Item): Item {
            return root.testCase.findChild(control, "fileDialogLoader");
        }

        function messageBoxLoader(control: Item): Item {
            return root.testCase.findChild(control, "messageBoxLoader");
        }

        function openedDialog(control: Item, name: string): QtObject {
            root.testCase.tryVerify(() => {
                const dlg = root.testCase.findChild(control, name);
                return dlg && (dlg.opened ?? dlg.visible);
            });
            const dialog = root.testCase.findChild(control, name);
            root.testCase.verify(dialog, `${name} not found`);
            return dialog;
        }
    }

    readonly property var expect: QtObject {
        function commentCount(control: Item, expected: int): void {
            root.testCase.tryVerify(() => root.find.tableView(control).commentCount === expected);
        }

        function commentTypeAt(control: Item, index: int, expected: string): void {
            root.testCase.tryVerify(() => root.find.tableView(control).commentList.itemAtIndex(index)?.commentType === expected);
        }

        function dialogOpened(control: Item, name: string): void {
            root.find.openedDialog(control, name);
        }

        function dialogClosed(control: Item, name: string): void {
            root.testCase.tryVerify(() => {
                const dlg = root.testCase.findChild(control, name);
                return !dlg || !(dlg.opened ?? dlg.visible);
            });
        }

        function commentListHasFocus(control: Item): void {
            root.testCase.tryVerify(() => root.find.tableView(control).commentList.activeFocus);
        }

        function commentEditorHasFocus(control: Item): void {
            root.testCase.tryVerify(() => root.find.commentTextArea(control)?.activeFocus);
        }
    }
}
