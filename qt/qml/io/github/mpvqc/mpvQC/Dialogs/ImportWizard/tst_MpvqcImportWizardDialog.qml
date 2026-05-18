// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 700
    height: 500
    visible: true
    when: windowShown
    name: "MpvqcImportWizardDialog"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    readonly property Component _dialogComponent: Component {
        MpvqcImportWizardDialog {}
    }

    readonly property var open: QtObject {
        function scenario(name: string): QtObject {
            const viewModel = testCase.bridge.buildWizardViewModel(name);
            testCase.verify(viewModel, `viewModel for '${name}' not built`);
            const dlg = testCase.createTemporaryObject(testCase._dialogComponent, testCase, {
                viewModel: viewModel
            });
            testCase.verify(dlg, `dialog for '${name}' not created`);
            dlg.open();
            testCase.tryCompare(dlg, "opened", true);
            const stepView = testCase.findChild(dlg.contentItem, "stepView");
            if (stepView) {
                stepView.animationDuration = 0;
            }
            return dlg;
        }
    }

    readonly property var find: QtObject {
        function videoList(dlg: QtObject): ListView {
            const list = testCase.findChild(dlg.contentItem, "videoList");
            testCase.verify(list, "videoList not found");
            return list;
        }

        function subtitleList(dlg: QtObject): ListView {
            const list = testCase.findChild(dlg.contentItem, "subtitleList");
            testCase.verify(list, "subtitleList not found");
            return list;
        }

        function sessionRadio(dlg: QtObject, mode: string): Item {
            const radio = testCase.findChild(dlg.contentItem, mode + "Radio");
            testCase.verify(radio, `${mode}Radio not found`);
            return radio;
        }

        function selectAll(dlg: QtObject): Item {
            const checkbox = testCase.findChild(dlg.contentItem, "selectAll");
            testCase.verify(checkbox, "selectAll checkbox not found");
            return checkbox;
        }

        function primaryButton(dlg: QtObject): Item {
            const btn = testCase.findChild(dlg.footer, "primaryButton");
            testCase.verify(btn, "primaryButton not found");
            return btn;
        }

        function cancelButton(dlg: QtObject): Item {
            const btn = testCase.findChild(dlg.footer, "cancelButton");
            testCase.verify(btn, "cancelButton not found");
            return btn;
        }

        function backButton(dlg: QtObject): Item {
            const btn = testCase.findChild(dlg.footer, "backButton");
            testCase.verify(btn, "backButton not found");
            return btn;
        }

        function stepEntryAt(dlg: QtObject, index: int): Item {
            const indicator = testCase.findChild(dlg.contentItem, "stepIndicator");
            testCase.verify(indicator, "stepIndicator not found");
            const entries = testCase._collectAll(indicator, "stepEntry");
            testCase.verify(entries.length > index, `stepEntry ${index} not found (have ${entries.length})`);
            return entries[index];
        }
    }

    function _collectAll(root: Item, objectName: string): list<Item> {
        const found = [];
        function visit(item: Item): void {
            if (!item) {
                return;
            }
            if (item.objectName === objectName) {
                found.push(item);
            }
            const kids = item.children;
            if (kids) {
                for (let i = 0; i < kids.length; i++) {
                    visit(kids[i]);
                }
            }
        }
        visit(root);
        return found;
    }

    readonly property var pick: QtObject {
        function video(dlg: QtObject, index: int): void {
            const list = testCase.find.videoList(dlg);
            testCase.tryVerify(() => list.itemAtIndex(index) !== null);
            testCase.mouseClick(list.itemAtIndex(index));
        }

        function subtitle(dlg: QtObject, index: int): void {
            const list = testCase.find.subtitleList(dlg);
            testCase.tryVerify(() => list.itemAtIndex(index) !== null);
            testCase.mouseClick(list.itemAtIndex(index));
        }

        function session(dlg: QtObject, mode: string): void {
            testCase.mouseClick(testCase.find.sessionRadio(dlg, mode));
        }

        function selectAll(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.selectAll(dlg));
        }

        function step(dlg: QtObject, index: int): void {
            testCase.mouseClick(testCase.find.stepEntryAt(dlg, index));
            testCase._waitForStepSettled(dlg);
        }
    }

    readonly property var click: QtObject {
        function primary(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.primaryButton(dlg));
        }

        function next(dlg: QtObject): void {
            testCase.click.primary(dlg);
            testCase._waitForStepSettled(dlg);
        }

        function cancel(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.cancelButton(dlg));
        }

        function back(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.backButton(dlg));
            testCase._waitForStepSettled(dlg);
        }
    }

    function _waitForStepSettled(dlg: QtObject): void {
        const stepView = findChild(dlg.contentItem, "stepView");
        verify(stepView, "stepView not found");
        tryVerify(() => !stepView.busy);
        waitForRendering(dlg.contentItem);
    }

    readonly property var expect: QtObject {
        function currentStep(dlg: QtObject, index: int): void {
            testCase.tryCompare(dlg.viewModel, "currentStepIndex", index);
            testCase.waitForRendering(dlg.contentItem);
        }

        function selectedVideo(dlg: QtObject, index: int): void {
            const list = testCase.find.videoList(dlg);
            testCase.tryVerify(() => list.itemAtIndex(index) !== null);
            testCase.tryVerify(() => list.itemAtIndex(index).selected === true);
        }

        function sessionMode(dlg: QtObject, mode: string): void {
            const expected = mode === "replace" ? MpvqcImportWizardSessionMode.REPLACE : MpvqcImportWizardSessionMode.MERGE;
            testCase.tryCompare(dlg.viewModel.sessionStepViewModel, "mode", expected);
            const radio = testCase.find.sessionRadio(dlg, mode);
            testCase.tryVerify(() => radio.selected === true);
        }

        function subtitleChecked(dlg: QtObject, index: int, checked: bool): void {
            const list = testCase.find.subtitleList(dlg);
            testCase.tryVerify(() => list.itemAtIndex(index) !== null);
            const checkbox = testCase.findChild(list.itemAtIndex(index), "checkbox");
            testCase.verify(checkbox, "checkbox not found");
            testCase.tryCompare(checkbox, "checked", checked);
        }

        function openedVideo(name: string): void {
            testCase.tryVerify(() => testCase.bridge.openedVideoName() === name);
        }

        function noOpenedVideo(): void {
            testCase.compare(testCase.bridge.openedVideoName(), "");
        }

        function openedSubtitleCount(count: int): void {
            testCase.tryVerify(() => testCase.bridge.openedSubtitleCount() === count);
        }

        function openedSubtitles(names: list<string>): void {
            testCase.tryVerify(() => {
                const opened = testCase.bridge.openedSubtitleNames();
                return opened.length === names.length && names.every(n => opened.indexOf(n) >= 0);
            });
        }
    }

    function init(): void {
        bridge.resetState();
    }

    function test_pickingVideoAndImportingOpensThatVideo(): void {
        const dlg = open.scenario("video-choice");
        pick.video(dlg, 1);
        click.primary(dlg);
        expect.openedVideo("b.mp4");
    }

    function test_navigationViaAllMechanismsKeepsPerStepSelections(): void {
        const dlg = open.scenario("all-steps");
        expect.currentStep(dlg, 0);

        click.next(dlg);
        expect.currentStep(dlg, 1);
        pick.session(dlg, "replace");

        click.next(dlg);
        expect.currentStep(dlg, 2);
        pick.video(dlg, 1);

        pick.step(dlg, 3);
        expect.currentStep(dlg, 3);
        pick.subtitle(dlg, 0);

        click.back(dlg);
        expect.currentStep(dlg, 2);
        expect.selectedVideo(dlg, 1);

        pick.step(dlg, 1);
        expect.currentStep(dlg, 1);
        expect.sessionMode(dlg, "replace");

        pick.step(dlg, 3);
        expect.currentStep(dlg, 3);
        expect.subtitleChecked(dlg, 0, false);
    }

    function test_pickingSkipVideoEntryOpensNoVideo(): void {
        const dlg = open.scenario("video-choice");
        // index 0 = a.mp4, 1 = b.mp4, 2 = implicit "Don't load a video"
        pick.video(dlg, 2);
        click.primary(dlg);
        expect.noOpenedVideo();
    }

    function test_deselectingSubtitlesExcludesThemFromImport(): void {
        const dlg = open.scenario("subtitles-only");
        // 3 subtitles default-checked; deselect b.srt (index 1)
        pick.subtitle(dlg, 1);
        click.primary(dlg);
        expect.openedSubtitles(["a.srt", "c.srt"]);
    }

    function test_subtitlesSelectAllTriStateReflectsRowChecks(): void {
        const dlg = open.scenario("subtitles-only");
        const selectAll = find.selectAll(dlg);

        tryCompare(selectAll, "checkState", Qt.Checked);

        pick.subtitle(dlg, 1);
        tryCompare(selectAll, "checkState", Qt.PartiallyChecked);

        pick.selectAll(dlg);
        tryCompare(selectAll, "checkState", Qt.Checked);

        pick.selectAll(dlg);
        tryCompare(selectAll, "checkState", Qt.Unchecked);

        pick.selectAll(dlg);
        tryCompare(selectAll, "checkState", Qt.Checked);
    }

    function test_closeOnlyModeShowsOnlyCloseAndClosesWithoutImport(): void {
        const dlg = open.scenario("errors-only");

        verify(!find.cancelButton(dlg).visible, "cancel should be hidden in close-only mode");
        verify(!find.backButton(dlg).visible, "back should be hidden on first step");
        verify(find.primaryButton(dlg).visible, "primary should be visible");

        click.primary(dlg);

        tryCompare(dlg, "opened", false);
        expect.noOpenedVideo();
        expect.openedSubtitleCount(0);
    }

    function test_confirmOnlyModeHidesCancelWhenVideoIsTheOnlyDecision(): void {
        const dlg = open.scenario("video-choice");

        verify(!find.cancelButton(dlg).visible, "cancel should be hidden in confirm-only mode");
        verify(!find.backButton(dlg).visible, "back should be hidden on first step");
        verify(find.primaryButton(dlg).visible, "primary should be visible");
    }

    function test_cancelDiscardsSelectionsAndImportsNothing(): void {
        const dlg = open.scenario("all-steps");

        pick.step(dlg, 1);
        pick.session(dlg, "replace");
        pick.step(dlg, 2);
        pick.video(dlg, 1);

        click.cancel(dlg);

        tryCompare(dlg, "opened", false);
        expect.noOpenedVideo();
        expect.openedSubtitleCount(0);
    }
}
