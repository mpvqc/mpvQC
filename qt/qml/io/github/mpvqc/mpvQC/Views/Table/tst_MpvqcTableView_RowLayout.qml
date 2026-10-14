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

    function _rows(): list<Item> {
        const list = control.commentList;
        return Array.from({
            length: list.count
        }, (_, row) => list.itemAtIndex(row));
    }

    function _rowsAreStacked(): bool {
        const rows = _rows();
        return rows.every(row => row !== null) && _helpers.bridge.nearlyEqual(rows[0].y, 0) && _helpers.bridge.stackedWithoutGaps(rows);
    }

    function _rowsHeight(): real {
        return _rows().reduce((height, row) => height + row.height, 0);
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
        tryVerify(() => _rowsAreStacked(), 1000, "rows left gaps or overlaps after the scroll bar vanished");

        control.viewModel.undo();
        tryVerify(() => _scrollBarShows(), 1000, "scroll bar should come back with the undo");
        tryVerify(() => _rowsAreStacked(), 1000, "rows left gaps or overlaps after the scroll bar came back");
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

    function test_deletingLastRowLeavesNoBackgroundBelowRows_data(): list<var> {
        return [
            {
                tag: "unscrolled",
                height: 4000,
                scrolled: false
            },
            {
                tag: "scrolled",
                height: 400,
                scrolled: true
            }
        ];
    }

    function test_deletingLastRowLeavesNoBackgroundBelowRows(data): void {
        const list = control.commentList;
        const lastRow = list.count - 1;
        control.height = data.height;
        if (data.scrolled) {
            list.positionViewAtEnd();
            verify(list.contentY > 0, "list should scroll");
        }
        tryVerify(() => list.itemAtIndex(lastRow) !== null, 1000, "last row not built");

        // A leftover background shows once the removed row goes to the pool, after its remove transition
        const pooled = createTemporaryObject(_helpers.signalSpy, testCase, {
            target: list.itemAtIndex(lastRow).ListView,
            signalName: "pooled"
        });
        verify(pooled);

        control.viewModel.removeRow(lastRow);
        tryVerify(() => pooled.count === 1, 1000, "removed row not pooled");

        const backgrounds = list.contentItem.children.filter(child => child.objectName === "rowBackground");
        verify(backgrounds.length > 0, "no row backgrounds found");
        const contentEnd = list.originY + list.contentHeight;
        verify(!backgrounds.some(background => background.visible && background.y >= contentEnd - _helpers.bridge.pixelTolerance), "a row background stays below the rows");
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
