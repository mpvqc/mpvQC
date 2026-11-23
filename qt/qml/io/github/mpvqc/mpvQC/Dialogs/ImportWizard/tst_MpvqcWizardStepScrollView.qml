// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    name: "MpvqcWizardStepScrollView"
    width: 400
    height: 400
    visible: true
    when: windowShown

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}
    readonly property int viewportHeight: 200

    function makeControl(contentHeight: real): MpvqcWizardStepScrollView {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            scrolledHeight: contentHeight
        });
        verify(control);
        waitForRendering(control);
        return control;
    }

    function viewport(control: MpvqcWizardStepScrollView): Flickable {
        return control.contentItem as Flickable;
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

        viewport(control).contentY = 120;
        control.scrollToTop();

        compare(viewport(control).contentY, 0);
    }

    function test_theEdgeCueIsGoneAtTheEdgeItPointsAt(): void {
        const control = makeControl(600);

        compare(scrimOpacities(control).top, 0);
        verify(scrimOpacities(control).bottom > 0, "overflow below should be cued");

        viewport(control).contentY = control.contentHeight - viewport(control).height;
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

        viewport(control).flick(0, -2000);
        tryVerify(() => !viewport(control).moving);

        verify(bridge.atScrollEnd(viewport(control)), `the flick should stop at the end, not at ${viewport(control).contentY}`);
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
