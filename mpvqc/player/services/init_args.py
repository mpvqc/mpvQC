# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from mpvqc.shared import map_path_to_str

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def make_embedded_init_args(
    *,
    win_id: int,
    config_dir: Path,
    screenshot_directory: Path,
    audio_client_name: str,
) -> dict:
    args = _make_shared_args(
        config_dir=config_dir,
        screenshot_directory=screenshot_directory,
        audio_client_name=audio_client_name,
    )
    return args | {"wid": win_id}


def make_in_scene_init_args(
    *,
    config_dir: Path,
    screenshot_directory: Path,
    audio_client_name: str,
) -> dict:
    args = _make_shared_args(
        config_dir=config_dir,
        screenshot_directory=screenshot_directory,
        audio_client_name=audio_client_name,
    )
    return args | {"vo": "libmpv"}


def _make_shared_args(*, config_dir: Path, screenshot_directory: Path, audio_client_name: str) -> dict:
    args: dict = {
        "keep_open": "yes",
        "idle": "yes",
        "osc": "yes",
        "cursor_autohide": "no",
        "input_cursor": "no",
        "input_default_bindings": "no",
        "config": "yes",
        "config_dir": map_path_to_str(config_dir),
        "screenshot_directory": map_path_to_str(screenshot_directory),
        "audio_client_name": audio_client_name,
        "ytdl": "yes",
    }

    if os.getenv("MPVQC_DEBUG") or os.getenv("MPVQC_PLAYER_LOG"):
        mpv_log_level = 25

        def player_logger(level: str, context: str, message: str) -> None:
            logger.log(mpv_log_level, message.rstrip(), extra={"mpv_level": level, "mpv_context": context})

        args["log_handler"] = player_logger

    return args
