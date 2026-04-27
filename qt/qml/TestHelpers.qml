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
}
