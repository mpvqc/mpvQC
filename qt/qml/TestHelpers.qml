// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import pyobjects

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

    function addComment(control: Item, commentType: string, text: string): void {
        const tableView = root.testCase.findChild(control, "tableView");
        root.testCase.verify(tableView, "tableView not found");
        const before = tableView.commentCount;
        tableView.addNewComment(commentType);
        root.testCase.tryVerify(() => root.testCase.findChild(control, "commentTextArea"));
        root.testCase.findChild(control, "commentTextArea").text = text;
        root.testCase.findChild(control, "editCommentPopup").close();
        root.testCase.tryVerify(() => tableView.commentCount === before + 1);
        root.testCase.wait(root.bridge.delayMs); // TODO: replace with a deterministic wait, model state propagation is async
    }

    function findOpenedDialog(control: Item, name: string): QtObject {
        root.testCase.tryVerify(() => {
            const dlg = root.testCase.findChild(control, name);
            return dlg && (dlg.opened ?? dlg.visible);
        });
        const dialog = root.testCase.findChild(control, name);
        root.testCase.verify(dialog, `${name} not found`);
        return dialog;
    }

    function acceptDialog(dialog: QtObject): void {
        dialog.accepted();
        dialog.close();
        root.bridge.waitForBackgroundJobs();
    }

    function openNewCommentMenu(control: Item): QtObject {
        const tableView = root.testCase.findChild(control, "tableView");
        root.testCase.verify(tableView, "tableView not found");
        tableView.forceActiveFocus();
        root.testCase.keyClick(Qt.Key_E);
        const menu = root.testCase.findChild(control, "newCommentMenu");
        root.testCase.verify(menu, "newCommentMenu not found");
        root.testCase.tryVerify(() => menu.opened);
        return menu;
    }

    function triggerMenuItem(control: Item, menuName: string, itemName: string): void {
        const menu = root.testCase.findChild(control, menuName);
        root.testCase.verify(menu, `${menuName} not found`);
        menu.open();
        root.testCase.tryVerify(() => menu.opened);

        const item = root.testCase.findChild(menu, itemName);
        root.testCase.verify(item, `${itemName} not found`);
        root.testCase.mouseClick(item);
        root.testCase.tryVerify(() => !menu.opened);
    }

    function triggerSubmenuItem(control: Item, parentMenuName: string, submenuName: string, itemObjectName: string): void {
        root._triggerSubmenuItemMatching(control, parentMenuName, submenuName, c => c?.objectName === itemObjectName, itemObjectName);
    }

    function triggerSubmenuItemByText(control: Item, parentMenuName: string, submenuName: string, itemText: string): void {
        root._triggerSubmenuItemMatching(control, parentMenuName, submenuName, c => c?.text === itemText, itemText);
    }

    function _triggerSubmenuItemMatching(control: Item, parentMenuName: string, submenuName: string, predicate: var, description: string): void {
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
