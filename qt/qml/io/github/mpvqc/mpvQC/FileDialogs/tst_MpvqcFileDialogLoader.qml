// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcFileDialogLoader"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    function makeControl(): MpvqcFileDialogLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        tryVerify(() => control.item.visible);
    }

    function test_openFileDialog_data(): var {
        return [
            {
                tag: "export-classic-document",
                open: control => control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.EXPORT_CLASSIC_DOCUMENT),
                objectName: "exportClassicDocumentFileDialog"
            },
            {
                tag: "export-custom-document",
                open: control => control.openCustomExportFileDialog(Qt.resolvedUrl("template.jinja")),
                objectName: "exportCustomDocumentFileDialog"
            },
            {
                tag: "import-documents",
                open: control => control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.IMPORT_DOCUMENTS),
                objectName: "importDocumentsFileDialog"
            },
            {
                tag: "import-subtitles",
                open: control => control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.IMPORT_SUBTITLES),
                objectName: "importSubtitlesFileDialog"
            },
            {
                tag: "import-video",
                open: control => control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.IMPORT_VIDEO),
                objectName: "importVideoFileDialog"
            },
            {
                tag: "save-document",
                open: control => control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.SAVE_DOCUMENT),
                objectName: "saveDocumentFileDialog"
            }
        ];
    }

    function test_openFileDialog(data): void {
        const control = makeControl();

        data.open(control);

        waitUntilOpened(control);
        compare(control.item.objectName, data.objectName);
        testCase.bridge.waitForBackgroundJobs();
    }

    function test_teardownIsDeferred_data(): var {
        return [
            {
                tag: "accepted",
                dismiss: dialog => dialog.accepted()
            },
            {
                tag: "rejected",
                dismiss: dialog => dialog.rejected()
            }
        ];
    }

    function test_teardownIsDeferred(data): void {
        const control = makeControl();

        control.openFileDialog(MpvqcFileDialogKind.FileDialogKind.IMPORT_SUBTITLES);
        waitUntilOpened(control);

        const dialog = control.item;
        data.dismiss(dialog);
        verify(control.item, "file dialog must outlive the signal that triggered its teardown");
        dialog.close();

        tryVerify(() => !control.item);
        verify(!control.active);
        testCase.bridge.waitForBackgroundJobs();
    }

    Component {
        id: objectUnderTest

        MpvqcFileDialogLoader {}
    }
}
