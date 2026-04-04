# SPDX-FileCopyrightText: zhiyiYo
# SPDX-FileCopyrightText: Virace
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Inspired and based on:
#  - https://github.com/zhiyiYo/PyQt-Frameless-Window
#  - https://gitee.com/Virace/pyside6-qml-frameless-window/tree/main

from .event import WindowsEventFilter as WindowsEventFilter
from .utils import configure_gwl_style as configure_gwl_style
from .utils import extend_frame_into_client_area as extend_frame_into_client_area
from .utils import set_outer_window_size as set_outer_window_size
