// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtTest

TestCase {
    id: testCase

    width: 500
    height: 120
    visible: true
    when: windowShown
    name: "MpvqcWizardVideoStepDelegate"

    Component {
        id: objectUnderTest

        MpvqcWizardVideoStepDelegate {
            anchors.fill: parent

            index: 0
            filename: "foobar.mp4"
            fullPath: "/movies/foobar.mp4"
            foundInDocument: false
            foundInSubtitle: false
            isNoVideo: false
            selected: false
        }
    }

    Component {
        id: spyComponent

        SignalSpy {}
    }

    function makeControl(properties = {}): Item {
        const delegate = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(delegate);
        return delegate;
    }

    function makeSpy(target, signalName): SignalSpy {
        const spy = createTemporaryObject(spyComponent, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function test_labelTextReflectsRowKind_data(): var {
        return [
            {
                tag: "candidate-shows-filename",
                isNoVideo: false,
                expectedText: "foobar.mp4"
            },
            {
                tag: "sentinel-shows-skip-label",
                isNoVideo: true,
                expectedText: qsTranslate("ImportWizardDialog", "Skip video")
            },
        ];
    }

    function test_labelTextReflectsRowKind(data): void {
        const delegate = makeControl({
            isNoVideo: data.isNoVideo
        });
        const label = findChild(delegate, "label");
        verify(label);
        compare(label.text, data.expectedText);
    }

    function test_provenanceIconsReflectFlags_data(): var {
        return [
            {
                tag: "neither",
                foundInDocument: false,
                foundInSubtitle: false,
                expectDoc: false,
                expectSub: false
            },
            {
                tag: "from-document-only",
                foundInDocument: true,
                foundInSubtitle: false,
                expectDoc: true,
                expectSub: false
            },
            {
                tag: "from-subtitle-only",
                foundInDocument: false,
                foundInSubtitle: true,
                expectDoc: false,
                expectSub: true
            },
            {
                tag: "both",
                foundInDocument: true,
                foundInSubtitle: true,
                expectDoc: true,
                expectSub: true
            },
        ];
    }

    function test_provenanceIconsReflectFlags(data): void {
        const delegate = makeControl({
            foundInDocument: data.foundInDocument,
            foundInSubtitle: data.foundInSubtitle
        });
        const docIcon = findChild(delegate, "fromDocumentIcon");
        const subIcon = findChild(delegate, "fromSubtitleIcon");
        verify(docIcon);
        verify(subIcon);
        compare(docIcon.visible, data.expectDoc);
        compare(subIcon.visible, data.expectSub);
    }

    function test_radioReflectsSelected_data(): var {
        return [
            {
                tag: "selected",
                selected: true,
                expectActive: true
            },
            {
                tag: "unselected",
                selected: false,
                expectActive: false
            },
        ];
    }

    function test_radioReflectsSelected(data): void {
        const delegate = makeControl({
            selected: data.selected
        });
        const radio = findChild(delegate, "radioIcon");
        verify(radio);
        compare(radio.active, data.expectActive);
    }

    function test_clickEmitsClicked(): void {
        const delegate = makeControl();
        const spy = makeSpy(delegate, "clicked");
        mouseClick(delegate);
        compare(spy.count, 1);
    }

    function test_labelTooltipShowsFullPath(): void {
        const delegate = makeControl();
        const label = findChild(delegate, "label");
        verify(label);
        compare(label.ToolTip.text, "/movies/foobar.mp4");
    }
}
