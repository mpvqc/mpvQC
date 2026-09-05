# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.i18n.services import I18nSettingsService, default_language


def test_language_falls_back_to_the_default_language(i18n_settings_service):
    assert i18n_settings_service.language == default_language()


def test_language_set_and_get(i18n_settings_service):
    i18n_settings_service.language = "he-IL"

    assert i18n_settings_service.language == "he-IL"


def test_language_writes_into_the_common_ini_section(i18n_settings_service, ini_section):
    i18n_settings_service.language = "he-IL"

    assert ini_section("Common")["language"] == "he-IL"


def test_language_stored_by_an_earlier_run_is_read_back(read_existing_settings):
    qsettings = read_existing_settings(
        """
        [Common]
        language=he-IL
        """
    )

    assert I18nSettingsService(qsettings).language == "he-IL"


def test_language_write_emits_the_language_once(i18n_settings_service, make_spy):
    spy = make_spy(i18n_settings_service.language_changed)

    i18n_settings_service.language = "he-IL"

    assert spy.count() == 1
    assert spy.at(0, 0) == "he-IL"

    i18n_settings_service.language = "he-IL"
    assert spy.count() == 1
