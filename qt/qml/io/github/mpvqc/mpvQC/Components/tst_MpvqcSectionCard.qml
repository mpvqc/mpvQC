// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcSectionCard"
    width: 400
    height: 400
    visible: true
    when: windowShown

    readonly property int expectedPadding: 20

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function makeControlWithTitleAction(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTestWithTitleAction, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function test_theTitleIsShown(): void {
        const control = makeControl({
            title: "Color scheme"
        });
        const title = findChild(control, "cardTitle");
        verify(title);
        compare(title.text, "Color scheme");
    }

    function test_theCardWearsTheSectionCardColorRole(): void {
        const control = makeControl();
        const card = findChild(control, "cardBackground");
        verify(card);
        tryCompare(card, "color", MpvqcAppearance.palette.sectionCard);
    }

    function test_theContentSitsInsideThePadding(): void {
        const control = makeControl();
        const content = findChild(control, "cardContent");
        verify(content);

        const topLeft = content.mapToItem(control, 0, 0);
        const bottomRight = content.mapToItem(control, content.width, content.height);

        compare(topLeft.x, testCase.expectedPadding);
        compare(control.width - bottomRight.x, testCase.expectedPadding);
        compare(control.implicitHeight - bottomRight.y, testCase.expectedPadding);
    }

    function test_withoutTitleActionsTheTitleSpansTheContentWidth(): void {
        const control = makeControl({
            title: "Color scheme"
        });
        const title = findChild(control, "cardTitle");
        verify(title);
        compare(title.width, control.width - 2 * testCase.expectedPadding);
    }

    function test_aTitleActionSitsAtTheTrailingEdgeOfTheTitleRow(): void {
        const control = makeControlWithTitleAction({
            title: "Subtitles"
        });
        const action = findChild(control, "cardTitleAction");
        verify(action);
        const title = findChild(control, "cardTitle");
        verify(title);

        const actionRight = action.mapToItem(control, action.width, 0);
        const titleLeft = title.mapToItem(control, 0, 0);

        compare(control.width - actionRight.x, testCase.expectedPadding);
        verify(titleLeft.x < actionRight.x - action.width);
    }

    Component {
        id: objectUnderTest

        MpvqcSectionCard {
            width: 300

            Rectangle {
                objectName: "cardContent"

                implicitHeight: 40

                Layout.fillWidth: true
            }
        }
    }

    Component {
        id: objectUnderTestWithTitleAction

        MpvqcSectionCard {
            width: 300

            titleActions: [
                Rectangle {
                    objectName: "cardTitleAction"

                    implicitWidth: 20
                    implicitHeight: 20
                }
            ]

            Rectangle {
                objectName: "cardContent"

                implicitHeight: 40

                Layout.fillWidth: true
            }
        }
    }
}
