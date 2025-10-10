# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import platform
from dataclasses import dataclass
from typing import Protocol

from loguru import logger

try:
    from PySide6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage

    QTDBUS_AVAILABLE = True
except ImportError:
    QTDBUS_AVAILABLE = False


@dataclass
class ButtonPreferences:
    minimize: bool = True
    maximize: bool = True
    close: bool = True


DEFAULT_BUTTON_PREFERENCES = ButtonPreferences()


class DesktopEnvironmentDetector(Protocol):
    def detect(self) -> ButtonPreferences:
        """Detect button preferences for this desktop environment."""
        ...


class DefaultDetector:
    """Default detector that shows all buttons."""

    def detect(self) -> ButtonPreferences:
        return DEFAULT_BUTTON_PREFERENCES


class GnomeDetector:
    def detect(self) -> ButtonPreferences:
        layout = read_portal_setting("org.gnome.desktop.wm.preferences", "button-layout")

        if layout is None:
            return DEFAULT_BUTTON_PREFERENCES

        return self.parse_button_layout(layout)

    @staticmethod
    def parse_button_layout(layout: str) -> ButtonPreferences:
        buttons = layout.replace(":", ",").lower()
        return ButtonPreferences(
            minimize="minimize" in buttons,
            maximize="maximize" in buttons,
            close="close" in buttons,
        )


class WindowButtonsService:
    """Service for detecting which window control buttons should be displayed."""

    def detect(self) -> ButtonPreferences:
        return self._create_detector().detect()

    @staticmethod
    def _create_detector() -> DesktopEnvironmentDetector:
        if platform.system() != "Linux":
            return DefaultDetector()

        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

        match desktop:
            case d if "gnome" in d:
                return GnomeDetector()
            case _:
                return DefaultDetector()

    @staticmethod
    def defaults() -> ButtonPreferences:
        return DEFAULT_BUTTON_PREFERENCES


def read_portal_setting(namespace: str, key: str) -> str | None:
    """Read a setting from the XDG Settings Portal via D-Bus."""
    if not QTDBUS_AVAILABLE:
        logger.debug("QtDBus not available, cannot read portal settings")
        return None

    try:
        connection = QDBusConnection.sessionBus()
        if not connection.isConnected():
            logger.warning("D-Bus session bus is not connected")
            return None

        interface = QDBusInterface(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Settings",
            connection,
        )

        if not interface.isValid():
            logger.debug("D-Bus settings portal interface is not valid")
            return None

        reply = interface.call("Read", namespace, key)

        if reply.type() == QDBusMessage.MessageType.ErrorMessage:
            logger.debug("D-Bus error reading {}.{}: {}", namespace, key, reply.errorMessage())
            return None

        dbus_variant = reply.arguments()[0]
        value = dbus_variant.variant().variant()

        if value is None:
            logger.debug("Portal setting {}.{} returned None", namespace, key)
            return None

        return value
    except Exception:
        logger.exception("Exception reading portal setting {}.{}: {}", namespace, key)
        return None
