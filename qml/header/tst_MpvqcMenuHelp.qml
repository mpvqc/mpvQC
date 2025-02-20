/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcMenuHelp"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: dialogMock

        QtObject {
            id: __dialogMock

            signal closed

            property bool openCalled: false

            function open(): void {
                __dialogMock.openCalled = true;
            }

            function deleteLater(): void {
            }
        }
    }

    Component {
        id: factoryMock

        QtObject {
            id: __factoryMock

            property bool createObjectCalled: false
            property var control: undefined

            function createObject(args) {
                __factoryMock.createObjectCalled = true;

                __factoryMock.control = testCase.createTemporaryObject(dialogMock, args);
                testCase.verify(__factoryMock.control);

                return __factoryMock.control;
            }

            function verify(): void {
                testCase.verify(__factoryMock.createObjectCalled);
                testCase.verify(__factoryMock.control.openCalled);
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcMenuHelp {
            id: objectUnderTest

            mpvqcApplication: QtObject {
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property string mpv_version: "any-version"
                    property string ffmpeg_version: "any-version"
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function getEnvironmentVariable(name: string): string { return "some-value" }
                }
            }
        }
    }

    function test_checkForUpdate(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryMessageBoxVersionCheck: factory
        });
        verify(control);

        control.updateAction.trigger();
        factory.verify();
    }

    function test_openShortcutDialog(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogShortcuts: factory
        });
        verify(control);

        control.shortcutAction.trigger();
        factory.verify();
    }

    function test_openExtendedExportMessageBox(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryMessageBoxExtendedExports: factory
        });
        verify(control);

        control.extendedExportsAction.trigger();
        factory.verify();
    }

    function test_openAboutDialog(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogAbout: factory
        });
        verify(control);

        control.aboutAction.trigger();
        factory.verify();
    }
}
