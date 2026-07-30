// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::TypeLabelClamp"

    readonly property int timeout: 2000

    readonly property Component objectUnderTest: Component {
        MpvqcTableView {
            backupEnabled: false

            height: testCase.height
            width: testCase.width
        }
    }

    readonly property Component mirroredObjectUnderTest: Component {
        MpvqcTableView {
            backupEnabled: false

            height: testCase.height
            width: testCase.width

            LayoutMirroring.enabled: true
            LayoutMirroring.childrenInherit: true
        }
    }

    readonly property string _pathologicalTypeName: "A".repeat(400)

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function init(): void {
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 150;
    }

    function makeControl(component: Component, commentType: string): var {
        _helpers.bridge.resetComments();
        const control = createTemporaryObject(component, testCase);
        verify(control);
        _helpers.bridge.importComments([
            {
                "time": 1000,
                "commentType": commentType,
                "comment": "Comment 1"
            }
        ]);
        waitForRendering(control);
        return control;
    }

    function _typeLabel(control: MpvqcTableView): Label {
        const delegate = control.commentList.itemAtIndex(0);
        return findChild(delegate, "commentTypeLabel") as Label;
    }

    function _commentLabel(control: MpvqcTableView): Label {
        const delegate = control.commentList.itemAtIndex(0);
        return findChild(delegate, "commentLabel") as Label;
    }

    function test_hugeMeasuredWidthClampsToTableFraction_data(): var {
        return [
            {
                tag: "ltr",
                component: objectUnderTest
            },
            {
                tag: "rtl",
                component: mirroredObjectUnderTest
            },
        ];
    }

    function test_hugeMeasuredWidthClampsToTableFraction(data: var): void {
        const control = makeControl(data.component, _pathologicalTypeName);

        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 100000;

        const typeLabel = _typeLabel(control);
        tryCompare(typeLabel, "width", control.width / 3);
        tryVerify(() => typeLabel.truncated);

        const commentLabel = _commentLabel(control);
        verify(commentLabel.width > 100);
    }

    function test_normalMeasuredWidthRendersUnclamped(): void {
        const control = makeControl(objectUnderTest, "Comment Type 1");

        const typeLabel = _typeLabel(control);
        compare(typeLabel.width, 150 + typeLabel.leftPadding + typeLabel.rightPadding);
        verify(!typeLabel.truncated);
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
