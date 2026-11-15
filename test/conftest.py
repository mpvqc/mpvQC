# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import deque
from configparser import RawConfigParser, SectionProxy
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, override

import inject
import pytest
from hypothesis import settings
from PySide6.QtCore import (
    QByteArray,
    QCoreApplication,
    QLocale,
    QMetaMethod,
    QObject,
    QResource,
    QSettings,
    SignalInstance,
)
from PySide6.QtTest import QSignalSpy

from mpvqc.application import MpvqcApplication
from mpvqc.build import BuildInfo
from mpvqc.comments import bindings as comments_bindings
from mpvqc.comments.services import CommentsSettingsService
from mpvqc.exporting.services import ExportSettingsService, ExportTemplateCatalogService
from mpvqc.i18n.services import I18nSettingsService, InternationalizationService
from mpvqc.player.services import PlayerService
from mpvqc.session import SessionService
from mpvqc.settings import open_settings_file
from mpvqc.shell.services import ShellSettingsService
from test.player.recording import RecordingPlayerHandle

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

settings.register_profile("fuzz", max_examples=10_000, deadline=None, print_blob=True)


@pytest.fixture
def player_handle(qt_app) -> RecordingPlayerHandle:
    return RecordingPlayerHandle()


@pytest.fixture
def player_service(player_handle) -> PlayerService:
    return PlayerService(player_handle)


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


def _declared_signal_names(recorded: QObject) -> list[str]:
    meta_object = recorded.metaObject()
    # found by walking up, because QObject.staticMetaObject reads None once a test's application has shut down;
    # the stubs type superClass() as never None, yet it is None at the root and ends the walk
    root = meta_object
    while (parent := root.superClass()) is not None:
        root = parent
    return [
        meta_object.method(index).name().toStdString()
        for index in range(root.methodCount(), meta_object.methodCount())
        if meta_object.method(index).methodType() == QMetaMethod.MethodType.Signal
    ]


class EmissionRecorder:
    def __init__(self, recorded: QObject):
        self._class_name = type(recorded).__name__
        names = _declared_signal_names(recorded)
        if not names:
            message = f"{self._class_name} declares no signal to record"
            raise TypeError(message)
        for name in names:
            if names.count(name) > 1:
                message = f"{self._class_name} declares two signals named {name}"
                raise TypeError(message)
        self._spies = {name: MySpy(getattr(recorded, name)) for name in names}

    def assert_exactly(self, **counts: int) -> None:
        __tracebackhide__ = True
        for name in counts:
            self._require_declared(name)
        expected = {name: count for name, count in counts.items() if count != 0}
        fired = {name: spy.count() for name, spy in self._spies.items() if spy.count() != 0}
        if expected != fired:
            message = (
                f"{self._class_name} did not emit exactly the expected signals\nexpected: {expected}\nrecorded: {fired}"
            )
            raise AssertionError(message)

    def assert_silent(self) -> None:
        __tracebackhide__ = True
        self.assert_exactly()

    def __getitem__(self, signal_name: str) -> MySpy:
        __tracebackhide__ = True
        self._require_declared(signal_name)
        return self._spies[signal_name]

    def _require_declared(self, signal_name: str) -> None:
        __tracebackhide__ = True
        if signal_name not in self._spies:
            declared = ", ".join(self._spies)
            message = f"{self._class_name} declares no signal named {signal_name!r}\ndeclared: {declared}"
            raise AssertionError(message)


@pytest.fixture(scope="session")
def record_emissions() -> Callable[[QObject], EmissionRecorder]:
    return EmissionRecorder


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


@pytest.fixture
def make_build_info() -> Callable[..., BuildInfo]:
    def _make(
        *,
        version: str = "1.0.0",
        is_release: bool = True,
        origin: str = "mpvqc-github",
        offers_update_check: bool = False,
    ) -> BuildInfo:
        return BuildInfo(
            name="mpvQC",
            app_id="io.github.mpvqc.mpvQC",
            organization="mpvQC",
            domain="mpvqc.github.io",
            version=version,
            commit="abc12345",
            is_release=is_release,
            origin=origin,
            offers_update_check=offers_update_check,
            dependencies=(),
            dev_dependencies=(),
        )

    return _make


@pytest.fixture
def session_service() -> SessionService:
    return SessionService()


@pytest.fixture
def configure_session(session_service) -> Callable:
    from mpvqc.session import SessionState

    def _configure(**kwargs):
        # noinspection PyProtectedMember
        old = session_service._state
        session_service._set(
            SessionState(
                document=kwargs.get("document", old.document),
                saved=bool(kwargs.get("saved", old.saved)),
            )
        )

    return _configure


@pytest.fixture
def qsettings(tmp_path) -> QSettings:
    return open_settings_file(tmp_path / "test_settings.ini")


class QSettingsIniParser(RawConfigParser):
    """Reads an ini the way QSettings wrote it: raw, because the interpolating parser rejects the percent
    signs QSettings leaves in values, and case-sensitive, because it writes its keys in camel case."""

    @override
    def optionxform(self, optionstr: str) -> str:
        return optionstr


@pytest.fixture
def ini_section(qsettings, tmp_path) -> Callable[[str], SectionProxy]:
    def _section(name: str) -> SectionProxy:
        qsettings.sync()
        parser = QSettingsIniParser()
        parser.read(tmp_path / "test_settings.ini")
        return parser[name]

    return _section


@pytest.fixture
def read_existing_settings(tmp_path) -> Callable[[str], QSettings]:
    def _read(content: str) -> QSettings:
        file = tmp_path / "existing_settings.ini"
        file.write_text(dedent(content).lstrip())
        # a handle that never wrote the file, because QSettings serves a writer its own values back typed,
        # hiding that an ini hands every value to a later run as text
        return QSettings(str(file), QSettings.Format.IniFormat)

    return _read


@pytest.fixture
def comments_settings_service(qsettings) -> CommentsSettingsService:
    return CommentsSettingsService(qsettings)


@pytest.fixture
def export_settings_service(qsettings) -> ExportSettingsService:
    return ExportSettingsService(qsettings)


@pytest.fixture
def shell_settings_service(qsettings) -> ShellSettingsService:
    return ShellSettingsService(qsettings)


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


@pytest.fixture
def common_bindings_with(qsettings):
    def i18n_settings_service() -> I18nSettingsService:
        return I18nSettingsService(qsettings)

    def _configure(*custom_configs):
        def config(binder: inject.Binder):
            binder.bind(QSettings, qsettings)
            comments_bindings(binder)
            binder.bind_to_constructor(ExportTemplateCatalogService, ExportTemplateCatalogService)
            binder.bind_to_constructor(I18nSettingsService, i18n_settings_service)
            binder.bind_to_constructor(InternationalizationService, InternationalizationService)
            binder.bind_to_constructor(SessionService, SessionService)

            for custom_config in custom_configs:
                custom_config(binder)

        inject.configure(config, allow_override=True, bind_in_runtime=False, clear=True)

    return _configure
