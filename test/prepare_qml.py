# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlEngine

from mpvqc import startup
from mpvqc.injections import bindings as original_bindings
from mpvqc.services import HostIntegrationService, WindowPropertiesService


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, _: QQmlEngine):
        import rc_project  # noqa: F401

        startup.configure_qt_application_data()
        startup.configure_qt_settings()
        configure_dependency_injection()
        startup.configure_environment_variables()
        startup.import_mpvqc_bindings()


class _StubWindowPropertiesService(WindowPropertiesService):
    def __init__(self):
        QObject.__init__(self)
        self._width = 0
        self._height = 0
        self._is_fullscreen = False
        self._is_maximized = False


def configure_dependency_injection():
    def test_bindings(binder: inject.Binder):
        original_bindings(binder)
        binder.bind_to_constructor(
            HostIntegrationService,
            lambda: HostIntegrationService(detect_configuration=False),
        )
        binder.bind(WindowPropertiesService, _StubWindowPropertiesService())

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)
