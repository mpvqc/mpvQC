# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appearance.services import AppearanceSettingsService


@pytest.fixture
def appearance_settings_service(settings_file) -> AppearanceSettingsService:
    return AppearanceSettingsService(settings_file.qsettings)
