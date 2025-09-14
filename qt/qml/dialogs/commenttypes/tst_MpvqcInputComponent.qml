// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

MpvqcInputComponent {
    id: objectUnderTest

    width: 400
    height: 400

    validateNewCommentType: input => null
    validateEditingOfCommentType: (input, inputBeingEdited) => null
    mpvqcApplication: QtObject {
        property var mpvqcTheme: QtObject {
            property color control: "purple"
        }
    }

    TestCase {
        name: "MpvqcInputComponent"
        when: windowShown

        SignalSpy {
            id: addedSpy
            target: objectUnderTest
            signalName: "added"
        }
        SignalSpy {
            id: editedSpy
            target: objectUnderTest
            signalName: "edited"
        }

        function test_mode_data() {
            return [
                {
                    tag: "add",
                    editing: false,
                    objectName: "MpvqcInputControls::add"
                },
                {
                    tag: "edit",
                    editing: true,
                    objectName: "MpvqcInputControls::edit"
                },
            ];
        }

        function test_mode(data) {
            objectUnderTest.loader.editing = data.editing;
            compare(objectUnderTest.loader.item.objectName, data.objectName);
        }

        function test_signal_data() {
            return [
                {
                    tag: "added",
                    editing: false,
                    spy: addedSpy
                },
                {
                    tag: "edited",
                    editing: true,
                    spy: editedSpy
                },
            ];
        }

        function test_signal(data) {
            objectUnderTest.loader.editing = data.editing;
            (objectUnderTest.loader.item as MpvqcInputControls).accepted(data.tag);
            compare(data.spy.count, 1);
        }

        function test_editing_started() {
            const textToEdit = "edit me";

            objectUnderTest.loader.editing = false;
            objectUnderTest.startEditing(textToEdit);

            verify(objectUnderTest.loader.editing);
            compare((objectUnderTest.loader.item as MpvqcInputControls).text, textToEdit);
        }

        function test_editing_stopped_data() {
            return [
                {
                    tag: "done",
                    exec: () => (objectUnderTest.loader.item as MpvqcInputControls).done()
                },
                {
                    tag: "reset",
                    exec: () => objectUnderTest.stopEditing()
                },
            ];
        }

        function test_editing_stopped(data) {
            objectUnderTest.loader.editing = true;
            data.exec();
            verify(!objectUnderTest.loader.editing);
        }
    }
}
