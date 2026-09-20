// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::OptionsMenu"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    function init(): void {
        failOnWarning(/.*(TypeError|Unable to assign).*/);
        it.resetState();
    }

    function cleanup(): void {
        testCase.Window.window.height = 720;
    }

    function openNewCommentMenu(control: Item): QtObject {
        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");
        tableView.forceActiveFocus();
        keyClick(Qt.Key_E);
        const menu = findChild(control, "newCommentMenu");
        verify(menu, "newCommentMenu not found");
        tryVerify(() => menu.opened);
        return menu;
    }

    function openAppearanceDialog(control: Item): QtObject {
        it.menu.trigger(control, "optionsMenu", "openAppearanceDialogMenuItem");
        return it.find.openedDialog(control, "appearanceDialog");
    }

    function pickColorScheme(dialog: QtObject, preference: string): void {
        const swatch = it.find.visualChild(dialog, `colorSchemePreferenceSwatch_${preference}`);
        verify(swatch, `colorSchemePreferenceSwatch_${preference} not found`);
        mouseClick(swatch);
        tryVerify(() => it.settings.colorSchemePreference() === preference);
    }

    function pickOtherAccentColor(dialog: QtObject): string {
        const section = it.find.visualChild(dialog, "accentColorSection");
        verify(section, "accentColorSection not found");
        const flow = it.find.visualChild(dialog, "accentColorFlow");
        verify(flow, "accentColorFlow not found");
        tryVerify(() => flow.height > 0 && flow.mapToItem(section, 0, flow.height).y <= section.height, 5000, "the accent section should unfold fully");

        const index = dialog.viewModel.accentColorIndex === 0 ? 1 : 0;
        const swatch = it.find.visualChild(dialog, `accentColorSwatch_${index}`);
        verify(swatch, `accentColorSwatch_${index} not found`);
        mouseClick(swatch);
        return swatch.accentColor;
    }

    function test_settingsDialogsHaveOneTopInset_data(): var {
        return [
            {
                tag: "appearance",
                menuItem: "openAppearanceDialogMenuItem",
                dialog: "appearanceDialog"
            },
            {
                tag: "backup",
                menuItem: "openBackupSettingsDialogMenuItem",
                dialog: "backupDialog"
            },
            {
                tag: "export",
                menuItem: "openExportSettingsDialogMenuItem",
                dialog: "exportSettingsDialog"
            },
            {
                tag: "import",
                menuItem: "openImportSettingsDialogMenuItem",
                dialog: "importSettingsDialog"
            }
        ];
    }

    function test_settingsDialogsHaveOneTopInset(data): void {
        const control = it.makeControl();
        it.menu.trigger(control, "optionsMenu", data.menuItem);
        const dialog = it.find.openedDialog(control, data.dialog);
        verify(waitForPolish(dialog.contentItem.Window.window));
        const card = findChild(dialog.contentItem, "cardBackground");
        verify(card);
        compare(card.mapToItem(dialog.contentItem, 0, 0).y, MpvqcConstants.dialogContentTopMargin);
        it.dialog.reject(dialog);
    }

    function test_appearanceDialog_accept_persistsColorSchemeAndAccent(): void {
        const control = it.makeControl();
        const dialog = openAppearanceDialog(control);

        pickColorScheme(dialog, "light");

        const section = findChild(dialog, "accentColorSection");
        verify(section, "accentColorSection not found");
        tryVerify(() => section.expanded);

        const expectedAccent = pickOtherAccentColor(dialog);
        tryVerify(() => it.settings.accentColor("light") === expectedAccent);

        it.dialog.accept(dialog);

        tryVerify(() => it.settings.colorSchemePreference() === "light");
        tryVerify(() => it.settings.accentColor("light") === expectedAccent);
    }

    function test_appearanceDialog_systemHidesTheAccentSection(): void {
        const control = it.makeControl();
        const dialog = openAppearanceDialog(control);

        const section = findChild(dialog, "accentColorSection");
        verify(section, "accentColorSection not found");

        pickColorScheme(dialog, "dark");
        tryVerify(() => section.expanded);

        pickColorScheme(dialog, "system");

        tryVerify(() => !section.expanded);
        tryVerify(() => !section.visible);
    }

    function test_appearanceDialog_reject_revertsColorSchemeAndBothAccents(): void {
        const control = it.makeControl();
        const initialPreference = it.settings.colorSchemePreference();
        const initialLightAccent = it.settings.accentColor("light");
        const initialDarkAccent = it.settings.accentColor("dark");

        const dialog = openAppearanceDialog(control);

        pickColorScheme(dialog, "light");
        const lightAccent = pickOtherAccentColor(dialog);
        tryVerify(() => it.settings.accentColor("light") === lightAccent);

        pickColorScheme(dialog, "dark");
        const darkAccent = pickOtherAccentColor(dialog);
        tryVerify(() => it.settings.accentColor("dark") === darkAccent);

        it.dialog.reject(dialog);

        tryVerify(() => it.settings.colorSchemePreference() === initialPreference);
        tryVerify(() => it.settings.accentColor("light") === initialLightAccent);
        tryVerify(() => it.settings.accentColor("dark") === initialDarkAccent);
    }

    function test_commentTypesDialog_deleteAndAdd_persistsAndUpdatesNewCommentMenu(): void {
        const control = it.makeControl();
        const defaults = it.settings.commentTypes();
        verify(defaults.length > 1, "expected multiple default comment types");
        const newType = "IntegrationTestType";

        it.menu.trigger(control, "optionsMenu", "openCommentTypesDialogMenuItem");
        const dialog = it.find.openedDialog(control, "commentTypesDialog");

        const listView = findChild(dialog, "commentTypesListView");
        verify(listView, "commentTypesListView not found");
        const deleteButton = findChild(dialog, "commentTypeDeleteButton");
        verify(deleteButton, "commentTypeDeleteButton not found");

        while (listView.count > 1) {
            tryVerify(() => deleteButton.enabled);
            const before = listView.count;
            mouseClick(deleteButton);
            tryVerify(() => listView.count === before - 1);
        }
        tryVerify(() => !deleteButton.enabled);

        const textField = findChild(dialog, "commentTypeTextField");
        verify(textField, "commentTypeTextField not found");
        const addButton = findChild(dialog, "commentTypeAddButton");
        verify(addButton, "commentTypeAddButton not found");
        textField.forceActiveFocus();
        textField.text = newType;
        tryVerify(() => addButton.enabled);
        mouseClick(addButton);
        tryVerify(() => listView.count === 2);

        it.dialog.accept(dialog);
        tryVerify(() => it.settings.commentTypes().length === 2);
        tryVerify(() => it.settings.commentTypes()[1] === newType);

        const menu = it.menu.openNewCommentMenu(control);
        tryVerify(() => menu.count === 2);
        menu.close();
    }

    function test_commentTypesDialog_resetButton_restoresDefaultsAndUpdatesNewCommentMenu(): void {
        const control = it.makeControl();
        const defaults = it.settings.commentTypes();
        verify(defaults.length > 1, "expected multiple default comment types");

        it.menu.trigger(control, "optionsMenu", "openCommentTypesDialogMenuItem");
        let dialog = it.find.openedDialog(control, "commentTypesDialog");
        mouseClick(findChild(dialog, "commentTypeDeleteButton"));
        it.dialog.accept(dialog);
        verify(it.settings.commentTypes().length < defaults.length, "precondition: settings should differ from defaults");

        it.menu.trigger(control, "optionsMenu", "openCommentTypesDialogMenuItem");
        dialog = it.find.openedDialog(control, "commentTypesDialog");
        const resetButton = dialog.standardButton(Dialog.Reset);
        verify(resetButton, "Reset standard button not found");
        mouseClick(resetButton);
        it.dialog.accept(dialog);
        tryVerify(() => JSON.stringify(it.settings.commentTypes()) === JSON.stringify(defaults));

        const menu = it.menu.openNewCommentMenu(control);
        tryVerify(() => menu.count === defaults.length);
        menu.close();
    }

    function test_applicationTitleRadio_data() {
        return [
            {
                tag: "filename",
                identifier: "filename",
                expected: 1
            },
            {
                tag: "filepath",
                identifier: "filepath",
                expected: 2
            },
            {
                tag: "default",
                identifier: "default",
                expected: 0
            },
        ];
    }

    function test_applicationTitleRadio(data): void {
        const control = it.makeControl();
        it.menu.triggerSubItem(control, "optionsMenu", "applicationTitleMenu", `applicationTitleMenuRadioItem_${data.identifier}`);
        tryVerify(() => it.settings.windowTitleFormat() === data.expected);
    }

    function test_layoutOrientationRadio_data() {
        return [
            {
                tag: "horizontal",
                identifier: "horizontal",
                expected: Qt.Horizontal
            },
            {
                tag: "vertical",
                identifier: "vertical",
                expected: Qt.Vertical
            },
        ];
    }

    function test_layoutOrientationRadio(data): void {
        const control = it.makeControl();
        it.menu.triggerSubItem(control, "optionsMenu", "layoutOrientationMenu", `layoutOrientationMenuRadioItem_${data.identifier}`);
        tryVerify(() => it.settings.layoutOrientation() === data.expected);

        const splitView = findChild(control, "applicationSplitView");
        verify(splitView, "applicationSplitView not found");
        tryVerify(() => splitView.orientation === data.expected);
    }

    function openBackupSettings(control: Item): QtObject {
        it.menu.trigger(control, "optionsMenu", "openBackupSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "backupDialog");
        verify(waitForPolish(dialog.contentItem.Window.window));
        return dialog;
    }

    function backupControl(dialog: QtObject, name: string): Item {
        const item = it.find.visualChild(dialog, name);
        verify(item, `${name} not found`);
        return item;
    }

    function test_backupDialog_drivesAllSettingsAndOpensFolder(): void {
        const control = it.makeControl();
        const initialEnabled = it.settings.backupEnabled();
        const initialInterval = it.settings.backupInterval();
        let dialog = openBackupSettings(control);
        const toggle = backupControl(dialog, "backupEnabledSwitch");
        if (!toggle.checked) {
            mouseClick(toggle);
        }
        const preset = backupControl(dialog, "backupIntervalPreset_180");
        mouseClick(preset);
        tryCompare(preset, "checked", true);
        mouseClick(toggle);
        tryCompare(preset, "enabled", false);
        compare(it.settings.backupEnabled(), initialEnabled);
        compare(it.settings.backupInterval(), initialInterval);

        const locationButton = backupControl(dialog, "backupOpenLocationButton");
        locationButton.forceActiveFocus(Qt.TabFocusReason);
        keyClick(Qt.Key_Space);
        tryVerify(() => it.bridge.openedDesktopUrls().includes(it.bridge.backupFolderUrl().toString()));
        mouseClick(dialog.standardButton(Dialog.Ok));
        it.expect.dialogClosed(control, "backupDialog");
        compare(it.settings.backupEnabled(), false);
        compare(it.settings.backupInterval(), 180);

        dialog = openBackupSettings(control);
        const restored = backupControl(dialog, "backupIntervalPreset_180");
        compare(restored.checked, true);
        compare(restored.enabled, false);
        mouseClick(backupControl(dialog, "backupEnabledSwitch"));
        tryCompare(restored, "enabled", true);
        compare(restored.checked, true);
    }

    function test_backupDialog_reject_discardsSettings(): void {
        const control = it.makeControl();

        const initialEnabled = it.settings.backupEnabled();
        const initialInterval = it.settings.backupInterval();

        for (const action of [Dialog.Cancel, Dialog.NoButton]) {
            const dialog = openBackupSettings(control);
            const toggle = backupControl(dialog, "backupEnabledSwitch");
            compare(toggle.checked, initialEnabled);
            if (!toggle.checked) {
                mouseClick(toggle);
            }
            mouseClick(backupControl(dialog, "backupIntervalPreset_300"));
            mouseClick(toggle);
            if (action === Dialog.Cancel) {
                mouseClick(dialog.standardButton(Dialog.Cancel));
            } else {
                keyClick(Qt.Key_Escape);
            }
            it.expect.dialogClosed(control, "backupDialog");
            compare(it.settings.backupEnabled(), initialEnabled);
            compare(it.settings.backupInterval(), initialInterval);
        }
    }

    function test_backupDialog_unmatchedIntervalSurvivesUnrelatedChanges(): void {
        const control = it.makeControl();
        const initialInterval = it.settings.backupInterval();
        verify(![30, 60, 90, 120, 180, 300].includes(initialInterval));
        const dialog = openBackupSettings(control);
        mouseClick(backupControl(dialog, "backupEnabledSwitch"));
        mouseClick(dialog.standardButton(Dialog.Ok));
        it.expect.dialogClosed(control, "backupDialog");
        compare(it.settings.backupInterval(), initialInterval);
    }

    function savedExportValues() {
        return {
            nickname: it.settings.nickname(),
            flags: [it.settings.writeHeaderDate(), it.settings.writeHeaderGenerator(), it.settings.writeHeaderNickname(), it.settings.writeHeaderVideoPath(), it.settings.writeHeaderSubtitles()]
        };
    }

    function openExportSettings(control: Item): QtObject {
        it.menu.trigger(control, "optionsMenu", "openExportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "exportSettingsDialog");
        verify(waitForPolish(dialog.contentItem.Window.window), "export dialog layout should settle");
        const field = findChild(dialog, "exportNicknameField");
        verify(field, "exportNicknameField not found");
        tryCompare(field, "activeFocus", true);
        return dialog;
    }

    function editExportNickname(dialog: QtObject, nickname: string): void {
        const field = findChild(dialog, "exportNicknameField");
        verify(field, "exportNicknameField not found");
        verify(field.enabled && !field.readOnly, "nickname must stay editable");
        mouseClick(field);
        keyClick(Qt.Key_A, Qt.ControlModifier);
        for (const character of nickname) {
            keyClick(character);
        }
        compare(field.text, nickname);
    }

    function test_exportSettingsDialog_savesAndReopensAllSettings(): void {
        const control = it.makeControl();
        const initial = savedExportValues();
        const edited = {
            nickname: "  Export Tester  ",
            flags: initial.flags.map(value => !value)
        };
        let dialog = openExportSettings(control);
        editExportNickname(dialog, edited.nickname);
        for (const row of exportOptionRows(dialog)) {
            const before = row.checked;
            mouseClick(row.toggle);
            tryCompare(row, "checked", !before);
        }
        const nicknameHeader = findChild(dialog, "exportWriteNicknameRow");
        mouseClick(nicknameHeader.toggle);
        tryCompare(nicknameHeader, "checked", false);
        compare(findChild(dialog, "exportNicknameField").text, edited.nickname, "disabling the header must preserve nickname whitespace");
        edited.nickname = "  Still Editable  ";
        editExportNickname(dialog, edited.nickname);
        mouseClick(nicknameHeader.toggle);
        compare(savedExportValues(), initial, "edits must remain temporary");

        mouseClick(dialog.standardButton(Dialog.Ok));
        it.expect.dialogClosed(control, "exportSettingsDialog");
        compare(savedExportValues(), edited);

        dialog = openExportSettings(control);
        compare(findChild(dialog, "exportNicknameField").text, edited.nickname);
        compare(exportOptionRows(dialog).map(row => row.checked), edited.flags);
        mouseClick(dialog.standardButton(Dialog.Cancel));
        it.expect.dialogClosed(control, "exportSettingsDialog");
    }

    function test_exportSettingsDialog_cancelAndEscapeDiscardAllSettings(): void {
        const control = it.makeControl();
        const initial = savedExportValues();
        for (const action of [Dialog.Cancel, Dialog.NoButton]) {
            const dialog = openExportSettings(control);
            compare(findChild(dialog, "exportNicknameField").text, initial.nickname);
            compare(exportOptionRows(dialog).map(row => row.checked), initial.flags);
            editExportNickname(dialog, "Discard Me");
            for (const row of exportOptionRows(dialog)) {
                const before = row.checked;
                mouseClick(row.toggle);
                tryCompare(row, "checked", !before);
            }
            if (action === Dialog.Cancel) {
                mouseClick(dialog.standardButton(Dialog.Cancel));
            } else {
                keyClick(Qt.Key_Escape);
            }
            it.expect.dialogClosed(control, "exportSettingsDialog");
            compare(savedExportValues(), initial);
        }
        const reopened = openExportSettings(control);
        compare(findChild(reopened, "exportNicknameField").text, initial.nickname);
        compare(exportOptionRows(reopened).map(row => row.checked), initial.flags);
    }

    function exportOptionRows(dialog: QtObject): list<var> {
        return ["exportWriteDateRow", "exportWriteGeneratorRow", "exportWriteNicknameRow", "exportWriteVideoPathRow", "exportWriteSubtitlesRow"].map(name => {
            const row = findChild(dialog, name);
            verify(row, `${name} not found`);
            return row;
        });
    }

    function visibleLabel(item: Item): Label {
        if (item instanceof Label && item.visible) {
            return item;
        }
        for (const child of item.children) {
            const label = visibleLabel(child);
            if (label) {
                return label;
            }
        }
        return null;
    }

    function test_exportSettingsDialog_leadingLabelsAndTrailingSwitches_data() {
        return [
            {
                tag: "empty-nickname",
                nickname: ""
            },
            {
                tag: "latin-nickname",
                nickname: "Nickname"
            },
            {
                tag: "hebrew-nickname",
                nickname: "כינוי"
            },
        ];
    }

    function test_exportSettingsDialog_leadingLabelsAndTrailingSwitches(data): void {
        const control = it.makeControl();
        const dialog = openExportSettings(control);
        const field = findChild(dialog, "exportNicknameField");
        field.text = data.nickname;
        dialog.contentItem.LayoutMirroring.childrenInherit = true;
        for (const mirrored of [false, true, false]) {
            dialog.contentItem.LayoutMirroring.enabled = mirrored;
            verify(waitForPolish(dialog.contentItem.Window.window), "export dialog layout should settle after mirroring");
            tryCompare(field, "effectiveHorizontalAlignment", mirrored ? Text.AlignRight : Text.AlignLeft);
            tryVerify(() => {
                const start = field.positionToRectangle(0).x;
                const end = field.positionToRectangle(field.length).x;
                const edge = mirrored ? Math.max(start, end) : Math.min(start, end);
                // positionToRectangle() reports text-layout coordinates, without padding.
                const expected = mirrored ? field.width - field.leftPadding - field.rightPadding : 0;
                return Math.abs(edge - expected) <= 1;
            }, 1000, "nickname text should render at the leading edge");
            for (const row of exportOptionRows(dialog)) {
                const label = visibleLabel(row);
                verify(label, "option label should be visible");
                tryCompare(label, "effectiveHorizontalAlignment", mirrored ? Text.AlignRight : Text.AlignLeft);
                tryVerify(() => {
                    const switchX = row.toggle.mapToItem(row, 0, 0).x;
                    return Math.abs(mirrored ? switchX : row.width - switchX - row.toggle.width) <= 1;
                }, 5000, "switch should sit at the trailing edge");
                const labelX = label.mapToItem(row, 0, 0).x;
                verify(Math.abs(mirrored ? row.width - labelX - label.width : labelX) <= 1, "label should sit at the leading edge");
            }
        }
    }

    function verticallyInside(item: Item, viewport: Item): bool {
        const top = item.mapToItem(viewport, 0, 0).y;
        return top >= -1 && top + item.height <= viewport.height + 1;
    }

    function verifyExportActionsVisible(dialog: QtObject): void {
        for (const action of [Dialog.Ok, Dialog.Cancel]) {
            const button = dialog.standardButton(action);
            verify(button.visible && button.enabled);
            verify(verticallyInside(button, testCase.Window.window.contentItem), "action must fit in the window");
            verify(button.mapToItem(dialog.contentItem, 0, 0).y >= dialog.contentItem.height, "action must stay below the scrolling body");
        }
    }

    function test_exportSettingsDialog_scrollsWithFixedActions(): void {
        const control = it.makeControl();
        let dialog = openExportSettings(control);
        const naturalHeight = dialog.height;
        compare(dialog.contentItem.height, dialog.contentItem.contentHeight, "short content should determine the body height");

        testCase.Window.window.height = 360;
        tryVerify(() => dialog.height <= testCase.Window.window.height, 5000, "dialog must fit the available window height");
        verify(dialog.height < naturalHeight, "body must shrink with the window");
        verifyExportActionsVisible(dialog);
        mouseClick(dialog.standardButton(Dialog.Cancel));
        it.expect.dialogClosed(control, "exportSettingsDialog");

        dialog = openExportSettings(control);
        dialog.contentItem.LayoutMirroring.enabled = true;
        dialog.contentItem.LayoutMirroring.childrenInherit = true;
        verify(waitForPolish(dialog.contentItem.Window.window), "export dialog layout should settle after mirroring");

        const field = findChild(dialog, "exportNicknameField");
        verify(field);
        verify(verticallyInside(field, dialog.contentItem));
        editExportNickname(dialog, "ScrollTester");

        const rows = exportOptionRows(dialog);
        for (const row of rows) {
            for (let attempt = 0; !verticallyInside(row.toggle, dialog.contentItem) && attempt < 10; attempt++) {
                const previousY = row.mapToItem(dialog.contentItem, 0, 0).y;
                mouseWheel(dialog.contentItem, dialog.contentItem.width / 2, dialog.contentItem.height / 2, 0, -120);
                tryVerify(() => row.mapToItem(dialog.contentItem, 0, 0).y < previousY);
                tryVerify(() => !dialog.contentItem.contentItem.moving);
            }
            verify(verticallyInside(row.toggle, dialog.contentItem), "every switch must be reachable by scrolling");
            const initial = row.checked;
            mouseClick(row.toggle);
            tryCompare(row, "checked", !initial);
            verifyExportActionsVisible(dialog);
        }

        mouseClick(dialog.standardButton(Dialog.Ok));
        it.expect.dialogClosed(control, "exportSettingsDialog");
        compare(it.settings.nickname(), "ScrollTester");
    }

    function openImportSettings(control: Item): QtObject {
        it.menu.trigger(control, "optionsMenu", "openImportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "importSettingsDialog");
        verify(waitForPolish(dialog.contentItem.Window.window), "import dialog layout should settle");
        return dialog;
    }

    function test_importSettingsDialog_changeOption_persistsOnAccept(): void {
        const control = it.makeControl();
        const initial = it.settings.loadFoundVideo();
        const dialog = openImportSettings(control);
        const edited = initial === 0 ? 2 : 0;
        const choice = it.find.visualChild(dialog, `loadFoundVideoChoice_${edited}`);
        verify(choice, "import choice not found");
        mouseClick(choice);
        verify(choice.checked);
        compare(it.settings.loadFoundVideo(), initial, "selection must remain staged until OK");

        mouseClick(dialog.standardButton(Dialog.Ok));
        it.expect.dialogClosed(control, "importSettingsDialog");
        compare(it.settings.loadFoundVideo(), edited);
    }

    function test_importSettingsDialog_reject_discardsSettings(): void {
        const control = it.makeControl();
        const initial = it.settings.loadFoundVideo();
        const dialog = openImportSettings(control);
        const edited = initial === 0 ? 2 : 0;
        const choice = it.find.visualChild(dialog, `loadFoundVideoChoice_${edited}`);
        verify(choice, "import choice not found");
        mouseClick(choice);
        verify(choice.checked);

        mouseClick(dialog.standardButton(Dialog.Cancel));
        it.expect.dialogClosed(control, "importSettingsDialog");
        compare(it.settings.loadFoundVideo(), initial);
    }

    function test_editMpvDialog_resetEditAcceptAndLinkActivation(): void {
        const control = it.makeControl();
        const sentinel = "# integration-test-mpv-marker";

        it.menu.trigger(control, "optionsMenu", "openEditMpvConfigDialogMenuItem");
        const dialog = it.find.openedDialog(control, "editMpvDialog");

        const textArea = findChild(dialog, "mpvConfTextArea");
        verify(textArea, "mpvConfTextArea not found");
        const fixtureText = textArea.text;

        const resetButton = dialog.standardButton(Dialog.Reset);
        verify(resetButton, "Reset standard button not found");
        mouseClick(resetButton);
        tryVerify(() => textArea.text !== fixtureText, 5000, "text should change after reset to defaults");
        const defaultText = textArea.text;

        textArea.text = defaultText + "\n" + sentinel + "\n";

        const label = findChild(dialog, "mpvConfLearnMoreLabel");
        verify(label, "mpvConfLearnMoreLabel not found");
        label.linkActivated(label.url);
        tryVerify(() => it.bridge.openedDesktopUrls().includes(label.url));

        it.dialog.accept(dialog);

        tryVerify(() => it.bridge.fileContains(it.bridge.mpvConfPath(), sentinel));
    }

    function test_editInputDialog_resetEditAcceptAndLinkActivation(): void {
        const control = it.makeControl();
        const sentinel = "# integration-test-input-marker";

        it.menu.trigger(control, "optionsMenu", "openEditInputConfigDialogMenuItem");
        const dialog = it.find.openedDialog(control, "editInputDialog");

        const textArea = findChild(dialog, "inputConfTextArea");
        verify(textArea, "inputConfTextArea not found");
        const fixtureText = textArea.text;

        const resetButton = dialog.standardButton(Dialog.Reset);
        verify(resetButton, "Reset standard button not found");
        mouseClick(resetButton);
        tryVerify(() => textArea.text !== fixtureText, 5000, "text should change after reset to defaults");
        const defaultText = textArea.text;

        textArea.text = defaultText + "\n" + sentinel + "\n";

        const label = findChild(dialog, "inputConfLearnMoreLabel");
        verify(label, "inputConfLearnMoreLabel not found");
        label.linkActivated(label.url);
        tryVerify(() => it.bridge.openedDesktopUrls().includes(label.url));

        it.dialog.accept(dialog);

        tryVerify(() => it.bridge.fileContains(it.bridge.inputConfPath(), sentinel));
    }

    function test_languageSubmenu_data() {
        return [
            {
                tag: "german",
                identifier: "de-DE"
            },
            {
                tag: "english",
                identifier: "en-US"
            },
        ];
    }

    function test_languageSubmenu(data): void {
        const control = it.makeControl();
        it.menu.triggerSubItem(control, "optionsMenu", "languageMenu", `languageMenuItem_${data.identifier}`);
        tryVerify(() => it.settings.language() === data.identifier);
    }

    TestHelpers {
        id: it

        testCase: testCase
    }
}
