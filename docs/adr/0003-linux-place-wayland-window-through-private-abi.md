# Place the Wayland window through Qt's private ABI

On Wayland the app draws its own window frame: rounded corners, a drop shadow, a resize band along the content edge.
The shadow needs transparent padding around the content, and the compositor treats that padded rectangle as the window.
Uncorrected, the visible content cannot sit flush against a screen edge, and snapping and maximizing act on the padding
instead of on what the user sees. Dropping the padding fixes the placement and costs the shadow and the rounded corners,
because there is nowhere left to paint them.

Qt has the correction. `QWaylandWindow::setCustomMargins` takes the inset from the padded rectangle to the visible one.
It takes it in native surface units, while the app computes the inset in Qt logical pixels;
`QHighDpiScaling::scaleAndOrigin` supplies the factor between the two, the layer the env scale factors set and
compositor scaling never enters. No public API reaches either: `QWindow` has no geometry inset, and the PySide6 wheel
ships `libQt6WaylandClient` with no bindings for it. So the Linux window-geometry code opens the bundled Qt GUI and
Wayland client libraries with ctypes, resolves three mangled C++ symbols, and calls the setter with the scaled inset.
`QWindow::handle()` returns a `QPlatformWindow*`, which is not the pointer the setter expects: a `QWaylandWindow`
carries a `QObject` base ahead of its `QPlatformWindow` base, so the code subtracts `sizeof(QObject)`, two pointers on
any build. That is as far as the claim goes: the code declares the visible rectangle through Qt's private margin API.

## Consequences

- The frameless window flags, the drop shadow margin the Linux desktop backend picks, the input mask and the resize
  band all assume the declaration happens. Remove the ctypes call and they stay, but the window is placed by its
  padding.
- The three mangled names are generated, never written. `just update-python-dependencies` runs the symbol updater, which
  demangles the bundled libraries and rewrites the constants. Hand-editing them defeats the check. When nothing in a
  library demangles to the wanted signature the updater stops with an error: that is the signal that the private API
  moved and the code needs a look.
- Failure is quiet by design. Symbols resolve once; if they don't, one warning goes to the log and the call is skipped.
  The app runs, with the placement problem back.
- Windows reaches the same Qt idea from the other side, through the undocumented `_q_windowsCustomMargins` property and
  no ctypes, with the sign reversed: a negative top margin that pushes the client area out over the caption strip. See
  ADR 0004.
- Delete this when PySide6 exposes a public window-geometry inset on `QWindow` or ships QtWaylandClient bindings. The
  margin call then becomes the public one and the ctypes goes, the factor conversion with it, since a public `QWindow`
  API would take logical pixels; nothing else in the Linux shell changes.
