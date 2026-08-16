# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import multiprocessing
import os
import sys
from typing import NamedTuple

import pytest

from mpvqc.window.services.linux import apply_wayland_content_margins, high_dpi_factor

WINDOW_GEOMETRY = "mpvqc.window.services.linux.window_geometry"


class ScaledMarginTestCase(NamedTuple):
    name: str
    factor: float
    margin: int
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ScaledMarginTestCase(
            name="factor_one_passes_margin_through",
            factor=1.0,
            margin=88,
            expected=88,
        ),
        ScaledMarginTestCase(
            name="fractional_factor_scales_margin",
            factor=1.25,
            margin=88,
            expected=110,
        ),
        ScaledMarginTestCase(
            name="fractional_result_rounds_to_nearest",
            factor=1.1,
            margin=88,
            expected=97,
        ),
        ScaledMarginTestCase(
            name="half_rounds_up_like_qround",
            factor=1.25,
            margin=10,
            expected=13,
        ),
        ScaledMarginTestCase(
            name="zero_margin_stays_zero",
            factor=1.25,
            margin=0,
            expected=0,
        ),
    ],
    ids=lambda case: case.name,
)
def test_content_margins_reach_native_call_in_native_units(
    case: ScaledMarginTestCase, make_recording_window, monkeypatch
):
    recorded: list[tuple[int, int, int, int]] = []

    def fake_handle(_window_ptr):
        return 4096

    def fake_set_custom_margins(_wayland_window_ptr, margins_ref):
        margins = margins_ref._obj
        recorded.append((margins.left, margins.top, margins.right, margins.bottom))

    monkeypatch.setattr(f"{WINDOW_GEOMETRY}._resolve_symbols", lambda: (fake_handle, fake_set_custom_margins))
    monkeypatch.setattr(f"{WINDOW_GEOMETRY}.high_dpi_factor", lambda _window: case.factor)

    apply_wayland_content_margins(make_recording_window(), case.margin)

    expected = (case.expected, case.expected, case.expected, case.expected)
    assert recorded == [expected]


@pytest.mark.skipif(sys.platform == "win32", reason="reads the bundled Linux Qt libraries")
def test_high_dpi_factor_reads_one_without_env_scale_factors(qt_app, make_recording_window):
    assert high_dpi_factor(make_recording_window()) == pytest.approx(1.0)


def test_high_dpi_factor_defaults_to_one_without_symbols(make_recording_window, monkeypatch):
    monkeypatch.setattr(f"{WINDOW_GEOMETRY}._resolve_scale_and_origin", lambda: None)

    assert high_dpi_factor(make_recording_window()) == pytest.approx(1.0)


def _read_factor_with_env_scale_factor(env_var, value, result):
    os.environ[env_var] = value
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PySide6.QtGui import QGuiApplication, QWindow

    from mpvqc.window.services.linux import high_dpi_factor

    QGuiApplication([])
    result.put(high_dpi_factor(QWindow()))


class EnvScaleFactorTestCase(NamedTuple):
    name: str
    env_var: str
    value: str
    expected: float


@pytest.mark.skipif(sys.platform == "win32", reason="reads the bundled Linux Qt libraries")
@pytest.mark.parametrize(
    "case",
    [
        EnvScaleFactorTestCase(
            name="global_scale_factor",
            env_var="QT_SCALE_FACTOR",
            value="1.25",
            expected=1.25,
        ),
        EnvScaleFactorTestCase(
            name="per_screen_scale_factors",
            env_var="QT_SCREEN_SCALE_FACTORS",
            value="1.5",
            expected=1.5,
        ),
    ],
    ids=lambda case: case.name,
)
def test_high_dpi_factor_follows_env_scale_factors(case: EnvScaleFactorTestCase):
    # A spawned interpreter, because the factor freezes when QGuiApplication
    # starts and the suite's is already running.
    context = multiprocessing.get_context("spawn")
    result = context.Queue()
    process = context.Process(
        target=_read_factor_with_env_scale_factor,
        args=(case.env_var, case.value, result),
    )
    process.start()
    factor = result.get(timeout=30)
    process.join(timeout=30)

    assert factor == pytest.approx(case.expected)
