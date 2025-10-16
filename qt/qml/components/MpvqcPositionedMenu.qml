// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../utility"

MpvqcMenu {
    id: root

    property point position: Qt.point(0, 0)

    property var deferToOnClose: () => {}

    /**
     * Override to provide custom position calculation logic.
     */
    function calculatePosition(): point {
        return position;
    }

    modal: true

    onAboutToShow: {
        const pos = calculatePosition();

        if (!parent) {
            return;
        }

        const margin = MpvqcConstants.popupWindowEdgeMargin;
        const checkX = isMirrored ? pos.x - width : pos.x;
        const violations = MpvqcWindowUtility.getEdgeViolations(parent, checkX, pos.y, width, implicitHeight, margin);

        if (isMirrored) {
            x = violations.left ? pos.x : pos.x - width;
        } else {
            x = violations.right ? pos.x - width : pos.x;
        }
        y = violations.bottom ? pos.y - implicitHeight : pos.y;

        const showToRight = isMirrored ? violations.left : !violations.right;
        if (violations.bottom) {
            transformOrigin = showToRight ? Popup.BottomLeft : Popup.BottomRight;
        } else {
            transformOrigin = showToRight ? Popup.TopLeft : Popup.TopRight;
        }
    }

    onClosed: {
        deferToOnClose();
        deferToOnClose = () => {};
    }
}
