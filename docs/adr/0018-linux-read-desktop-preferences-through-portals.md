# Read Linux desktop preferences through XDG portals

Whenever a Linux desktop preference is needed, it's read through the freedesktop portal that exposes it, rather
than through a desktop environment's own config files or libraries. Window-button layout is the first case. Portals
work the same way across desktops without per-desktop-environment code, and are the interface Linux desktops are
converging on; that it's also the interface Flatpak's sandbox allows (ADR 0017) is a secondary benefit.

Button layout is read from `org.gnome.desktop.wm.preferences`'s `button-layout` key, a GNOME-authored setting that
has become the de facto cross-desktop convention for this data, through the generic `org.freedesktop.portal.Settings`
interface. When the portal, the interface, or the key can't be resolved, the app silently falls back to a fixed default.
