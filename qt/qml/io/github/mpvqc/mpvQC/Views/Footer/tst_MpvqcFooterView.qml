// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcFooterView"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    function init(): void {
        bridge.resetState();
    }

    function makeControl(properties = {}): MpvqcFooterView {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function setPercentageShown(control: MpvqcFooterView, enabled: bool): void {
        if (control.viewModel.showPercentage !== enabled) {
            control.viewModel.togglePercentage();
        }
        compare(control.viewModel.showPercentage, enabled);
    }

    function openContextMenuItem(control: Item, menuItem: string): var {
        const button = findChild(control, "contextMenuButton");
        mouseClick(button, button.width / 2, button.height / 2);
        tryVerify(() => findChild(control, menuItem) !== null);
        return findChild(control, menuItem);
    }

    function test_commentCountLabel_data(): var {
        return [
            {
                tag: "hidden",
                selectedIndex: 0,
                total: 0,
                visible: false,
                expected: ""
            },
            {
                tag: "1 of 1",
                selectedIndex: 0,
                total: 1,
                visible: true,
                expected: "1/1"
            },
            {
                tag: "1 of 3",
                selectedIndex: 0,
                total: 3,
                visible: true,
                expected: "1/3"
            },
            {
                tag: "2 of 3",
                selectedIndex: 1,
                total: 3,
                visible: true,
                expected: "2/3"
            },
            {
                tag: "3 of 3",
                selectedIndex: 2,
                total: 3,
                visible: true,
                expected: "3/3"
            },
        ];
    }

    function test_commentCountLabel(data): void {
        const control = makeControl({
            selectedCommentIndex: data.selectedIndex,
            totalCommentCount: data.total
        });

        const label = findChild(control, "commentCountLabel");
        compare(label.visible, data.visible);
        if (data.visible) {
            compare(label.text, data.expected);
        }
    }

    function test_labelsStayBlankWithoutVideo_data(): var {
        return [
            {
                tag: "default format",
                menuItem: "defaultFormatMenuItem"
            },
            {
                tag: "current time",
                menuItem: "currentTimeMenuItem"
            },
            {
                tag: "remaining time",
                menuItem: "remainingTimeMenuItem"
            },
            {
                tag: "hide time",
                menuItem: "hideTimeMenuItem"
            },
            {
                tag: "progress in percent",
                menuItem: "percentMenuItem"
            },
        ];
    }

    function test_labelsStayBlankWithoutVideo(data): void {
        const control = makeControl();
        setPercentageShown(control, false);

        const timeLabel = findChild(control, "timeLabel");
        const percentLabel = findChild(control, "percentLabel");
        verify(!timeLabel.visible);
        verify(!percentLabel.visible);
        compare(timeLabel.text, "");

        const menuItem = openContextMenuItem(control, data.menuItem);
        mouseClick(menuItem, menuItem.width / 2, menuItem.height / 2);

        verify(!timeLabel.visible);
        compare(timeLabel.text, "");
        verify(!percentLabel.visible);

        const button = findChild(control, "contextMenuButton");
        mouseClick(button, button.width / 2, button.height / 2);
        tryVerify(() => menuItem.visible);
        verify(menuItem.checked);
    }

    function test_contextMenuDrivesLabelsOverLoadedVideo(): void {
        const control = makeControl();
        bridge.loadVideo({
            duration: 125,
            timePos: 65,
            timeRemaining: 60,
            percentPos: 42
        });

        const timeLabel = findChild(control, "timeLabel");
        const percentLabel = findChild(control, "percentLabel");
        tryVerify(() => timeLabel.visible);
        compare(timeLabel.text, "01:05/02:05");
        verify(percentLabel.visible);
        compare(percentLabel.text, "42%");

        const currentTimeItem = openContextMenuItem(control, "currentTimeMenuItem");
        mouseClick(currentTimeItem, currentTimeItem.width / 2, currentTimeItem.height / 2);

        tryCompare(timeLabel, "text", "01:05");
        verify(timeLabel.visible);

        const percentItem = openContextMenuItem(control, "percentMenuItem");
        mouseClick(percentItem, percentItem.width / 2, percentItem.height / 2);

        tryVerify(() => !percentLabel.visible);
        verify(timeLabel.visible);
        compare(timeLabel.text, "01:05");
    }

    Component {
        id: objectUnderTest

        MpvqcFooterView {
            selectedCommentIndex: 0
            totalCommentCount: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
        }
    }
}
