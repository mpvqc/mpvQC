// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcModalOverlayRegistration"

    function makePopup(factory): var {
        const popup = createTemporaryObject(factory, testCase);
        verify(popup);
        return popup;
    }

    function cleanup(): void {
        tryVerify(() => !MpvqcModalState.anyModalOverlayOpen);
    }

    function test_modalPopupRegisters_data(): var {
        return [
            {
                tag: "dialog",
                factory: dialogFactory
            },
            {
                tag: "message-box",
                factory: messageBoxFactory
            },
            {
                tag: "positioned-menu",
                factory: positionedMenuFactory
            }
        ];
    }

    function test_modalPopupRegisters(data): void {
        const popup = makePopup(data.factory);
        verify(popup.modal);
        verify(!MpvqcModalState.anyModalOverlayOpen);

        popup.open();
        tryVerify(() => MpvqcModalState.anyModalOverlayOpen);

        popup.close();
        tryVerify(() => !MpvqcModalState.anyModalOverlayOpen);
    }

    function test_nonModalMenuDoesNotRegister(): void {
        const menu = makePopup(menuFactory);
        verify(!menu.modal);

        menu.open();
        tryVerify(() => menu.visible);
        verify(!MpvqcModalState.anyModalOverlayOpen);

        menu.close();
    }

    function test_destructionWhileOpenReleases(): void {
        const popup = makePopup(dialogFactory);
        popup.open();
        tryVerify(() => MpvqcModalState.anyModalOverlayOpen);

        popup.destroy();
        tryVerify(() => !MpvqcModalState.anyModalOverlayOpen);
    }

    Component {
        id: dialogFactory

        MpvqcDialog {}
    }

    Component {
        id: messageBoxFactory

        MpvqcMessageBox {}
    }

    Component {
        id: positionedMenuFactory

        MpvqcPositionedMenu {}
    }

    Component {
        id: menuFactory

        MpvqcMenu {}
    }
}
