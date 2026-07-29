// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::SearchBoxPosition"

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _expect: _helpers.expect
    readonly property alias _find: _helpers.find
    readonly property alias _wait: _helpers.wait

    readonly property int timeout: 2000

    property var control: null

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function init(): void {
        control = _helpers.makeControl();
        control.commentList.currentIndex = 0;
        waitForRendering(control);

        _helpers.bridge.importComments([
            {
                "time": 0,
                "commentType": "Comment Type 1",
                "comment": "some comment"
            },
        ]);
        waitForRendering(control);

        keyPress(Qt.Key_F, Qt.ControlModifier);
        _wait.searchBoxOpened(control);
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
        _wait.searchBoxClosed(control);
        _expect.hasActiveFocus(control);

        control.height = 300;
        waitForRendering(control);

        keyPress(Qt.Key_F, Qt.ControlModifier);
        _wait.searchBoxOpened(control);

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

    // The override covers the whole box while a drag is on or a modal popup is open.
    // Hover delivery freezes during an exclusive grab, so hovered is not asserted here.
    function _expectOverrideCursor(cursor: int, phase: string): void {
        const popup = _find.searchBoxPopup(control);
        const handler = testCase.findChild(popup, "cursorOverrideHandler");
        verify(handler, "cursorOverrideHandler");
        compare(popup._overrideCursor, cursor, `${phase}: override claim`);
        compare(handler.cursorShape, cursor, phase);
    }

    function test_grabSpotCursors_data(): list<var> {
        return [
            {
                tag: "search-icon",
                widget: () => _find.searchIconLabel(control),
                cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler")
            },
            {
                tag: "status-label",
                widget: () => _find.searchStatusLabel(control),
                cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler")
            },
            {
                tag: "previous-button-disabled",
                widget: () => _find.searchPreviousButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "previousButtonCursorHandler")
            },
            {
                tag: "next-button-disabled",
                widget: () => _find.searchNextButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "nextButtonCursorHandler")
            },
        ];
    }

    function test_grabSpotCursors(data): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);
        const widget = data.widget();
        const cursorHandler = data.cursorHandler(widget);

        // Map widget center to dragArea coordinates
        const widgetCenter = widget.mapToItem(dragArea, widget.width / 2, widget.height / 2);
        const cx = widgetCenter.x;
        const cy = widgetCenter.y;

        // Hover → open hand, no scale
        mouseMove(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.OpenHandCursor, "hover");
        fuzzyCompare(popup.scale, 1, 0.02, "hover-scale");

        // Press → closed hand, scaled up
        mousePress(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "press");
        tryVerify(() => popup.scale > 1.037, 500, "press-scale-up");

        // Release without moving → back to open hand and scale 1
        mouseRelease(dragArea, cx, cy);
        compare(cursorHandler.cursorShape, Qt.OpenHandCursor, "release");
        tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 500, "release-scale-down");

        // Drag → the override handler takes over with a closed hand, scaled up
        mousePress(dragArea, cx, cy);
        waitForRendering(control);
        compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "drag-press");

        mouseMove(dragArea, cx, cy - 100);
        waitForRendering(control);
        _expectOverrideCursor(Qt.ClosedHandCursor, "drag-move");
        tryVerify(() => popup.scale > 1.037, 500, "drag-scale-up");

        mouseRelease(dragArea, cx, cy - 100);
        compare(cursorHandler.cursorShape, Qt.OpenHandCursor, "drag-release");
        tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 2000, "drag-release-scale-down");
    }

    function test_textFieldPressDoesNotPickTheBoxUp(): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);
        const textField = _find.searchTextField(control);

        const center = textField.mapToItem(dragArea, textField.width / 2, textField.height / 2);

        // The press is for the text field itself, so nothing lifts
        mouseMove(dragArea, center.x, center.y);
        mousePress(dragArea, center.x, center.y);
        verify(!popup._shouldScaleUp, "press");

        // Only an actual drag picks the box up, and then the override covers the text field too
        mouseMove(dragArea, center.x, center.y - 100);
        waitForRendering(control);
        _expectOverrideCursor(Qt.ClosedHandCursor, "drag-move");
        tryVerify(() => popup.scale > 1.037, 500, "drag-scale-up");

        mouseRelease(dragArea, center.x, center.y - 100);
        verify(popup._overrideCursor === undefined, "the override retires once the drag ends");
    }

    function test_cursorBehaviorNavButtonsEnabled_data(): list<var> {
        return [
            {
                tag: "previous-button-enabled",
                widget: () => _find.searchPreviousButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "previousButtonCursorHandler"),
                needsMultipleResults: true
            },
            {
                tag: "next-button-enabled",
                widget: () => _find.searchNextButton(control),
                cursorHandler: widget => testCase.findChild(widget.parent, "nextButtonCursorHandler"),
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
            _helpers.bridge.importComments([
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
            _helpers.typeWord("some");
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

        // Drag → the override handler takes over with a closed hand
        mousePress(dragArea, cx, cy);
        waitForRendering(control);
        mouseMove(dragArea, cx, cy - 100);
        waitForRendering(control);
        _expectOverrideCursor(Qt.ClosedHandCursor, "drag-move-enabled");

        mouseRelease(dragArea, cx, cy - 100);
        compare(cursorHandler.cursorShape, Qt.ArrowCursor, "drag-release-enabled");
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
