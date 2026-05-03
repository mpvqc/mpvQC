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

    Component {
        id: objectUnderTest

        Item {
            width: testCase.width
            height: testCase.height

            MpvqcFooterView {
                objectName: "footer"
                selectedCommentIndex: 0
                totalCommentCount: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
            }
        }
    }

    function makeControl(props): var {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        const footer = findChild(control, "footer");
        for (const key in (props ?? {})) {
            footer[key] = props[key];
        }
        waitForRendering(control);
        return control;
    }

    function configureStatusbar(control: Item, enabled: bool): void {
        const footer = findChild(control, "footer");
        if (footer.viewModel.statusbarPercentage !== enabled) {
            footer.viewModel.toggleStatusbarPercentage();
        }
        compare(footer.viewModel.statusbarPercentage, enabled);
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
        configureStatusbar(control, false);

        const timeLabel = findChild(control, "timeLabel");
        const percentLabel = findChild(control, "percentLabel");
        verify(!timeLabel.visible);
        verify(!percentLabel.visible);
        compare(timeLabel.text, "");

        const button = findChild(control, "contextMenuButton");
        mouseClick(button, button.width / 2, button.height / 2);

        tryVerify(() => findChild(control, data.menuItem) !== null);
        const menuItem = findChild(control, data.menuItem);
        mouseClick(menuItem, menuItem.width / 2, menuItem.height / 2);

        verify(!timeLabel.visible);
        compare(timeLabel.text, "");
        verify(!percentLabel.visible);

        mouseClick(button, button.width / 2, button.height / 2);
        tryVerify(() => menuItem.visible);
        verify(menuItem.checked);
    }

    function test_timeLabelWithVideoLoaded_data(): var {
        return [
            {
                tag: "default format",
                menuItem: "defaultFormatMenuItem",
                initialTimeFormat: MpvqcTimeFormat.TimeFormat.EMPTY,
                expectedText: "01:05/02:05"
            },
            {
                tag: "current time",
                menuItem: "currentTimeMenuItem",
                initialTimeFormat: MpvqcTimeFormat.TimeFormat.EMPTY,
                expectedText: "01:05"
            },
            {
                tag: "remaining time",
                menuItem: "remainingTimeMenuItem",
                initialTimeFormat: MpvqcTimeFormat.TimeFormat.EMPTY,
                expectedText: "-01:00"
            },
            {
                tag: "hide time",
                menuItem: "hideTimeMenuItem",
                initialTimeFormat: MpvqcTimeFormat.TimeFormat.CURRENT_TIME,
                expectedText: ""
            },
        ];
    }

    function test_timeLabelWithVideoLoaded(data): void {
        const control = makeControl();
        const footer = findChild(control, "footer");

        footer.viewModel.setVideoLoaded(true);
        footer.viewModel.setDuration(125.0);
        footer.viewModel.setTimePos(65);
        footer.viewModel.setTimeRemaining(60);
        footer.viewModel.setPercentPos(42);
        footer.viewModel.timeFormat = data.initialTimeFormat;
        configureStatusbar(control, true);

        const timeLabel = findChild(control, "timeLabel");
        const percentLabel = findChild(control, "percentLabel");

        const button = findChild(control, "contextMenuButton");
        mouseClick(button, button.width / 2, button.height / 2);

        tryVerify(() => findChild(control, data.menuItem) !== null);
        const menuItem = findChild(control, data.menuItem);
        mouseClick(menuItem, menuItem.width / 2, menuItem.height / 2);

        compare(timeLabel.visible, data.expectedText !== "");
        compare(timeLabel.text, data.expectedText);
        verify(percentLabel.visible);
        compare(percentLabel.text, "42%");

        mouseClick(button, button.width / 2, button.height / 2);
        tryVerify(() => menuItem.visible);
        verify(menuItem.checked);
    }

    function test_percentLabelToggleWithVideoLoaded_data(): var {
        return [
            {
                tag: "off to on",
                initial: false,
                expectedVisible: true,
                expectedChecked: true
            },
            {
                tag: "on to off",
                initial: true,
                expectedVisible: false,
                expectedChecked: false
            },
        ];
    }

    function test_percentLabelToggleWithVideoLoaded(data): void {
        const control = makeControl();
        const footer = findChild(control, "footer");

        footer.viewModel.setVideoLoaded(true);
        footer.viewModel.setPercentPos(42);
        configureStatusbar(control, data.initial);

        const percentLabel = findChild(control, "percentLabel");

        const button = findChild(control, "contextMenuButton");
        mouseClick(button, button.width / 2, button.height / 2);

        tryVerify(() => findChild(control, "percentMenuItem") !== null);
        const menuItem = findChild(control, "percentMenuItem");
        mouseClick(menuItem, menuItem.width / 2, menuItem.height / 2);

        compare(percentLabel.visible, data.expectedVisible);
        if (data.expectedVisible) {
            compare(percentLabel.text, "42%");
        }

        mouseClick(button, button.width / 2, button.height / 2);
        tryVerify(() => menuItem.visible);
        compare(menuItem.checked, data.expectedChecked);
    }
}
