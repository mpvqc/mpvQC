# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from functools import cached_property

try:
    # noinspection PyUnusedImports
    from PySide6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage

    QTDBUS_AVAILABLE = True
except ImportError:
    QTDBUS_AVAILABLE = False


logger = logging.getLogger(__name__)


class SettingsPortal:
    """Context manager for reading from org.freedesktop.portal.Settings
    (https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html) via D-Bus."""

    def __init__(self):
        self._connection_name = f"mpvqc-portal-{id(self)}"
        self._connection: QDBusConnection | None = None
        self._interface: QDBusInterface | None = None

    def __enter__(self):
        if not QTDBUS_AVAILABLE:
            logger.debug("QtDBus not available, cannot read portal settings")
            return self

        self._connection = QDBusConnection.connectToBus(QDBusConnection.BusType.SessionBus, self._connection_name)

        if not self._connection.isConnected():
            logger.warning("D-Bus session bus is not connected")
            return self

        self._interface = QDBusInterface(
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Settings",
            self._connection,
        )

        if not self._interface.isValid():  # type: ignore[union-attr]
            logger.debug("D-Bus settings portal interface is not valid")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection is not None:
            QDBusConnection.disconnectFromBus(self._connection_name)
        return False

    @cached_property
    def _portal_version(self) -> int:
        """Get the version of the Settings portal (e.g., 1 or 2), or 0 if unable to determine

        https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html#org-freedesktop-portal-settings-version
        """

        if self._interface is None or not self._interface.isValid():
            return 0

        try:
            version = self._interface.property("version")
            if version is not None:
                return int(version)
        except Exception:
            logger.debug("Could not determine Settings portal version")

        return 0

    def read_one(self, namespace: str, key: str) -> str | None:
        """Read a single setting from the portal. Wraps
        https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html#org-freedesktop-portal-settings-readone

        Args:
            namespace: The settings namespace (e.g., "org.gnome.desktop.wm.preferences")
            key: The setting key (e.g., "button-layout")

        Returns:
            The setting value, or None if unavailable or on error
        """

        if self._interface is None or not self._interface.isValid():
            return None

        portal_version = self._portal_version
        if portal_version == 0:
            return None

        try:
            # ReadOne() is preferred for version 2+
            if portal_version >= 2:  # noqa: PLR2004
                method_name = "ReadOne"
            else:
                method_name = "Read"
                logger.debug("Using deprecated Read() method (portal version: %s)", portal_version)

            reply = self._interface.call(method_name, namespace, key)

            if reply.type() == QDBusMessage.MessageType.ErrorMessage:
                logger.debug("D-Bus error reading %s %s: %s", namespace, key, reply.errorMessage())
                return None

            dbus_variant = reply.arguments()[0]

            if portal_version >= 2:  # noqa: SIM108,PLR2004
                value = dbus_variant.variant()
            else:
                value = dbus_variant.variant().variant()

            if value is None:
                logger.debug("Portal setting %s %s returned None", namespace, key)
                return None

            return str(value)
        except Exception:
            logger.exception("Exception reading portal setting %s %s", namespace, key)
            return None
