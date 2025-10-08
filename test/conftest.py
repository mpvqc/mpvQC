# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Generator
from importlib.util import find_spec
from typing import Any

import pytest
from PySide6.QtCore import QByteArray, SignalInstance
from PySide6.QtTest import QSignalSpy

from mpvqc.application import MpvqcApplication
from mpvqc.services import SettingsService, StateService, TypeMapperService


class MySpy:
    def __init__(self, signal: SignalInstance):
        self._signal = signal
        self._recreate()

    def _recreate(self) -> None:
        self._qt_spy = QSignalSpy(self._signal)
        assert self._qt_spy.isValid()

    def at(self, invocation: int, argument: int) -> Any:
        return self._qt_spy.at(invocation)[argument]

    def count(self) -> int:
        return self._qt_spy.count()

    def is_valid(self) -> bool:
        return self._qt_spy.isValid()

    def signal(self) -> QByteArray:
        return self._qt_spy.signal()

    def size(self) -> int:
        return self._qt_spy.size()

    def wait(self, timeout: int) -> bool:
        return self._qt_spy.wait(timeout)

    def reset(self):
        self._recreate()


@pytest.fixture(scope="session")
def make_spy():
    def _make(signal):
        return MySpy(signal)

    return _make


@pytest.fixture(scope="session")
def type_mapper() -> TypeMapperService:
    return TypeMapperService()


@pytest.fixture
def state_service() -> StateService:
    return StateService()


@pytest.fixture
def configure_state(state_service) -> Callable:
    from mpvqc.services.state import ApplicationState

    def _configure(**kwargs):
        # noinspection PyProtectedMember
        old = state_service._state
        state_service._state = ApplicationState(
            document=kwargs.get("document", old.document),
            video=kwargs.get("video", old.video),
            saved=bool(kwargs.get("saved", old.saved)),
        )

    return _configure


@pytest.fixture
def settings_service(tmp_path, type_mapper):
    file = tmp_path / "test_settings.ini"
    return SettingsService(ini_file=type_mapper.map_path_to_str(file))


@pytest.fixture(scope="session", autouse=True)
def qt_app() -> Generator[MpvqcApplication, Any]:
    app = MpvqcApplication([])
    yield app
    app.shutdown()


@pytest.fixture(scope="session", autouse=True)
def check_generated_resources():
    if find_spec("test.rc_project") is None:
        message = (
            "Can not find resource module 'test.rc_project'\n"
            "To execute individual tests, please run 'just test-python' once before"
        )
        raise FileNotFoundError(message)
    import test.rc_project  # noqa: F401
