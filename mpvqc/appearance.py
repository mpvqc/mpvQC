# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import NewType

ThemeIdentifier = NewType("ThemeIdentifier", str)
AccentColor = NewType("AccentColor", str)


@dataclass(frozen=True)
class ThemeAppearance:
    theme_identifier: ThemeIdentifier
    stored_accent: AccentColor | None


@dataclass(frozen=True)
class Palette:
    accent_color: AccentColor
    background: str
    foreground: str
    hint: str
    accent: str
    separator: str
    error: str
    error_text: str
    header_background: str
    popup_background: str
    popup_text: str
    menu_background: str
    dialog_background: str
    tooltip_background: str
    tooltip_text: str
    row_base: str
    row_base_text: str
    row_stripe: str
    row_stripe_text: str
    row_selected: str
    row_selected_text: str
