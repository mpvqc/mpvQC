# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import inject
import pytest

from mpvqc.window.services import (
    NoEmbeddedPlayerTracker,
    NoSurfaceHandler,
    NoWindowConfigurator,
    NoWindowRevealer,
    PlatformBackend,
    PlatformService,
    QtWindowStateHandler,
    WindowButtonPreference,
    linux_tiling_capabilities,
)
from mpvqc.window.viewmodels import (
    MpvqcWindowButtonsViewModel,
    WindowButtonsInputs,
    WindowButtonsProps,
    derive_window_buttons_props,
)

ALL_BUTTONS = WindowButtonPreference(minimize=True, maximize=True, close=True)
NO_BUTTONS = WindowButtonPreference(minimize=False, maximize=False, close=False)
NO_MAXIMIZE = WindowButtonPreference(minimize=True, maximize=False, close=True)
CLOSE_ONLY = WindowButtonPreference(minimize=False, maximize=False, close=True)


class FakeWindowButtons:
    def __init__(self, preference: WindowButtonPreference) -> None:
        self._preference = preference
        self._callbacks: list[Callable[[WindowButtonPreference], None]] = []

    @property
    def preference(self) -> WindowButtonPreference:
        return self._preference

    def on_preference_changed(self, callback: Callable[[WindowButtonPreference], None]) -> None:
        self._callbacks.append(callback)

    def push(self, preference: WindowButtonPreference) -> None:
        self._preference = preference
        for callback in self._callbacks:
            callback(preference)


@pytest.fixture
def window_button_source() -> FakeWindowButtons:
    return FakeWindowButtons(ALL_BUTTONS)


@pytest.fixture
def platform_service(qt_app, window_button_source) -> PlatformService:
    backend = PlatformBackend(
        capabilities=linux_tiling_capabilities(),
        window_state=QtWindowStateHandler(),
        surface=NoSurfaceHandler(),
        window_configuration=NoWindowConfigurator(),
        window_reveal=NoWindowRevealer(),
        embedded_player=NoEmbeddedPlayerTracker(),
        window_buttons=window_button_source,
    )
    return PlatformService(backend)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, platform_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlatformService, platform_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcWindowButtonsViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcWindowButtonsViewModel()

    return _make


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(view_model: MpvqcWindowButtonsViewModel) -> dict:
        return {
            "showMinimizeButton": make_spy(view_model.showMinimizeButtonChanged),
            "showMaximizeButton": make_spy(view_model.showMaximizeButtonChanged),
            "showCloseButton": make_spy(view_model.showCloseButtonChanged),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items()}


class DerivationCase(NamedTuple):
    name: str
    inputs: WindowButtonsInputs
    expected: WindowButtonsProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="every button drawn",
            inputs=WindowButtonsInputs(preference=ALL_BUTTONS),
            expected=WindowButtonsProps(
                show_minimize_button=True,
                show_maximize_button=True,
                show_close_button=True,
            ),
        ),
        DerivationCase(
            name="no button drawn",
            inputs=WindowButtonsInputs(preference=NO_BUTTONS),
            expected=WindowButtonsProps(
                show_minimize_button=False,
                show_maximize_button=False,
                show_close_button=False,
            ),
        ),
        DerivationCase(
            name="maximize dropped",
            inputs=WindowButtonsInputs(preference=NO_MAXIMIZE),
            expected=WindowButtonsProps(
                show_minimize_button=True,
                show_maximize_button=False,
                show_close_button=True,
            ),
        ),
        DerivationCase(
            name="close alone",
            inputs=WindowButtonsInputs(preference=CLOSE_ONLY),
            expected=WindowButtonsProps(
                show_minimize_button=False,
                show_maximize_button=False,
                show_close_button=True,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_window_buttons_props(case.inputs) == case.expected


def test_initial_snapshot_reads_the_platform_at_construction(make_view_model, window_button_source):
    window_button_source.push(CLOSE_ONLY)

    view_model = make_view_model()

    assert not view_model.showMinimizeButton
    assert not view_model.showMaximizeButton
    assert view_model.showCloseButton


def test_dropped_maximize_emits_the_maximize_notify_alone(make_view_model, window_button_source, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    window_button_source.push(NO_MAXIMIZE)

    assert emissions(spies) == {"showMinimizeButton": 0, "showMaximizeButton": 1, "showCloseButton": 0}
    assert spies["showMaximizeButton"].at(0, 0) is False
    assert view_model.showMinimizeButton
    assert not view_model.showMaximizeButton
    assert view_model.showCloseButton


def test_losing_every_button_emits_all_three(make_view_model, window_button_source, spy_notifies):
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    window_button_source.push(NO_BUTTONS)

    assert emissions(spies) == {"showMinimizeButton": 1, "showMaximizeButton": 1, "showCloseButton": 1}
    assert spies["showMinimizeButton"].at(0, 0) is False
    assert spies["showMaximizeButton"].at(0, 0) is False
    assert spies["showCloseButton"].at(0, 0) is False


def test_repeated_preference_emits_nothing(make_view_model, window_button_source, spy_notifies):
    # WindowButtonDetector drops a repeat before it pushes, so only this fake can drive one in.
    view_model = make_view_model()
    spies = spy_notifies(view_model)

    window_button_source.push(ALL_BUTTONS)

    assert emissions(spies) == {"showMinimizeButton": 0, "showMaximizeButton": 0, "showCloseButton": 0}


def test_props_swap_completes_before_the_first_emission(make_view_model, window_button_source):
    view_model = make_view_model()
    observed: list[tuple[bool, bool, bool]] = []

    view_model.showMinimizeButtonChanged.connect(
        lambda _: observed.append(
            (view_model.showMinimizeButton, view_model.showMaximizeButton, view_model.showCloseButton)
        )
    )

    window_button_source.push(NO_BUTTONS)

    assert observed == [(False, False, False)]
