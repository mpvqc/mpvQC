# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ruff: noqa: F401
import logging
import platform

logger = logging.getLogger(__name__)

if platform.system() == "Windows":
    from .player_win_id import MpvWindowPyObject
else:
    from .player_framebuffer_object_offscreen import MpvqcMpvFrameBufferObjectPyObject
