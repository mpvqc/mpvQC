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
    name: "MpvqcTableView::SearchBoxStacking"

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _expect: _helpers.expect
    readonly property alias _find: _helpers.find
    readonly property alias _wait: _helpers.wait

    readonly property int timeout: 2000

    // Short enough that the search box reaches the rows, tall enough that editors open downward
    readonly property int _tableHeight: 330

    property var control: null

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function init(): void {
        control = _helpers.makeControl();
        _helpers.bridge.importComments(_fillerComments(5));
        control.height = _tableHeight;
        waitForRendering(control);

        keyPress(Qt.Key_F, Qt.ControlModifier);
        _wait.searchBoxOpened(control);
        _expect.hasSearchBoxOpen(control);
    }

    function cleanup(): void {
        control.destroy();
        control = null;
    }

    function _fillerComments(count: int): list<var> {
        const comments = [];
        for (let i = 0; i < count; ++i) {
            comments.push({
                "time": i * 100,
                "commentType": "Comment Type 1",
                "comment": `Filler ${i}`
            });
        }
        return comments;
    }

    // Global coordinates: on Windows a menu is its own window, and mapToItem does not cross windows
    function _globalBoundsOfSearchBox(): rect {
        const item = _find.searchBoxPopup(control).contentItem.parent;
        const topLeft = item.mapToGlobal(0, 0);
        return Qt.rect(topLeft.x, topLeft.y, item.width, item.height);
    }

    function _globalCenterOf(item: Item): point {
        return item.mapToGlobal(item.width / 2, item.height / 2);
    }

    function _covers(bounds: rect, point: point): bool {
        return point.x >= bounds.x && point.x <= bounds.x + bounds.width && point.y >= bounds.y && point.y <= bounds.y + bounds.height;
    }

    function _openEditor(clickPoint: point, editor: string): void {
        mouseDoubleClickSequence(control, clickPoint.x, clickPoint.y);
        _wait.editControlOpened(control);
        _expect.isEditorShowing(control, editor);
    }

    function _menuEntryOver(bounds: rect, row: int): var {
        const menu = _find.editCommentTypeMenu(control);
        const currentCommentType = control.getItem(row, "commentType");

        for (let i = menu.count - 1; i >= 0; --i) {
            const entry = menu.itemAt(i); // qmllint disable
            if (entry && entry.commentType !== currentCommentType && _covers(bounds, _globalCenterOf(entry))) {
                return entry;
            }
        }
        return null;
    }

    function test_timeEditorTakesTheClickOverTheSearchBox(): void {
        const searchBox = _globalBoundsOfSearchBox();
        const row = 5;

        _openEditor(_clickHelper.centerOfTimeLabel(control, row), "timePopup");

        const button = findChild(control, "incrementButton");
        verify(button);
        verify(_covers(searchBox, _globalCenterOf(button)), "the increment button has to sit over the search box, or the two never compete");

        const spinBox = _find.timeSpinBox(control);
        const before = spinBox.value;

        mouseClick(button, button.width / 2, button.height / 2);

        compare(spinBox.value, before + spinBox.stepSize, "the search box took the click meant for the time editor");
    }

    function test_commentTypeEditorTakesTheClickOverTheSearchBox(): void {
        const searchBox = _globalBoundsOfSearchBox();
        const row = 2;

        _openEditor(_clickHelper.centerOfCommentTypeLabel(control, row), "commentTypeMenu");

        const entry = _menuEntryOver(searchBox, row);
        verify(entry, "a menu entry has to sit over the search box, or the two never compete");

        const chosen = entry.commentType;

        mouseClick(entry, entry.width / 2, entry.height / 2);

        _expect.hasItemCommentType(control, row, chosen);
    }

    function test_searchBoxIgnoresPressesOnTheTimeEditor(): void {
        const searchBox = _globalBoundsOfSearchBox();
        const row = 5;

        _openEditor(_clickHelper.centerOfTimeLabel(control, row), "timePopup");

        const button = findChild(control, "incrementButton");
        verify(_covers(searchBox, _globalCenterOf(button)), "the increment button has to sit over the search box, or the two never compete");

        const popup = _find.searchBoxPopup(control);

        mousePress(button, button.width / 2, button.height / 2);
        const reacted = popup._shouldScaleUp;
        mouseRelease(button, button.width / 2, button.height / 2);

        verify(!reacted, "the search box reacted to a press that landed on the time editor above it");
    }

    function test_searchBoxStillReactsToItsOwnPresses(): void {
        const popup = _find.searchBoxPopup(control);
        const dragArea = _find.searchDragArea(control);

        // The search icon, not the middle: the middle is the text field, which takes the press itself
        const icon = _find.searchIconLabel(control);
        const grip = icon.mapToItem(dragArea, icon.width / 2, icon.height / 2);

        mouseMove(dragArea, grip.x, grip.y);
        mousePress(dragArea, grip.x, grip.y);
        const reacted = popup._shouldScaleUp;
        mouseRelease(dragArea, grip.x, grip.y);

        verify(reacted, "pressing the search box itself still has to pick it up");
    }

    // The claim check tells a deliberate arrow apart from the handler's resting default
    function _overrideCursorAt(item: Item): int {
        const dragArea = _find.searchDragArea(control);
        const point = item.mapToItem(dragArea, item.width / 2, item.height / 2);
        mouseMove(dragArea, point.x, point.y);

        const popup = _find.searchBoxPopup(control);
        const handler = findChild(popup, "cursorOverrideHandler");
        verify(handler, "cursorOverrideHandler");
        verify(handler.hovered, "the override handler should be hovered at that point");
        verify(popup._overrideCursor !== undefined, "the override should be claiming the cursor");
        compare(handler.cursorShape, popup._overrideCursor, "the handler should carry the claimed cursor");

        return handler.cursorShape;
    }

    function _cursorOverGrip(): int {
        return _overrideCursorAt(_find.searchIconLabel(control));
    }

    function _cursorOverTextField(): int {
        return _overrideCursorAt(_find.searchTextField(control));
    }

    // Row 0, so the editor opens at the top and leaves the whole search box uncovered
    function test_searchBoxShowsAPlainCursorUnderAModalPopup_data(): list<var> {
        return [
            {
                tag: "time-popup-grip",
                clickPoint: c => _clickHelper.centerOfTimeLabel(c, 0),
                editor: "timePopup",
                cursor: () => _cursorOverGrip()
            },
            {
                tag: "time-popup-text-field",
                clickPoint: c => _clickHelper.centerOfTimeLabel(c, 0),
                editor: "timePopup",
                cursor: () => _cursorOverTextField()
            },
            {
                tag: "comment-type-menu-grip",
                clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 0),
                editor: "commentTypeMenu",
                cursor: () => _cursorOverGrip()
            },
            {
                tag: "comment-type-menu-text-field",
                clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 0),
                editor: "commentTypeMenu",
                cursor: () => _cursorOverTextField()
            },
        ];
    }

    function test_searchBoxShowsAPlainCursorUnderAModalPopup(data): void {
        _openEditor(data.clickPoint(control), data.editor);

        compare(data.cursor(), Qt.ArrowCursor, "the search box offered a cursor it cannot honour while a modal popup is open");
    }

    // The inline editor is not modal and sits below, so the search box keeps its cursors
    function test_searchBoxKeepsItsCursorsUnderTheInlineEditor(): void {
        _openEditor(_clickHelper.centerOfCommentLabel(control, 2), "commentPopup");

        const popup = _find.searchBoxPopup(control);
        verify(popup._overrideCursor === undefined, "the inline editor must not trigger the override");

        const dragArea = _find.searchDragArea(control);
        const icon = _find.searchIconLabel(control);
        const grip = icon.mapToItem(dragArea, icon.width / 2, icon.height / 2);
        mouseMove(dragArea, grip.x, grip.y);

        const backgroundHandler = findChild(popup, "popupBackgroundCursorHandler");
        verify(backgroundHandler.hovered, "the grip should be hovered");
        compare(backgroundHandler.cursorShape, Qt.OpenHandCursor, "the inline editor must not take the grab away");
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
