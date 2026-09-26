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
        AppFontHost {}
    }

    readonly property Component mirroredObjectUnderTest: Component {
        AppFontHost {
            LayoutMirroring.enabled: true
            LayoutMirroring.childrenInherit: true
        }
    }

    readonly property string _pathologicalTypeName: "A".repeat(400)

    // The calculator measures the application font, which the app window hands down and the test window does not.
    component AppFontHost: Control {
        readonly property MpvqcTableView table: contentItem as MpvqcTableView

        width: testCase.width
        height: testCase.height
        font: MpvqcFonts.applicationFont

        contentItem: MpvqcTableView {
            backupEnabled: false
        }
    }

    function makeControl(component: Component, commentType: string): MpvqcTableView {
        _helpers.bridge.resetComments();
        const host = createTemporaryObject(component, testCase) as AppFontHost;
        verify(host);
        _helpers.bridge.importComments([
            {
                "time": 1000,
                "commentType": commentType,
                "comment": "Comment 1"
            }
        ]);
        waitForRendering(host);
        return host.table;
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

        const typeLabel = _typeLabel(control);
        tryCompare(typeLabel, "width", control.width / 3);
        tryVerify(() => typeLabel.truncated);

        const commentLabel = _commentLabel(control);
        verify(commentLabel.width > 100);
    }

    function test_normalMeasuredWidthRendersUnclamped(): void {
        const control = makeControl(objectUnderTest, "Comment Type 1");

        const typeLabel = _typeLabel(control);
        compare(typeLabel.width, MpvqcLabelWidthCalculator.commentTypesLabelWidth + typeLabel.leftPadding + typeLabel.rightPadding);
        verify(!typeLabel.truncated);
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
