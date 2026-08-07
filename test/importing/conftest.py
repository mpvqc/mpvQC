# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.importing.services import ImportSettingsService


@pytest.fixture
def import_settings_service(settings_file) -> ImportSettingsService:
    return ImportSettingsService(settings_file.qsettings)
