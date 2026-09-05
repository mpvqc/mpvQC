# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.i18n.services import I18nSettingsService, InternationalizationService


@pytest.fixture
def i18n_settings_service(settings_file) -> I18nSettingsService:
    return I18nSettingsService(settings_file.qsettings)


@pytest.fixture
def internationalization_service() -> InternationalizationService:
    return InternationalizationService()
