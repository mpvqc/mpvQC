# Ship Linux through a single channel, and treat Wayland as the only tested display

The project distributes itself on Linux through exactly one channel at a time. Today that channel is
Flatpak, it reaches every Linux distribution, which is the whole point of packaging this way.
**We don't accept contributions that add another Linux packaging format (deb, rpm, AppImage, snap), and we won't
link to a third-party build of them either.**

Wayland is the only display protocol the project runs and tests: nobody on the project uses X11, so nobody can build
or verify a fix for it there, and major desktops are moving off it anyway. For the same reason, the window-placement
correction ADR 0003 makes for Wayland stays Wayland-only, and the app runs on X11 uncorrected. Patches from the
community that improve X11 support, including that correction, are welcome, but since nobody on the project tests
against X11, a regression there can ship unnoticed from one release to the next.
