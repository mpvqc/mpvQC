// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcBackupDialog"
    width: 640
    height: 720
    visible: true
    when: windowShown

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    function init(): void {
        failOnWarning(/.*/);
    }

    function makeControl(enabled = true): MpvqcBackupDialog {
        const dialog = createTemporaryObject(_dialog, testCase);
        verify(dialog);
        dialog.viewModel.temporaryBackupEnabled = enabled;
        dialog.viewModel.temporaryBackupInterval = 75;
        dialog.open();
        verify(waitForRendering(dialog.contentItem));
        tryCompare(dialog, "opened", true);
        verify(waitForPolish(dialog.contentItem.Window.window));
        return dialog;
    }

    function makeSpy(target: QtObject, signalName: string): SignalSpy {
        const spy = createTemporaryObject(_spy, testCase, {
            target,
            signalName
        });
        verify(spy && spy.valid);
        return spy;
    }

    function presets(item: Item): list<var> {
        let result = [];
        for (const child of item.children) {
            if (child instanceof Button && child.objectName.startsWith("backupIntervalPreset_")) {
                result.push(child);
            } else {
                result = result.concat(presets(child));
            }
        }
        return result;
    }

    function test_presetsMapToSecondsAndSurviveFolding(): void {
        const dialog = makeControl();
        const buttons = presets(dialog.contentItem);
        compare(buttons.length, 6);
        verify(buttons.every(button => !button.checked), "an unmatched interval must have no selection");
        const seconds = [30, 60, 90, 120, 180, 300];
        for (let index = 0; index < buttons.length; index++) {
            mouseClick(buttons[index]);
            compare(dialog.viewModel.temporaryBackupInterval, seconds[index]);
            compare(buttons.map(button => button.checked), seconds.map(value => value === seconds[index]));
        }

        const toggle = findChild(dialog.contentItem, "backupEnabledSwitch");
        const interval = findChild(dialog.contentItem, "backupIntervalCard");
        const enabled = findChild(dialog.contentItem, "backupEnabledCard");
        const location = findChild(dialog.contentItem, "backupLocationCard");
        verify(toggle && interval && enabled && location);

        mouseClick(toggle);
        verify(buttons.every(button => !button.enabled));
        mouseClick(buttons[0]);
        compare(dialog.viewModel.temporaryBackupInterval, 300);
        tryCompare(interval, "visible", false);
        verify(waitForPolish(dialog.contentItem.Window.window));
        const gap = bridge.verticalGap(enabled, location);
        verify(bridge.nearlyEqual(gap, MpvqcConstants.dialogSectionSpacing), `the folded interval should leave a gap of ${MpvqcConstants.dialogSectionSpacing}, not ${gap}`);

        mouseClick(toggle);
        tryCompare(interval, "visible", true);
        verify(buttons.every(button => button.enabled));
        verify(buttons[5].checked);
    }

    function test_opensWithIntervalHiddenWhenBackupsDisabled(): void {
        const dialog = makeControl(false);
        const interval = findChild(dialog.contentItem, "backupIntervalCard");
        verify(interval);
        verify(!interval.visible);
    }

    function test_rapidTogglesPreserveUnmatchedInterval(): void {
        const dialog = makeControl();
        const toggle = findChild(dialog.contentItem, "backupEnabledSwitch");
        const interval = findChild(dialog.contentItem, "backupIntervalCard");
        verify(toggle && interval);

        mouseClick(toggle);
        mouseClick(toggle);
        mouseClick(toggle);
        tryCompare(interval, "visible", false);

        mouseClick(toggle);
        tryCompare(interval, "visible", true);
        compare(dialog.viewModel.temporaryBackupInterval, 75);
        verify(presets(dialog.contentItem).every(button => !button.checked));
    }

    function test_disabledPresetsLeaveKeyboardFocusToLocation(): void {
        const dialog = makeControl();
        const buttons = presets(dialog.contentItem);
        const toggle = findChild(dialog.contentItem, "backupEnabledSwitch");
        const location = findChild(dialog.contentItem, "backupOpenLocationButton");
        verify(toggle && location);
        buttons[0].forceActiveFocus();
        verify(buttons[0].activeFocus);

        dialog.viewModel.temporaryBackupEnabled = false;
        verify(buttons.every(button => !button.enabled && !button.activeFocus));
        keyClick(Qt.Key_Space);
        compare(dialog.viewModel.temporaryBackupInterval, 75);

        toggle.forceActiveFocus();
        keyClick(Qt.Key_Tab);
        verify(location.activeFocus);
        verify(location.enabled);
        const clicked = makeSpy(location, "clicked");
        keyClick(Qt.Key_Space);
        compare(clicked.count, 1);
    }

    function test_presetLabelsWrap_data() {
        return [
            {
                tag: "words",
                label: "A much longer translated interval label"
            },
            {
                tag: "unbroken-word",
                label: "AnUnbrokenTranslatedIntervalLabelThatMustWrap"
            },
        ];
    }

    function test_presetLabelsWrap(data): void {
        const dialog = makeControl();
        const buttons = presets(dialog.contentItem);
        const originalHeight = buttons[0].height;
        buttons[0].text = data.label;
        tryVerify(() => buttons[0].height > originalHeight);
        const label = buttons[0].contentItem;
        verify(label instanceof Label);
        verify(label.lineCount > 1);
        verify(label.contentWidth <= label.width + bridge.pixelTolerance);
        verify(label.contentHeight <= label.height + bridge.pixelTolerance);
    }

    function test_longDirectoryScrollsWithoutMovingFooter(): void {
        const dialog = makeControl();
        const label = findChild(dialog.contentItem, "backupDirectoryLabel");
        verify(label);
        compare(label.text, dialog.viewModel.backupDirectory);
        const dialogSize = Qt.size(dialog.width, dialog.height);
        const ok = dialog.standardButton(Dialog.Ok);
        const footerY = ok.mapToItem(dialog.contentItem, 0, 0).y;
        label.text = "/" + "very-long-directory-name/".repeat(70);
        tryVerify(() => dialog.contentItem.contentHeight > dialog.contentItem.height);
        verify(label.lineCount > 1);
        verify(label.contentWidth <= label.width + bridge.pixelTolerance);
        verify(bridge.nearlyEqual(dialog.width, dialogSize.width), `a long directory must not resize the dialog width from ${dialogSize.width} to ${dialog.width}`);
        verify(bridge.nearlyEqual(dialog.height, dialogSize.height), `a long directory must not resize the dialog height from ${dialogSize.height} to ${dialog.height}`);
        const okY = ok.mapToItem(dialog.contentItem, 0, 0).y;
        verify(bridge.nearlyEqual(okY, footerY), `a long directory must not move the footer from ${footerY} to ${okY}`);
        verify(okY >= dialog.contentItem.height - bridge.pixelTolerance, "the footer must stay below the scrolling body");
        const labelBottom = () => label.mapToItem(dialog.contentItem, 0, label.height).y;
        verify(labelBottom() > dialog.contentItem.height + bridge.pixelTolerance, "the long directory should run past the body");
        const flickable = dialog.contentItem.contentItem;
        flickable.contentY = flickable.contentHeight - flickable.height;
        verify(labelBottom() <= dialog.contentItem.height + bridge.pixelTolerance, `scrolling to the end should reveal the whole directory, its bottom is at ${labelBottom()}`);
    }

    Component {
        id: _spy

        SignalSpy {}
    }

    Component {
        id: _dialog

        MpvqcBackupDialog {
            popupType: Popup.Item
        }
    }
}
