// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    readonly property int timeout: 2000

    TestHelpers {
        id: _helpers

        testCase: testCase
    }

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _expect: _helpers.expect
    readonly property alias _find: _helpers.find

    readonly property Component signalSpy: _helpers.signalSpy
    readonly property Component objectWithRealViewModel: _helpers.objectWithRealViewModel

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::SearchBoxPosition"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function makeControl(): var {
        return _helpers.makeControl();
    }

    function waitUntilEditControlOpened(control: MpvqcTableView): void {
        _helpers.waitUntilEditControlOpened(control);
    }

    function waitUntilEditControlClosed(control: MpvqcTableView): void {
        _helpers.waitUntilEditControlClosed(control);
    }

    function waitUntilContextMenuOpened(control: MpvqcTableView): void {
        _helpers.waitUntilContextMenuOpened(control);
    }

    function waitUntilContextMenuClosed(control: MpvqcTableView): void {
        _helpers.waitUntilContextMenuClosed(control);
    }

    function waitUntilMessageBoxOpened(control: MpvqcTableView): void {
        _helpers.waitUntilMessageBoxOpened(control);
    }

    function waitUntilMessageBoxClosed(control: MpvqcTableView): void {
        _helpers.waitUntilMessageBoxClosed(control);
    }

    function waitUntilSearchBoxOpened(control: MpvqcTableView): void {
        _helpers.waitUntilSearchBoxOpened(control);
    }

    function waitUntilSearchBoxClosed(control: MpvqcTableView): void {
        _helpers.waitUntilSearchBoxClosed(control);
    }

    function getCommentTypeItems(control: MpvqcTableView): list<Item> {
        return _helpers.getCommentTypeItems(control);
    }

    function typeWord(word: string): void {
        _helpers.typeWord(word);
    }

    property var control: null

    function init(): void {
        control = testCase.makeControl();
        control.commentList.currentIndex = 0;
        waitForRendering(control);

        control.commentList.model.import_comments([
            {
                "time": 0,
                "commentType": "Comment Type 1",
                "comment": "some comment"
            },
        ]);
        waitForRendering(control);

        keyPress(Qt.Key_F, Qt.ControlModifier);
        testCase.waitUntilSearchBoxOpened(control);
        _expect.hasSearchBoxOpen(control);
    }

    function cleanup(): void {
        control.destroy();
        control = null;
    }

    function _bottomY(): real {
        const popup = _find.searchBoxPopup(control);
        return control.height - popup.height - popup.edgeMarginVertical;
    }

    function test_initialPositionIsAtBottom(): void {
        const popup = _find.searchBoxPopup(control);
        fuzzyCompare(popup.y, _bottomY(), 1);
    }

    function test_sticksToBottomWhenParentShrinks(): void {
        const popup = _find.searchBoxPopup(control);

        control.height = control.height - 100;
        waitForRendering(control);

        tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
    }

    function test_sticksToBottomWhenParentGrows(): void {
        const popup = _find.searchBoxPopup(control);

        control.height = control.height + 100;
        waitForRendering(control);

        tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
    }

    function test_sticksToBottomThroughMultipleResizes(): void {
        const popup = _find.searchBoxPopup(control);

        for (const h of [300, 500, 200, 600]) {
            control.height = h;
            waitForRendering(control);
            tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
        }
    }

    function test_reopenedAtBottomAfterResize(): void {
        keyPress(Qt.Key_Escape);
        testCase.waitUntilSearchBoxClosed(control);
        _expect.hasActiveFocus(control);

        control.height = 300;
        waitForRendering(control);

        keyPress(Qt.Key_F, Qt.ControlModifier);
        testCase.waitUntilSearchBoxOpened(control);

        const popup = _find.searchBoxPopup(control);
        tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
    }

    function test_isDraggable(): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);
        const initialY = popup.y;

        mouseDrag(dragArea, dragArea.width / 2, dragArea.height / 2, 0, -80);
        waitForRendering(control);

        verify(popup.y < initialY - 20);
    }

    function test_snapsToBottomWhenShrunkPastDragPosition(): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);

        // Drag the popup away from the bottom
        mouseDrag(dragArea, dragArea.width / 2, dragArea.height / 2, 0, -80);
        waitForRendering(control);
        const draggedY = popup.y;
        verify(draggedY < _bottomY() - 20);

        // Shrink the parent so the popup's dragged position would be out of bounds
        control.height = draggedY + popup.height + popup.edgeMarginVertical - 10;
        waitForRendering(control);

        tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
    }

    function test_cursorBehavior_data(): list<var> {
        return [
            {
                tag: "search-icon",
                widget: () => _find.searchIconLabel(control),
                cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler"),
                hoverCursor: Qt.OpenHandCursor,
                pressCursor: Qt.ClosedHandCursor,
                scalesOnPress: true
            },
            {
                tag: "text-field",
                widget: () => _find.searchTextField(control),
                cursorHandler: widget => testCase.findChild(widget, "searchTextFieldCursorHandler"),
                hoverCursor: Qt.IBeamCursor,
                pressCursor: Qt.IBeamCursor,
                scalesOnPress: false
            },
            {
                tag: "status-label",
                widget: () => _find.searchStatusLabel(control),
                cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler"),
                hoverCursor: Qt.OpenHandCursor,
                pressCursor: Qt.ClosedHandCursor,
                scalesOnPress: true
            },
            {
                tag: "previous-button-disabled",
                widget: () => _find.searchPreviousButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "previousButtonDisabledCursorHandler"),
                hoverCursor: Qt.OpenHandCursor,
                pressCursor: Qt.ClosedHandCursor,
                scalesOnPress: true
            },
            {
                tag: "next-button-disabled",
                widget: () => _find.searchNextButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "nextButtonDisabledCursorHandler"),
                hoverCursor: Qt.OpenHandCursor,
                pressCursor: Qt.ClosedHandCursor,
                scalesOnPress: true
            },
        ];
    }

    function test_cursorBehavior(data): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);
        const widget = data.widget();
        const cursorHandler = data.cursorHandler(widget);

        // Map widget center to dragArea coordinates
        const widgetCenter = widget.mapToItem(dragArea, widget.width / 2, widget.height / 2);
        const cx = widgetCenter.x;
        const cy = widgetCenter.y;

        // Hover → expected cursor, no scale
        mouseMove(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, data.hoverCursor, "hover");
        fuzzyCompare(popup.scale, 1, 0.02, "hover-scale");

        // Press → cursor depends on widget, scale depends on widget
        mousePress(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, data.pressCursor, "press");
        if (data.scalesOnPress) {
            tryVerify(() => popup.scale > 1.037, 500, "press-scale-up");
        } else {
            fuzzyCompare(popup.scale, 1, 0.02, "press-no-scale");
        }

        // Release without moving → back to hover cursor and scale 1
        mouseRelease(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, data.hoverCursor, "release");
        if (data.scalesOnPress) {
            tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 500, "release-scale-down");
        }

        // Drag → closed hand throughout, scaled up
        mousePress(dragArea, cx, cy);
        waitForRendering(control);
        compare(cursorHandler.cursorShape, data.pressCursor, "drag-press");

        mouseMove(dragArea, cx, cy - 100);
        waitForRendering(control);
        compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "drag-move");
        tryVerify(() => popup.scale > 1.037, 500, "drag-scale-up");

        mouseRelease(dragArea, cx, cy - 100);
        compare(cursorHandler.cursorShape, data.hoverCursor, "drag-release");
        tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 2000, "drag-release-scale-down");
    }

    function test_cursorBehaviorNavButtonsEnabled_data(): list<var> {
        return [
            {
                tag: "previous-button-enabled",
                widget: () => _find.searchPreviousButton(control),
                cursorHandler: widget => testCase.findChild(widget, "previousButtonEnabledCursorHandler"),
                needsMultipleResults: true
            },
            {
                tag: "next-button-enabled",
                widget: () => _find.searchNextButton(control),
                cursorHandler: widget => testCase.findChild(widget, "nextButtonEnabledCursorHandler"),
                needsMultipleResults: true
            },
            {
                tag: "close-button",
                widget: () => _find.searchCloseButton(control),
                cursorHandler: widget => testCase.findChild(widget, "closeButtonCursorHandler"),
                needsMultipleResults: false
            },
        ];
    }

    function test_cursorBehaviorNavButtonsEnabled(data): void {
        if (data.needsMultipleResults) {
            // Import additional comments so search yields multiple results
            control.commentList.model.import_comments([
                {
                    "time": 1,
                    "commentType": "Comment Type 1",
                    "comment": "some comment"
                },
                {
                    "time": 2,
                    "commentType": "Comment Type 1",
                    "comment": "some comment"
                },
            ]);
            waitForRendering(control);

            // Type a query that matches multiple comments
            const textField = _find.searchTextField(control);
            mouseClick(textField);
            testCase.typeWord("some");
            waitForRendering(control);
        }

        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);
        const widget = data.widget();
        const cursorHandler = data.cursorHandler(widget);

        verify(widget.enabled, "button should be enabled");

        const widgetCenter = widget.mapToItem(dragArea, widget.width / 2, widget.height / 2);
        const cx = widgetCenter.x;
        const cy = widgetCenter.y;

        // Hover → arrow cursor
        mouseMove(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.ArrowCursor, "hover-enabled");

        // Press → arrow cursor
        mousePress(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.ArrowCursor, "press-enabled");
        fuzzyCompare(popup.scale, 1, 0.02, "press-no-scale");

        // Release
        mouseRelease(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.ArrowCursor, "release-enabled");

        // Drag → closed hand
        mousePress(dragArea, cx, cy);
        waitForRendering(control);
        mouseMove(dragArea, cx, cy - 100);
        waitForRendering(control);
        compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "drag-move-enabled");

        mouseRelease(dragArea, cx, cy - 100);
        compare(cursorHandler.cursorShape, Qt.ArrowCursor, "drag-release-enabled");
    }
}
