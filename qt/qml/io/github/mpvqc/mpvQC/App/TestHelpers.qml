// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

QtObject {
    id: root

    required property TestCase suite

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}
    readonly property MpvqcTestSettings settings: MpvqcTestSettings {}

    readonly property var menu: QtObject {
        function trigger(control: Item, menuName: string, itemName: string): void {
            const menu = root.suite.findChild(control, menuName);
            root.suite.verify(menu, `${menuName} not found`);
            menu.open();
            root.suite.tryVerify(() => menu.opened);

            const item = root.suite.findChild(menu, itemName);
            root.suite.verify(item, `${itemName} not found`);
            root.suite.mouseClick(item);
            root.suite.tryVerify(() => !menu.opened);
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
            root.suite.keyClick(Qt.Key_E);
            return _waitForNewCommentMenu(control);
        }

        function openNewCommentMenuViaRightClick(control: Item): QtObject {
            const inputArea = root.suite.findChild(control, "playerInputArea");
            root.suite.verify(inputArea, "playerInputArea not found");
            root.suite.tryVerify(() => inputArea.width > 0 && inputArea.height > 0);
            root.suite.mouseClick(inputArea, inputArea.width / 2, inputArea.height / 2, Qt.RightButton);
            return _waitForNewCommentMenu(control);
        }

        function _waitForNewCommentMenu(control: Item): QtObject {
            const menu = root.suite.findChild(control, "newCommentMenu");
            root.suite.verify(menu, "newCommentMenu not found");
            root.suite.tryVerify(() => menu.opened);
            return menu;
        }

        function _triggerSubItemMatching(control: Item, parentMenuName: string, submenuName: string, predicate: var, description: string): void {
            const parent = root.suite.findChild(control, parentMenuName);
            root.suite.verify(parent, `${parentMenuName} not found`);
            parent.open();
            root.suite.tryVerify(() => parent.opened);

            const submenu = root.suite.findChild(parent, submenuName);
            root.suite.verify(submenu, `${submenuName} not found`);
            submenu.open();
            root.suite.tryVerify(() => submenu.opened);

            let item = null;
            for (let i = 0; i < submenu.count; i++) {
                const candidate = submenu.itemAt(i);
                if (predicate(candidate)) {
                    item = candidate;
                    break;
                }
            }
            root.suite.verify(item, `${description} not found`);
            root.suite.mouseClick(item);
            root.suite.tryVerify(() => !submenu.opened);
        }
    }

    readonly property var dialog: QtObject {
        function accept(dialog: var): void {
            _finish(dialog, () => dialog.accepted());
        }

        function reject(dialog: var): void {
            _finish(dialog, () => dialog.rejected());
        }

        function _finish(dialog: var, emitOutcome: var): void {
            const name = dialog.objectName;
            emitOutcome();
            dialog.close();
            if (name) {
                root.suite.tryVerify(() => !root.suite.findChild(root.suite, name));
            } else {
                root.suite.tryVerify(() => !dialog || !(dialog.opened ?? dialog.visible));
            }
            root.bridge.waitForBackgroundJobs();
        }
    }

    readonly property var comment: QtObject {
        function add(control: Item, commentType: string, text: string): void {
            const tableView = root.find.tableView(control);
            const before = tableView.commentCount;
            tableView.addNewComment(commentType);
            root.suite.tryVerify(() => root.find.commentTextArea(control));
            root.find.commentTextArea(control).text = text;
            root.suite.findChild(control, "editCommentPopup").close();
            root.suite.tryVerify(() => tableView.commentCount === before + 1);
            root.suite.tryVerify(() => !root.suite.findChild(control, "editCommentPopup"));
        }
    }

    readonly property var find: QtObject {
        function tableView(control: Item): Item {
            const tv = root.suite.findChild(control, "tableView");
            root.suite.verify(tv, "tableView not found");
            return tv;
        }

        function commentTextArea(control: Item): Item {
            return root.suite.findChild(control, "commentTextArea");
        }

        function dialogLoader(control: Item): Item {
            return root.suite.findChild(control, "dialogLoader");
        }

        function fileDialogLoader(control: Item): Item {
            return root.suite.findChild(control, "fileDialogLoader");
        }

        function messageBoxLoader(control: Item): Item {
            return root.suite.findChild(control, "messageBoxLoader");
        }

        // View delegates hang off their view visually only, so findChild walks past them.
        // Popups are no items, so the search enters them through their content item.
        function visualChild(item: var, objectName: string): Item {
            if (!item) {
                return null;
            }
            if (item.objectName === objectName) {
                return item;
            }
            const kids = item.children ?? [item.contentItem];
            for (let i = 0; i < kids.length; i++) {
                const found = visualChild(kids[i], objectName);
                if (found) {
                    return found;
                }
            }
            return null;
        }

        function openedDialog(control: Item, name: string): QtObject {
            root.suite.tryVerify(() => {
                const dlg = root.suite.findChild(control, name);
                return dlg && (dlg.opened ?? dlg.visible);
            });
            const dialog = root.suite.findChild(control, name);
            root.suite.verify(dialog, `${name} not found`);
            return dialog;
        }
    }

    readonly property var expect: QtObject {
        function commentCount(control: Item, expected: int): void {
            root.suite.tryVerify(() => root.find.tableView(control).commentCount === expected);
        }

        function commentTypeAt(control: Item, index: int, expected: string): void {
            root.suite.tryVerify(() => root.find.tableView(control).commentList.itemAtIndex(index)?.commentType === expected);
        }

        function dialogOpened(control: Item, name: string): void {
            root.find.openedDialog(control, name);
        }

        function dialogClosed(control: Item, name: string): void {
            root.suite.tryVerify(() => {
                const dlg = root.suite.findChild(control, name);
                return !dlg || !(dlg.opened ?? dlg.visible);
            });
        }

        function commentListHasFocus(control: Item): void {
            root.suite.tryVerify(() => root.find.tableView(control).commentList.activeFocus);
        }

        function commentEditorHasFocus(control: Item): void {
            root.suite.tryVerify(() => root.find.commentTextArea(control)?.activeFocus);
        }

        function openedVideo(name: string): void {
            root.suite.tryVerify(() => root.bridge.openedVideoName() === name);
        }

        function noOpenedVideo(): void {
            root.suite.compare(root.bridge.openedVideoName(), "");
        }

        function openedSubtitleCount(count: int): void {
            root.suite.tryVerify(() => root.bridge.openedSubtitleCount() === count);
        }

        function openedSubtitles(names: list<string>): void {
            root.suite.tryVerify(() => {
                const opened = root.bridge.openedSubtitleNames();
                return opened.length === names.length && names.every(n => opened.indexOf(n) >= 0);
            });
        }
    }

    readonly property var player: QtObject {
        // The player holds a subtitle back until a video plays; drop subtitles after this.
        function playVideo(): void {
            root.bridge.loadVideo({});
        }
    }

    readonly property var imports: QtObject {
        function dropFiles(control: Item, urls: list<var>): void {
            const dropArea = root.suite.findChild(control, "fileDropArea");
            root.suite.verify(dropArea, "fileDropArea not found");
            dropArea.viewModel.open(urls);
            root.bridge.waitForBackgroundJobs();
        }
    }

    readonly property var wizard: QtObject {
        function opened(control: Item): QtObject {
            const dlg = root.find.openedDialog(control, "importWizardDialog");
            const stepView = root.suite.findChild(dlg.contentItem, "stepView");
            if (stepView) {
                stepView.sweepDuration = 0;
            }
            return dlg;
        }

        function clickPrimary(dlg: QtObject): void {
            const btn = root.suite.findChild(dlg.footer, "primaryButton");
            root.suite.verify(btn, "primaryButton not found");
            root.suite.mouseClick(btn);
        }

        function clickCancel(dlg: QtObject): void {
            const btn = root.suite.findChild(dlg.footer, "cancelButton");
            root.suite.verify(btn, "cancelButton not found");
            root.suite.mouseClick(btn);
        }

        function advance(dlg: QtObject): void {
            root.wizard.clickPrimary(dlg);
            root.suite.waitForRendering(dlg.contentItem);
        }

        function pickVideo(dlg: QtObject, index: int): void {
            _pickRow(dlg, "videoList", index);
        }

        function pickNoVideo(dlg: QtObject): void {
            const list = root.suite.findChild(dlg.contentItem, "videoList");
            root.suite.verify(list, "videoList not found");
            _pickRow(dlg, "videoList", list.count - 1);
        }

        function pickSubtitle(dlg: QtObject, index: int): void {
            _pickRow(dlg, "subtitleList", index);
        }

        function _pickRow(dlg: QtObject, listName: string, index: int): void {
            const list = root.suite.findChild(dlg.contentItem, listName);
            root.suite.verify(list, `${listName} not found`);
            root.suite.tryVerify(() => list.itemAtIndex(index) !== null);
            root.suite.mouseClick(list.itemAtIndex(index));
        }
    }

    readonly property Component _contentComponent: Component {
        MpvqcApplicationContent {
            anchors.fill: parent
            windowActive: true
            windowWidth: root.suite.width
        }
    }

    readonly property Component _signalSpy: Component {
        SignalSpy {}
    }

    function resetState(): void {
        root.bridge.resetState();
    }

    function makeControl(): MpvqcApplicationContent {
        const control = root.suite.createTemporaryObject(root._contentComponent, root.suite);
        root.suite.verify(control);
        return control;
    }

    function makeSpy(target, signalName: string): SignalSpy {
        const spy = root.suite.createTemporaryObject(root._signalSpy, root.suite, {
            target: target,
            signalName: signalName
        });
        root.suite.verify(spy);
        return spy;
    }
}
