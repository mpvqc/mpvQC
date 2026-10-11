// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 900
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::ColumnLayout"

    readonly property Component objectUnderTest: Component {
        AppFontHost {}
    }

    readonly property Component mirroredObjectUnderTest: Component {
        AppFontHost {
            LayoutMirroring.enabled: true
            LayoutMirroring.childrenInherit: true
        }
    }

    readonly property Component timeFormatViewModel: Component {
        MpvqcCommentTableTimeFormatViewModel {}
    }

    readonly property int columnGap: 28

    // From play_arrow_rounded.svg: the tip is the quadratic from (16.362, 10.853) over (18, 12), furthest right at t = 0.5.
    readonly property real arrowPaintedLeft: 8
    readonly property real arrowPaintedRight: 17.181

    readonly property string shortType: "Spelling"
    readonly property string longType: "Considerably longer type"
    readonly property string pathologicalType: "A".repeat(400)

    property var _originalTimeFormatViewModel

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

    function initTestCase(): void {
        _originalTimeFormatViewModel = MpvqcTableUtility.viewModel;
    }

    function init(): void {
        _bridge.resetState();
        // resetState() rewires the bundle's MpvqcTableUtility; tests in this directory see their own copy.
        MpvqcTableUtility.viewModel = createTemporaryObject(timeFormatViewModel, testCase);
    }

    function cleanup(): void {
        MpvqcTableUtility.viewModel = _originalTimeFormatViewModel;
    }

    function makeControl(component: Component, longFormat: bool, widestType = longType): MpvqcTableView {
        const host = createTemporaryObject(component, testCase) as AppFontHost;
        verify(host);
        _bridge.loadVideo({
            duration: longFormat ? 2 * 60 * 60 : 60
        });
        _bridge.importComments([
            {
                "time": 1000,
                "commentType": widestType,
                "comment": "Comment 1"
            },
            {
                "time": 62000,
                "commentType": shortType,
                "comment": "Comment 2"
            }
        ]);
        waitForRendering(host);
        compare(_typeLabel(host.table, 0).text, widestType);
        tryCompare(MpvqcTableUtility, "useLongFormat", longFormat);
        return host.table;
    }

    function _delegate(control: MpvqcTableView, row: int): Item {
        return control.commentList.itemAtIndex(row);
    }

    function _playButton(control: MpvqcTableView, row: int): ToolButton {
        return findChild(_delegate(control, row), "playButton") as ToolButton;
    }

    function _timeLabel(control: MpvqcTableView, row: int): Label {
        return findChild(_delegate(control, row), "timeLabel") as Label;
    }

    function _typeLabel(control: MpvqcTableView, row: int): Label {
        return findChild(_delegate(control, row), "commentTypeLabel") as Label;
    }

    function _commentLabel(control: MpvqcTableView, row: int): Label {
        return findChild(_delegate(control, row), "commentLabel") as Label;
    }

    function _arrowPaintedSpan(control: MpvqcTableView, row: int): var {
        const button = _playButton(control, row);
        const contentItem = button.contentItem;
        const iconX = contentItem.x + (contentItem.width - button.icon.width) / 2;
        const x = button.mapToItem(control, iconX, 0).x;
        return {
            left: x + arrowPaintedLeft,
            right: x + arrowPaintedRight
        };
    }

    function _textLayoutSpan(control: MpvqcTableView, label: Label): var {
        const available = label.width - label.leftPadding - label.rightPadding;
        const textWidth = Math.min(label.contentWidth, available);
        let offset = label.leftPadding;
        if (label.effectiveHorizontalAlignment === Text.AlignHCenter) {
            offset += (available - textWidth) / 2;
        } else if (label.effectiveHorizontalAlignment === Text.AlignRight) {
            offset += available - textWidth;
        }
        const x = label.mapToItem(control, offset, 0).x;
        return {
            left: x,
            right: x + textWidth
        };
    }

    function _verifyFitsColumn(label: Label): void {
        const available = label.width - label.leftPadding - label.rightPadding;
        verify(label.contentWidth <= available, `'${label.text}' is ${label.contentWidth} wide in a ${available} column`);
    }

    function _gap(mirrored: bool, before: var, after: var): real {
        return mirrored ? before.left - after.right : after.left - before.right;
    }

    function _layouts(): list<var> {
        return [
            {
                tag: "ltr-short-time",
                component: objectUnderTest,
                mirrored: false,
                longFormat: false
            },
            {
                tag: "ltr-long-time",
                component: objectUnderTest,
                mirrored: false,
                longFormat: true
            },
            {
                tag: "rtl-short-time",
                component: mirroredObjectUnderTest,
                mirrored: true,
                longFormat: false
            },
            {
                tag: "rtl-long-time",
                component: mirroredObjectUnderTest,
                mirrored: true,
                longFormat: true
            },
        ];
    }

    function test_visibleContentIsEvenlySpaced_data(): list<var> {
        return _layouts();
    }

    function test_visibleContentIsEvenlySpaced(data: var): void {
        const control = makeControl(data.component, data.longFormat);
        const row = 0;
        _verifyFitsColumn(_timeLabel(control, row));
        _verifyFitsColumn(_typeLabel(control, row));

        const arrow = _arrowPaintedSpan(control, row);
        const time = _textLayoutSpan(control, _timeLabel(control, row));
        const type = _textLayoutSpan(control, _typeLabel(control, row));
        const comment = _textLayoutSpan(control, _commentLabel(control, row));

        const arrowToTime = _gap(data.mirrored, arrow, time);
        const timeToType = _gap(data.mirrored, time, type);
        const typeToComment = _gap(data.mirrored, type, comment);
        verify(_bridge.nearlyEqual(arrowToTime, columnGap), `arrow → time should be ${columnGap}, not ${arrowToTime}`);
        verify(_bridge.nearlyEqual(timeToType, columnGap), `time → type should be ${columnGap}, not ${timeToType}`);
        verify(_bridge.nearlyEqual(typeToComment, columnGap), `type → comment should be ${columnGap}, not ${typeToComment}`);
    }

    function test_shorterTypeLeavesExtraSpace_data(): list<var> {
        return _layouts();
    }

    function test_shorterTypeLeavesExtraSpace(data: var): void {
        const control = makeControl(data.component, data.longFormat);
        const longRow = 0;
        const shortRow = 1;

        const shortType = _typeLabel(control, shortRow);
        const longType = _typeLabel(control, longRow);
        _verifyFitsColumn(longType);
        verify(shortType.contentWidth < longType.contentWidth);

        const type = _textLayoutSpan(control, shortType);
        const comment = _textLayoutSpan(control, _commentLabel(control, shortRow));
        const extra = longType.contentWidth - shortType.contentWidth;

        const typeToComment = _gap(data.mirrored, type, comment);
        verify(_bridge.nearlyEqual(typeToComment, columnGap + extra), `short type → comment should be ${columnGap + extra}, not ${typeToComment}`);
    }

    function test_cappedTypeColumnKeepsLeadingGaps_data(): list<var> {
        return _layouts();
    }

    function test_cappedTypeColumnKeepsLeadingGaps(data: var): void {
        const control = makeControl(data.component, data.longFormat, pathologicalType);
        const row = 0;

        const typeLabel = _typeLabel(control, row);
        tryCompare(typeLabel, "width", control.width / 3);
        tryVerify(() => typeLabel.truncated);

        const arrow = _arrowPaintedSpan(control, row);
        const time = _textLayoutSpan(control, _timeLabel(control, row));
        const type = _textLayoutSpan(control, typeLabel);

        const arrowToTime = _gap(data.mirrored, arrow, time);
        const timeToType = _gap(data.mirrored, time, type);
        verify(_bridge.nearlyEqual(arrowToTime, columnGap), `arrow → time should be ${columnGap}, not ${arrowToTime}`);
        verify(_bridge.nearlyEqual(timeToType, columnGap), `time → capped type should be ${columnGap}, not ${timeToType}`);
        verify(_commentLabel(control, row).width > 100);
    }

    function test_playButtonKeepsTouchTarget(): void {
        const control = makeControl(objectUnderTest, false);
        const button = _playButton(control, 0);

        compare(button.width, 44);
        compare(button.height, 44);
        compare(button.icon.width, 24);
        compare(button.icon.height, 24);
    }

    function test_playArrowFollowsRowForeground_data(): list<var> {
        return [
            {
                tag: "selected",
                row: 0
            },
            {
                tag: "unselected",
                row: 1
            },
        ];
    }

    function test_playArrowFollowsRowForeground(data: var): void {
        const control = makeControl(objectUnderTest, false);
        control.commentList.currentIndex = 0;
        const delegate = _delegate(control, data.row);
        const button = _playButton(control, data.row);

        tryVerify(() => Qt.colorEqual(button.contentItem.color, delegate.foregroundColor));
    }

    MpvqcTestBridge {
        id: _bridge
    }
}
