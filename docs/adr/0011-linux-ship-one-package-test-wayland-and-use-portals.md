# Ship one Linux package, test Wayland, and read desktop preferences through portals

The project ships one Linux packaging format through one store at a time. Today that format is Flatpak, shipped through
the project's Flatpak remote. It reaches every Linux distribution, which is the whole point of packaging this way.
**We don't accept contributions that add another Linux packaging format (deb, rpm, AppImage, snap), and we won't
link to a third-party build of them either.**

Wayland is the only display protocol the project runs and tests: nobody on the project uses X11, so nobody can build
or verify a fix for it there, and major desktops are moving off it anyway. For the same reason, the window-placement
correction ADR 0003 makes for Wayland stays Wayland-only, and the app runs on X11 uncorrected. Patches from the
community that improve X11 support, including that correction, are welcome, but since nobody on the project tests
against X11, a regression there can ship unnoticed from one release to the next.

Whenever the app needs a Linux desktop preference, it reads through the freedesktop portal rather than a desktop
environment's config files or libraries. Portals give every desktop one interface and are the boundary Flatpak permits.
Window-button layout is the first case: the app reads the de facto cross-desktop `button-layout` key through
`org.freedesktop.portal.Settings`. If the portal, interface, or key is unavailable, it silently uses a fixed default.
