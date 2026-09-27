// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCommentTypesDialogLayout"
    width: 600
    height: 900
    visible: true
    when: windowShown

    readonly property TestHelpers helper: TestHelpers {
        testCase: testCase
    }

    function init(): void {
        failOnWarning(/.*(TypeError|Unable to assign|Binding loop).*/);
        helper.bridge.resetState();
    }

    function test_draftFieldTextStartsAtTheLeadingEdge_data(): var {
        return [
            {
                tag: "latin-draft",
                draft: "ZZZ Draft"
            },
            {
                tag: "hebrew-draft",
                draft: "טיוטה"
            }
        ];
    }

    function test_draftFieldTextStartsAtTheLeadingEdge(data): void {
        const dialog = helper.makeDialog();
        const field = helper.textField(dialog);
        field.text = data.draft;
        for (const mirrored of [false, true, false]) {
            dialog.contentItem.LayoutMirroring.enabled = mirrored;
            verify(waitForPolish(dialog.contentItem.Window.window), "dialog layout should settle after mirroring");
            tryCompare(field, "effectiveHorizontalAlignment", mirrored ? Text.AlignRight : Text.AlignLeft);
            tryVerify(() => {
                const start = field.positionToRectangle(0).x;
                const end = field.positionToRectangle(field.length).x;
                const edge = mirrored ? Math.max(start, end) : Math.min(start, end);
                // positionToRectangle() reports text-layout coordinates, without padding.
                const expected = mirrored ? field.width - field.leftPadding - field.rightPadding : 0;
                return Math.abs(edge - expected) <= 1;
            }, 1000, "draft text should render at the leading edge");
        }
    }

    function test_eightCompleteRowsStayVisible_data(): var {
        return [
            {
                tag: "no-feedback",
                draft: "",
                feedback: false
            },
            {
                tag: "bracket-feedback",
                draft: "ZZZ [Bracketed]",
                feedback: true
            }
        ];
    }

    function test_eightCompleteRowsStayVisible(data): void {
        const dialog = helper.makeDialog();
        for (let i = 1; i <= 5; i++) {
            helper.addType(dialog, `ZZZ Long Type ${i} with a label long enough to reach the delete button`);
        }
        const list = helper.listView(dialog);
        list.positionViewAtBeginning();
        const addCard = helper.find(dialog.contentItem, "commentTypesAddCard");
        const heightWithoutFeedback = dialog.height;
        const listTopWithoutFeedback = list.mapToItem(dialog.contentItem, 0, 0).y;

        helper.textField(dialog).text = data.draft;
        verify(waitForPolish(dialog.contentItem.Window.window));

        compare(helper.validationLabel(dialog).text !== "", data.feedback);
        compare(dialog.contentHeight, MpvqcConstants.mediumDialogContentHeight);
        compare(dialog.height, heightWithoutFeedback, "feedback must not resize the dialog");
        compare(list.mapToItem(dialog.contentItem, 0, 0).y, listTopWithoutFeedback, "feedback must not move the list");
        verify(list.height >= 8 * MpvqcConstants.listRowHeight);
        verify(helper.verticallyInside(list, dialog.contentItem));
        verify(helper.verticallyInside(addCard, dialog.contentItem));
        verify(helper.verticallyInside(helper.find(dialog.contentItem, "commentTypesListCard"), dialog.contentItem));
        verify(addCard.mapToItem(dialog.contentItem, 0, addCard.height).y <= listTopWithoutFeedback, "the add card must sit above the list");
        for (let i = 0; i < 8; i++) {
            verify(helper.verticallyInside(helper.rowPart(list, i, "commentTypeDelegate"), list), `row ${i} must be completely visible`);
        }
    }
}
