// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtTest

TestCase {
    id: testCase

    name: "MpvqcWizardStepScrollView"
    width: 400
    height: 400
    visible: true
    when: windowShown

    readonly property int viewportHeight: 200

    function makeControl(contentHeight: real): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            scrolledHeight: contentHeight
        });
        verify(control);
        waitForRendering(control);
        return control;
    }

    function scrimOpacities(control: Item): var {
        const top = findChild(control, "topScrim");
        const bottom = findChild(control, "bottomScrim");
        verify(top, "topScrim not found");
        verify(bottom, "bottomScrim not found");
        return {
            top: top.opacity,
            bottom: bottom.opacity
        };
    }

    function test_scrollToTopReturnsToTheStart(): void {
        const control = makeControl(600);

        control.contentItem.contentY = 120;
        control.scrollToTop();

        compare(control.contentItem.contentY, 0);
    }

    function test_theEdgeCueIsGoneAtTheEdgeItPointsAt(): void {
        const control = makeControl(600);

        compare(scrimOpacities(control).top, 0);
        verify(scrimOpacities(control).bottom > 0, "overflow below should be cued");

        control.contentItem.contentY = control.contentHeight - control.contentItem.height;
        waitForRendering(control);

        verify(scrimOpacities(control).top > 0, "overflow above should be cued");
        compare(scrimOpacities(control).bottom, 0);
    }

    function test_contentThatFitsIsNeverCued(): void {
        const control = makeControl(testCase.viewportHeight / 2);

        compare(scrimOpacities(control).top, 0);
        compare(scrimOpacities(control).bottom, 0);
    }

    function test_scrollingStopsAtTheEnd(): void {
        const control = makeControl(600);

        control.contentItem.flick(0, -2000);
        tryVerify(() => !control.contentItem.moving);

        compare(control.contentItem.contentY, control.contentHeight - control.contentItem.height);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardStepScrollView {
            property alias scrolledHeight: _content.implicitHeight

            width: 300
            height: testCase.viewportHeight

            Rectangle {
                id: _content

                color: "red"

                Layout.fillWidth: true
            }
        }
    }
}
