# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import NamedTuple, NewType

type Rect = tuple[int, int, int, int]
"""left, top, right, bottom, the order a Win32 RECT uses."""

WindowRect = NewType("WindowRect", Rect)
ProposedRect = NewType("ProposedRect", Rect)
MonitorRect = NewType("MonitorRect", Rect)
WorkArea = NewType("WorkArea", Rect)
ClientRect = NewType("ClientRect", Rect)


class MonitorGeometry(NamedTuple):
    monitor_rect: MonitorRect
    work_area: WorkArea


def overhangs(rect: WindowRect | ProposedRect, monitor_rect: MonitorRect) -> bool:
    return _covers(rect, monitor_rect) and rect != monitor_rect


def _covers(rect: Rect, monitor_rect: MonitorRect) -> bool:
    left, top, right, bottom = rect
    m_left, m_top, m_right, m_bottom = monitor_rect
    return left <= m_left and top <= m_top and right >= m_right and bottom >= m_bottom
