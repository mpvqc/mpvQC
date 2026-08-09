// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls // qmllint disable unused-imports
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 200
    visible: true
    when: windowShown
    name: "MpvqcWizardSubtitlesStepDelegate"

    function makeControl(properties = {}): Item {
        const delegate = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(delegate);
        waitForRendering(delegate);
        return delegate;
    }

    function test_labelShowsFilename(): void {
        const delegate = makeControl();
        const label = findChild(delegate, "label");
        verify(label);
        compare(label.text, "foobar.srt");
    }

    function test_rowTooltipShowsFullPath(): void {
        const delegate = makeControl();
        compare(delegate.ToolTip.text, "/subtitles/foobar.srt");
    }

    function test_checkedRowKeepsThePlainBackground(): void {
        const delegate = makeControl({
            isChecked: true
        });
        compare(delegate.background.color.a, 0);
    }

    function test_longFilenameWrapsAndTheRowGrowsToFitIt(): void {
        const delegate = makeControl({
            filename: "[Group] A Very Long Release Name Nobody Should Ever Have To Read In Full 01v2 (BD 1080p HEVC FLAC) [DEADBEEF].srt"
        });
        const label = findChild(delegate, "label");
        verify(label);
        verify(label.lineCount > 1);
        verify(delegate.height >= label.contentHeight);
    }

    function test_rowMirrorsUnderRightToLeftLayouts(): void {
        const delegate = makeControl({
            "LayoutMirroring.enabled": true,
            "LayoutMirroring.childrenInherit": true
        });
        const indicator = findChild(delegate, "checkIndicator");
        const label = findChild(delegate, "label");
        verify(indicator);
        verify(label);
        verify(indicator.x > label.x);
        compare(label.effectiveHorizontalAlignment, Text.AlignRight);
    }

    function test_indicatorReflectsIsChecked_data(): list<var> {
        return [
            {
                tag: "checked",
                isChecked: true
            },
            {
                tag: "unchecked",
                isChecked: false
            },
        ];
    }

    function test_indicatorReflectsIsChecked(data): void {
        const delegate = makeControl({
            isChecked: data.isChecked
        });
        const indicator = findChild(delegate, "checkIndicator");
        verify(indicator);
        compare(indicator.checked, data.isChecked);
    }

    function test_clickingAnywhereOnTheRowClicksTheRow_data(): list<var> {
        return [
            {
                tag: "on-the-indicator",
                childName: "checkIndicator"
            },
            {
                tag: "on-the-label",
                childName: "label"
            },
        ];
    }

    function test_clickingAnywhereOnTheRowClicksTheRow(data): void {
        const delegate = makeControl();
        const spy = createTemporaryObject(clickedSpy, testCase, {
            target: delegate
        });
        verify(spy);
        mouseClick(findChild(delegate, data.childName));
        compare(spy.count, 1);
    }

    Component {
        id: clickedSpy

        SignalSpy {
            signalName: "clicked"
        }
    }

    Component {
        id: objectUnderTest

        MpvqcWizardSubtitlesStepDelegate {
            width: testCase.width

            index: 0
            filename: "foobar.srt"
            fullPath: "/subtitles/foobar.srt"
            isChecked: false
        }
    }
}
