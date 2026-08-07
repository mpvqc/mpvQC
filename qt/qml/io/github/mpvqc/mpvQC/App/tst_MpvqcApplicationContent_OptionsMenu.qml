// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::OptionsMenu"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    function init(): void {
        it.resetState();
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

    function test_applicationLayoutRadio_data() {
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

    function test_applicationLayoutRadio(data): void {
        const control = it.makeControl();
        it.menu.triggerSubItem(control, "optionsMenu", "applicationLayoutMenu", `applicationLayoutMenuRadioItem_${data.identifier}`);
        tryVerify(() => it.settings.layoutOrientation() === data.expected);

        const splitView = findChild(control, "applicationSplitView");
        verify(splitView, "applicationSplitView not found");
        tryVerify(() => splitView.orientation === data.expected);
    }

    function test_backupDialog_drivesAllSettingsAndOpensFolder(): void {
        const control = it.makeControl();

        const initialEnabled = it.settings.backupEnabled();
        const initialInterval = it.settings.backupInterval();
        const newEnabled = !initialEnabled;
        const newInterval = initialInterval + 30;

        it.menu.trigger(control, "optionsMenu", "openBackupSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "backupDialog");

        const switchRow = findChild(dialog, "backupEnabledRow");
        verify(switchRow, "backupEnabledRow not found");
        switchRow.checked = newEnabled;

        const intervalRow = findChild(dialog, "backupIntervalRow");
        verify(intervalRow, "backupIntervalRow not found");
        intervalRow.value = newInterval;

        const locationButton = findChild(dialog, "backupOpenLocationButton");
        verify(locationButton, "backupOpenLocationButton not found");
        mouseClick(locationButton);
        tryVerify(() => it.bridge.openedDesktopUrls().includes("mpvqc-test://backup-folder"));

        it.dialog.accept(dialog);

        tryVerify(() => it.settings.backupEnabled() === newEnabled);
        tryVerify(() => it.settings.backupInterval() === newInterval);
    }

    function test_backupDialog_reject_discardsSettings(): void {
        const control = it.makeControl();

        const initialEnabled = it.settings.backupEnabled();
        const initialInterval = it.settings.backupInterval();

        it.menu.trigger(control, "optionsMenu", "openBackupSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "backupDialog");

        const switchRow = findChild(dialog, "backupEnabledRow");
        verify(switchRow, "backupEnabledRow not found");
        switchRow.checked = !initialEnabled;

        const intervalRow = findChild(dialog, "backupIntervalRow");
        verify(intervalRow, "backupIntervalRow not found");
        intervalRow.value = initialInterval + 30;

        it.dialog.reject(dialog);

        verify(it.settings.backupEnabled() === initialEnabled, "backup enabled should be unchanged after reject");
        verify(it.settings.backupInterval() === initialInterval, "backup interval should be unchanged after reject");
    }

    function test_exportSettingsDialog_drivesAllSettings(): void {
        const control = it.makeControl();

        const initial = {
            nickname: it.settings.nickname(),
            date: it.settings.writeHeaderDate(),
            generator: it.settings.writeHeaderGenerator(),
            nicknameHeader: it.settings.writeHeaderNickname(),
            videoPath: it.settings.writeHeaderVideoPath(),
            subtitles: it.settings.writeHeaderSubtitles()
        };
        const newNickname = initial.nickname + "-edited";

        it.menu.trigger(control, "optionsMenu", "openExportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "exportSettingsDialog");

        const nicknameRow = findChild(dialog, "exportNicknameRow");
        verify(nicknameRow, "exportNicknameRow not found");
        nicknameRow.input = newNickname;

        const switchRows = ["exportWriteDateRow", "exportWriteGeneratorRow", "exportWriteNicknameRow", "exportWriteVideoPathRow", "exportWriteSubtitlesRow"];
        for (const name of switchRows) {
            const row = findChild(dialog, name);
            verify(row, `${name} not found`);
            row.checked = !row.checked;
        }

        it.dialog.accept(dialog);

        tryVerify(() => it.settings.nickname() === newNickname);
        tryVerify(() => it.settings.writeHeaderDate() === !initial.date);
        tryVerify(() => it.settings.writeHeaderGenerator() === !initial.generator);
        tryVerify(() => it.settings.writeHeaderNickname() === !initial.nicknameHeader);
        tryVerify(() => it.settings.writeHeaderVideoPath() === !initial.videoPath);
        tryVerify(() => it.settings.writeHeaderSubtitles() === !initial.subtitles);
    }

    function test_exportSettingsDialog_reject_discardsSettings(): void {
        const control = it.makeControl();

        const initialNickname = it.settings.nickname();
        const initialDate = it.settings.writeHeaderDate();

        it.menu.trigger(control, "optionsMenu", "openExportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "exportSettingsDialog");

        const nicknameRow = findChild(dialog, "exportNicknameRow");
        verify(nicknameRow, "exportNicknameRow not found");
        nicknameRow.input = initialNickname + "-edited";

        const dateRow = findChild(dialog, "exportWriteDateRow");
        verify(dateRow, "exportWriteDateRow not found");
        dateRow.checked = !initialDate;

        it.dialog.reject(dialog);

        verify(it.settings.nickname() === initialNickname, "nickname should be unchanged after reject");
        verify(it.settings.writeHeaderDate() === initialDate, "write header date should be unchanged after reject");
    }

    function test_importSettingsDialog_changeOption_persistsOnAccept(): void {
        const control = it.makeControl();
        const initial = it.settings.loadFoundVideo();

        it.menu.trigger(control, "optionsMenu", "openImportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "importSettingsDialog");

        const comboBox = findChild(dialog, "loadFoundVideoComboBox");
        verify(comboBox, "loadFoundVideoComboBox not found");
        const newIndex = comboBox.currentIndex === 0 ? comboBox.count - 1 : 0;
        verify(newIndex !== comboBox.currentIndex, "expected to pick a different option");
        comboBox.activated(newIndex);

        it.dialog.accept(dialog);
        tryVerify(() => it.settings.loadFoundVideo() === newIndex);
        verify(it.settings.loadFoundVideo() !== initial, "setting should differ from initial value");
    }

    function test_importSettingsDialog_reject_discardsSettings(): void {
        const control = it.makeControl();
        const initial = it.settings.loadFoundVideo();

        it.menu.trigger(control, "optionsMenu", "openImportSettingsDialogMenuItem");
        const dialog = it.find.openedDialog(control, "importSettingsDialog");

        const comboBox = findChild(dialog, "loadFoundVideoComboBox");
        verify(comboBox, "loadFoundVideoComboBox not found");
        const newIndex = comboBox.currentIndex === 0 ? comboBox.count - 1 : 0;
        verify(newIndex !== comboBox.currentIndex, "expected to pick a different option");
        comboBox.activated(newIndex);

        it.dialog.reject(dialog);

        verify(it.settings.loadFoundVideo() === initial, "load found video should be unchanged after reject");
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
