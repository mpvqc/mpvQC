# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

from mpvqc.importing.services import ImporterService, MimetypeProviderService


def bindings(binder: inject.Binder) -> None:
    binder.bind_to_constructor(ImporterService, ImporterService)
    binder.bind_to_constructor(MimetypeProviderService, MimetypeProviderService)
