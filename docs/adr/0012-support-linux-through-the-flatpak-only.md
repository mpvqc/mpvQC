# Support Linux through the Flatpak only

The project builds, tests and designs against one Linux artifact: the Flatpak. Not because packaging elsewhere is
forbidden, but because the app leans on things the sandbox and the manifest guarantee together, and buying those back
for an unsandboxed build costs more than a second artifact is worth.

The color scheme is the clearest case. Inside a sandbox Qt finds the Flatpak marker and puts its portal platform theme
ahead of the desktop's own; that theme reads the desktop's color scheme and follows it live. Outside a sandbox, on a
desktop Qt carries no theme for — which is every tiling compositor — Qt falls back to its generic theme, which never
asks the portal at all. The app then cannot see the system color scheme, at startup or ever. The alternative is owning
a D-Bus portal client to buy back what the sandbox already provides, on a path we do not ship. We took the sandbox.

The sandbox alone turned out not to be enough, and it took a bug to find out. Qt's Flatpak pick is only what it reaches
for when nothing else asks for a theme: an explicit `QT_QPA_PLATFORMTHEME` in the launching environment beats it.
Launchers on tiling desktops commonly export `gtk3` so that Qt apps match GTK ones, and that theme reads the color
scheme once at startup and then never reports a change again. The app comes up correct and quietly stops following the
desktop, which reads as a stranger bug than never following it at all. So the manifest pins the theme instead of
trusting the fallback, and users who want a different one still have `flatpak override --env`. That is the second
reason the supported artifact is the Flatpak: the guarantee lives in the packaging, and a source checkout has nothing
pinning anything.

The bundled Qt is the other. The Wayland window placement resolves mangled C++ symbols out of the Qt libraries that
ship with the app, and the dependency updater regenerates those constants from those exact libraries (ADR 0003). A
build linked against a distribution's Qt is not the build those names were generated against.

## What this does not say

Rebuilds and repackages are legitimate and stay so. ADR 0002 already treats an honest rebuild as honest — it keeps the
upstream app ID, reports its channel as unofficial, and that is the whole consequence. Running from a source checkout
stays the normal way to develop. Neither is supported in the sense this ADR means: neither is what a release is
verified on, and neither constrains a design decision.

## Consequences

- **No portal client of our own.** A non-sandboxed build on a desktop Qt has no theme for never sees the system color
  scheme at all, so it reports unknown forever and renders light under System (ADR 0011) through every desktop flip.
  That is this decision showing through, not a bug against the color scheme code. The fix for a user hitting it is the
  Flatpak.
- **The manifest owns the platform theme.** Removing the pin hands the choice back to whatever launched the app, and on
  a tiling desktop that is usually a theme that cannot report changes.
- **Linux release verification happens on the locally built Flatpak.** The release checklist already says so. Window
  chrome and color scheme are both invisible to CI and both depend on what the sandbox and the manifest pin.
- **The private-ABI symbol constants track the bundled Qt**, and the updater that regenerates them assumes those
  libraries are the ones the app will load.
- **Reversing this means adding, not removing.** A portal client for the color scheme, symbol resolution that tolerates
  a system Qt, and a test matrix that covers both. Worth doing the day a second Linux artifact becomes a goal, and not
  before.
