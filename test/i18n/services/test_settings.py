# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QLocale

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


def test_missing_language_uses_current_system_language_only_when_needed(settings_file, monkeypatch, make_spy):
    calls = []
    locale = "de_DE"

    def system_locale():
        calls.append(locale)
        return QLocale(locale)

    monkeypatch.setattr(QLocale, "system", system_locale)
    service = I18nSettingsService(settings_file.qsettings)
    spy = make_spy(service.language_changed)
    assert calls == []
    assert service.language == "de-DE"
    locale = "he_IL"
    assert service.language == "he-IL"
    service.language = "he-IL"
    assert calls == ["de_DE", "he_IL", "he_IL"]
    assert not settings_file.qsettings.contains("Common/language")
    assert spy.count() == 0

    settings_file.qsettings.setValue("Common/language", "")
    assert (service.language, calls) == ("", ["de_DE", "he_IL", "he_IL"])
    settings_file.qsettings.remove("Common/language")
    assert service.language == "he-IL"
    assert calls == ["de_DE", "he_IL", "he_IL", "he_IL"]


@pytest.mark.parametrize(
    "stored",
    [
        pytest.param("", id="empty"),
        pytest.param("@Invalid()", id="invalid"),
    ],
)
def test_a_present_empty_language_stays_empty_without_rewriting(read_existing_settings, make_spy, stored):
    store = read_existing_settings(f"[Common]\nlanguage={stored}\n")
    original = store.value("Common/language")
    service = I18nSettingsService(store)
    spy = make_spy(service.language_changed)

    assert not service.language
    service.language = ""

    assert store.contains("Common/language")
    assert store.value("Common/language") == original
    assert spy.count() == 0
