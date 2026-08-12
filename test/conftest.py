# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import deque
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any, override

import inject
import pytest
from PySide6.QtCore import QByteArray, QCoreApplication, QLocale, QResource, SignalInstance
from PySide6.QtTest import QSignalSpy

from mpvqc.application import MpvqcApplication
from mpvqc.services import (
    BuildInfoService,
    CommentsService,
    ExportSettingsService,
    ExportTemplateCatalogService,
    InternationalizationService,
    PlayerService,
    ResourceService,
    SettingsFileService,
    SettingsService,
    StateService,
    TimeFormatterService,
    TypeMapperService,
)
from mpvqc.services.player.state import OBSERVED_PROPERTIES, RawPropertyValue, make_observer


class FakePlayerService(PlayerService):
    """Stands in for mpv: raw values pass through the production observers,
    so coercion, dedupe, and signal emission match the real service."""

    def __init__(self) -> None:
        super().__init__()
        self._raw_time_pos: float | None = None
        self._observers = {spec.name: make_observer(spec, self._apply_property_update) for spec in OBSERVED_PROPERTIES}

    @property
    @override
    def exact_time_pos(self) -> float:
        if self._raw_time_pos is not None:
            return self._raw_time_pos
        return super().exact_time_pos

    def load_video(self, path: str) -> None:
        self._observe("path", path)
        self._observe("filename", Path(path).name)

    def unload_video(self) -> None:
        self._raw_time_pos = None
        self._observe("path", None)

    def update(
        self,
        *,
        duration: float | None = None,
        percent_pos: float | None = None,
        time_pos: float | None = None,
        time_remaining: float | None = None,
        height: int | None = None,
        width: int | None = None,
        track_list: list[dict] | None = None,
    ) -> None:
        if duration is not None:
            # the reducer matches float instances, an int literal would be dropped
            self._observe("duration", duration + 0.0)
        if percent_pos is not None:
            self._observe("percent-pos", percent_pos)
        if time_pos is not None:
            self._raw_time_pos = time_pos
            self._observe("time-pos", time_pos)
        if time_remaining is not None:
            self._observe("time-remaining", time_remaining)
        if height is not None:
            self._observe("height", height)
        if width is not None:
            self._observe("width", width)
        if track_list is not None:
            self._observe("track-list", track_list)

    def _observe(self, name: str, raw: RawPropertyValue) -> None:
        self._observers[name](name, raw)


@pytest.fixture
def fake_player_service() -> FakePlayerService:
    return FakePlayerService()


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


class ManualJobExecutor:
    def __init__(self) -> None:
        self.pending: deque[Callable[[], None]] = deque()

    def execute(self, work: Callable[[], None]) -> None:
        self.pending.append(work)

    def run_next(self) -> None:
        self.pending.popleft()()

    def drain(self) -> None:
        while self.pending:
            self.run_next()


@pytest.fixture
def manual_executor() -> ManualJobExecutor:
    return ManualJobExecutor()


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
        state_service._set(
            ApplicationState(
                document=kwargs.get("document", old.document),
                saved=bool(kwargs.get("saved", old.saved)),
            )
        )

    return _configure


@pytest.fixture
def settings_file(tmp_path, type_mapper) -> SettingsFileService:
    file = tmp_path / "test_settings.ini"
    return SettingsFileService(ini_file=type_mapper.map_path_to_str(file))


@pytest.fixture
def settings_service(settings_file) -> SettingsService:
    return SettingsService(settings_file.qsettings)


@pytest.fixture
def export_settings_service(settings_file) -> ExportSettingsService:
    return ExportSettingsService(settings_file.qsettings)


@pytest.fixture(autouse=True)
def restore_default_locale():
    locale = QLocale()
    yield
    QLocale.setDefault(locale)


@pytest.fixture(autouse=True)
def clear_injector():
    yield
    inject.clear()


@pytest.fixture
def qt_app() -> Generator[MpvqcApplication, Any]:
    QCoreApplication.setApplicationName("TestApp")
    app = MpvqcApplication([])
    yield app
    app.shutdown()


@pytest.fixture(scope="session", autouse=True)
def check_generated_resources():
    resources = Path(__file__).resolve().parent / "project.rcc"
    if not QResource.registerResource(str(resources)):
        message = (
            f"Can not register resource file '{resources}'\n"
            "To execute individual tests, please run 'just test-python' once before"
        )
        raise FileNotFoundError(message)


@pytest.fixture(scope="session")
def common_bindings_with():
    def _configure(*custom_configs):
        def config(binder: inject.Binder):
            # Common & shared services
            binder.bind_to_constructor(BuildInfoService, BuildInfoService)
            binder.bind_to_constructor(CommentsService, CommentsService)
            binder.bind_to_constructor(ExportTemplateCatalogService, ExportTemplateCatalogService)
            binder.bind_to_constructor(InternationalizationService, InternationalizationService)
            binder.bind_to_constructor(ResourceService, ResourceService)
            binder.bind_to_constructor(StateService, StateService)
            binder.bind_to_constructor(TimeFormatterService, TimeFormatterService)
            binder.bind_to_constructor(TypeMapperService, TypeMapperService)

            # Custom services
            for custom_config in custom_configs:
                custom_config(binder)

        inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)

    return _configure
