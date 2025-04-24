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
import QtQuick.Controls.Material
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcMenuOptions"

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

        MpvqcMenuOptions {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property bool backupEnabled: false
                    property int backupInterval: 90
                    property int theme: Material.Dark
                    property int primary: Material.Teal
                    property string nickname: "nickname"
                    property bool writeHeaderDate: false
                    property bool writeHeaderGenerator: false
                    property bool writeHeaderNickname: false
                    property bool writeHeaderVideoPath: false
                }
                property var contentItem: Item {}
                property var mpvqcApplicationPathsPyObject: QtObject {
                    property url dir_backup: "file:///hello.txt"
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function urlToAbsolutePath(url) {
                        return `${url}-as-abs-path`;
                    }
                }
            }
        }
    }

    function test_openAppearanceSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogAppearance: factory
        });
        verify(control);

        control.appearanceAction.trigger();
        factory.verify();
    }

    function test_openCommentTypeSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogCommentTypes: factory
        });
        verify(control);

        control.commentTypesAction.trigger();
        factory.verify();
    }

    function test_openBackupSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogBackupSettings: factory
        });
        verify(control);

        control.backupAction.trigger();
        factory.verify();
    }

    function test_openExportSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogExportSettings: factory
        });
        verify(control);

        control.exportAction.trigger();
        factory.verify();
    }

    function test_openImportSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogImportSettings: factory
        });

        control.importAction.trigger();
        factory.verify();
    }

    function test_editMpvSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogEditMpvSettings: factory
        });

        control.editMpvAction.trigger();
        factory.verify();
    }

    function test_editInputSettings(): void {
        const factory = createTemporaryObject(factoryMock, testCase);
        verify(factory);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            factoryDialogEditInputSettings: factory
        });

        control.editInputAction.trigger();
        factory.verify();
    }
}
