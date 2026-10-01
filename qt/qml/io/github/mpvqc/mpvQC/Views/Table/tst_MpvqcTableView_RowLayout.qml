// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    width: 800
    height: 800
    visible: true
    when: windowShown
    name: "MpvqcTableView::RowLayout"

    // Comments that wrap at some of the widths below, so a row's height depends on the scroll bar.
    // The long types make the type column as wide as it gets. The removed rows are tall, so taking one
    // away frees more height than the scroll bar costs the other rows in extra lines, whatever the font
    readonly property list<var> comments: [["Note", "Comment from the long-named document"], ["Q&A", "x"], ["Spelling", "Comment from the v1 document"], ["Spelling", "First comment from the classic document"], ["Continuity and consistency across episodes", "A type no default config lists"], ["Note", tallComment], ["VeryLongType".repeat(33), "A four hundred character type"], ["Note", "The video this document names does not exist"], ["Timing", "Second comment from the classic document"], ["Phrasing", "Second comment from the v1 document"], ["Note", "Third comment from the classic document"], ["Note", tallComment]]
    readonly property string tallComment: "A comment long enough to span several lines. ".repeat(8)
    readonly property int removedRow: 5

    property var control: null

    function init(): void {
        control = _helpers.makeRealCommentTypesControl();
        _helpers.bridge.resetComments();
        _helpers.bridge.importComments(comments.map((comment, index) => ({
                    "time": index * 1000,
                    "commentType": comment[0],
                    "comment": comment[1]
                })));
        waitForRendering(control);
    }

    function cleanup(): void {
        control.destroy();
        control = null;
    }

    function _scrollBarShows(): bool {
        return control.commentList.ScrollBar.vertical.isShown;
    }

    function _rowsAreStacked(): bool {
        const list = control.commentList;
        let expectedY = 0;
        for (let row = 0; row < list.count; row++) {
            const item = list.itemAtIndex(row);
            if (!item || Math.abs(item.y - expectedY) > 0.5) {
                return false;
            }
            expectedY += item.height;
        }
        return true;
    }

    function _rowsHeight(): real {
        const list = control.commentList;
        let height = 0;
        for (let row = 0; row < list.count; row++) {
            height += list.itemAtIndex(row).height;
        }
        return height;
    }

    /**
     *  Leaves the list a sliver too short for its rows, so the scroll bar shows and removing `row`
     *  takes it away. The content height is only an estimate until every row exists, so the rows
     *  are measured in a list tall enough to hold them all.
     */
    function _fitAllRowsBut(row: int): void {
        const list = control.commentList;
        control.height = 4000;
        tryVerify(() => !_scrollBarShows() && _rowsAreStacked(), 1000, "rows not stacked in the tall list");

        control.height = _rowsHeight() - 2;
        tryVerify(() => _scrollBarShows(), 1000, "scroll bar should show in the short list");
        list.positionViewAtBeginning();
        tryVerify(() => _rowsAreStacked(), 1000, "rows not stacked in the short list");
        verify(_rowsHeight() - list.itemAtIndex(row).height <= list.height, "row too short to take the scroll bar away");
    }

    function test_rowsStayStackedWhenScrollBarComesAndGoes_data(): list<var> {
        return [470, 617].map(width => ({
                    tag: `width-${width}`,
                    width: width
                }));
    }

    function test_rowsStayStackedWhenScrollBarComesAndGoes(data): void {
        control.width = data.width;
        _fitAllRowsBut(removedRow);

        control.viewModel.removeRow(removedRow);
        tryVerify(() => !_scrollBarShows(), 1000, "scroll bar should vanish with the removal");
        wait(300);
        verify(_rowsAreStacked(), "rows left gaps or overlaps after the scroll bar vanished");

        control.viewModel.undo();
        tryVerify(() => _scrollBarShows(), 1000, "scroll bar should come back with the undo");
        wait(300);
        verify(_rowsAreStacked(), "rows left gaps or overlaps after the scroll bar came back");
    }

    function test_scrollBarFollowsRowThatMovesNoOtherRow(): void {
        const list = control.commentList;
        _fitAllRowsBut(list.count - 1);

        control.viewModel.removeRow(list.count - 1);
        tryVerify(() => !_scrollBarShows(), 1000, "scroll bar should vanish with the removal");

        // The last row comes back below every other row, so no transition runs
        control.viewModel.undo();
        tryVerify(() => _scrollBarShows(), 1000, "scroll bar should come back with the undo");
        tryVerify(() => _rowsAreStacked(), 1000, "rows left gaps or overlaps after the scroll bar came back");
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
