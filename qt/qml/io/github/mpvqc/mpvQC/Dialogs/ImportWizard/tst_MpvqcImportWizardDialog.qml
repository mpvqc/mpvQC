// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls // qmllint disable unused-imports
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
            testCase.verify(stepView, "stepView not found");
            stepView.sweepDuration = 0;
            waitForRendering(dlg.contentItem);
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

        function sessionRow(dlg: QtObject, mode: string): Item {
            const row = testCase.findChild(dlg.contentItem, mode + "Row");
            testCase.verify(row, `${mode}Row not found`);
            return row;
        }

        function selectAll(dlg: QtObject): Item {
            const button = testCase.findChild(dlg.contentItem, "selectAll");
            testCase.verify(button, "selectAll button not found");
            return button;
        }

        function selectAllIndicator(dlg: QtObject): Item {
            const indicator = testCase.findChild(dlg.contentItem, "selectAllIndicator");
            testCase.verify(indicator, "selectAllIndicator not found");
            return indicator;
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

        function stepPager(dlg: QtObject): Item {
            const pager = testCase.findChild(dlg.contentItem, "stepPager");
            testCase.verify(pager, "stepPager not found");
            return pager;
        }

        function stepName(dlg: QtObject): Item {
            const label = testCase.findChild(dlg.contentItem, "stepName");
            testCase.verify(label, "stepName not found");
            return label;
        }

        function stepScroll(dlg: QtObject): Item {
            const scroll = testCase.findChild(dlg.contentItem, "stepScroll");
            testCase.verify(scroll, "stepScroll not found");
            return scroll;
        }

        function pagerDotAt(dlg: QtObject, index: int): Item {
            const dots = testCase._collectAll(testCase.find.stepPager(dlg), "pagerDot");
            testCase.verify(dots.length > index, `pagerDot ${index} not found (have ${dots.length})`);
            return dots[index];
        }
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
            testCase.mouseClick(testCase.find.sessionRow(dlg, mode));
        }

        function selectAll(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.selectAll(dlg));
        }

        function step(dlg: QtObject, index: int): void {
            testCase.mouseClick(testCase.find.pagerDotAt(dlg, index));
            testCase.waitForRendering(dlg.contentItem);
        }
    }

    readonly property var click: QtObject {
        function primary(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.primaryButton(dlg));
        }

        function next(dlg: QtObject): void {
            testCase.click.primary(dlg);
            testCase.waitForRendering(dlg.contentItem);
        }

        function cancel(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.cancelButton(dlg));
        }

        function back(dlg: QtObject): void {
            testCase.mouseClick(testCase.find.backButton(dlg));
            testCase.waitForRendering(dlg.contentItem);
        }
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
            const expected = mode === "replace" ? MpvqcImportWizardSessionMode.SessionMode.REPLACE : MpvqcImportWizardSessionMode.SessionMode.MERGE;
            const sessionStep = dlg.viewModel.steps.find(step => step.kind === MpvqcImportWizardStepKind.StepKind.SESSION);
            testCase.verify(sessionStep, "session step not found");
            testCase.tryCompare(sessionStep, "mode", expected);
            const row = testCase.find.sessionRow(dlg, mode);
            testCase.tryVerify(() => row.selected === true);
        }

        function subtitleChecked(dlg: QtObject, index: int, checked: bool): void {
            const list = testCase.find.subtitleList(dlg);
            testCase.tryVerify(() => list.itemAtIndex(index) !== null);
            const indicator = testCase.findChild(list.itemAtIndex(index), "checkIndicator");
            testCase.verify(indicator, "checkIndicator not found");
            testCase.tryCompare(indicator, "checked", checked);
        }

        function selectAllTriState(dlg: QtObject, checked: bool, partial: bool): void {
            const indicator = testCase.find.selectAllIndicator(dlg);
            testCase.tryCompare(indicator, "checked", checked);
            testCase.tryCompare(indicator, "partial", partial);
        }
    }

    readonly property Component _dialogComponent: Component {
        MpvqcImportWizardDialog {
            // Opening and closing animate, and no test here is about that motion
            enter: null
            exit: null
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

    function init(): void {
        bridge.resetState();
    }

    function test_navigationViaAllMechanismsKeepsPerStepSelections(): void {
        const dlg = open.scenario("all-steps");
        verify(find.stepPager(dlg).visible, "pager should show with more than one step");
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

    function test_theStepNavigationNamesEveryStepAndTracksTheCurrentOne(): void {
        const dlg = open.scenario("all-steps");
        const names = dlg.viewModel.stepNames;

        for (let index = 0; index < names.length; index++) {
            compare(find.pagerDotAt(dlg, index).ToolTip.text, names[index]);
        }
        compare(find.stepName(dlg).text, names[0]);

        click.next(dlg);
        expect.currentStep(dlg, 1);
        compare(find.stepName(dlg).text, names[1]);
    }

    function test_navigatingStartsTheNextStepAtTheTop(): void {
        const dlg = open.scenario("all-steps");
        const scroll = find.stepScroll(dlg);

        scroll.contentItem.contentY = 40;

        click.next(dlg);

        expect.currentStep(dlg, 1);
        tryCompare(scroll.contentItem, "contentY", 0);
    }

    function test_subtitlesSelectAllTriStateReflectsRowChecks(): void {
        const dlg = open.scenario("subtitles-only");

        expect.selectAllTriState(dlg, true, false);

        pick.subtitle(dlg, 1);
        expect.selectAllTriState(dlg, false, true);

        pick.selectAll(dlg);
        expect.selectAllTriState(dlg, true, false);

        pick.selectAll(dlg);
        expect.selectAllTriState(dlg, false, false);

        pick.selectAll(dlg);
        expect.selectAllTriState(dlg, true, false);
    }

    function test_errorsStepShowsRejectionReasonPerDocument(): void {
        const dlg = open.scenario("errors-only");

        const errorRows = findChild(dlg, "errorRows");
        verify(errorRows, "error rows not found");
        tryCompare(errorRows, "count", 2);

        tryVerify(() => errorRows.itemAt(0) !== null);
        tryVerify(() => errorRows.itemAt(1) !== null);

        const first = errorRows.itemAt(0);
        const second = errorRows.itemAt(1);

        compare(first.filename, "broken.qc");
        compare(second.filename, "future.json");
        verify(first.reason.length > 0, "invalid document should show a rejection reason");
        verify(second.reason.length > 0, "unsupported document should show a rejection reason");
        verify(first.reason !== second.reason, "different rejection reasons should render differently");
    }

    function test_closeOnlyModeShowsOnlyClose(): void {
        const dlg = open.scenario("errors-only");

        verify(!find.cancelButton(dlg).visible, "cancel should be hidden in close-only mode");
        verify(!find.backButton(dlg).visible, "back should be hidden on first step");
        verify(find.primaryButton(dlg).visible, "primary should be visible");
        verify(!find.stepPager(dlg).visible, "pager should be hidden with a single step");
        verify(!find.stepName(dlg).visible, "step name should be hidden with a single step");

        click.primary(dlg);

        tryCompare(dlg, "opened", false);
    }

    function test_cancelClosesTheDialogAndDismissesTheImport(): void {
        const dlg = open.scenario("all-steps");

        click.cancel(dlg);

        tryCompare(dlg, "opened", false);
        compare(bridge.wizardOutcome().outcome, "dismissed");
    }

    function test_confirmReportsThePickedVideo(): void {
        const dlg = open.scenario("video-choice");

        pick.video(dlg, 1);
        click.primary(dlg);

        tryCompare(dlg, "opened", false);
        compare(bridge.wizardOutcome().outcome, "finished");
        compare(bridge.wizardOutcome().video, "b.mp4");
    }
}
