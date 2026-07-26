# Keep the native Windows frame and reclaim only the caption strip

The app draws its own title bar on Windows: window buttons, menu, drag area. The usual way to get one is a frameless
window, which is what the two projects this code descends from do. Frameless costs the native drop shadow, the borders,
the rounded corners, snap layouts and the DWM maximize and restore animations, and every non-client behavior has to be
rebuilt by hand to get them back.

So the window keeps its full native frame and gives up only the caption strip. Before the native window is created, the
frame integration sets Qt's undocumented `_q_windowsCustomMargins` property with a negative top margin: the caption
height plus the top resize border at the primary monitor's DPI. Qt extends the client area up over the caption, and the
title bar goes there. The left, right and bottom bands stay real non-client frame, so resizing there, the shadow, the
borders, the corners and the animations are all still Windows'.

This is the mirror of the Wayland decision in ADR 0003. Same Qt idea, custom margins on the window, opposite sign:
Windows pushes the client area outward over the caption, Wayland pulls the declared window inward from its padding.
Windows needs no private ABI for it, only an undocumented property name.

## Consequences

- A native event filter corrects Qt's frame in the two cases where the negative caption margin is wrong: maximized,
  where the correction overshoots the work area, and fullscreen. Every other message on the main window passes through
  to Qt untouched, which is the point of the whole approach.
- A fullscreen window is deliberately larger than the monitor. DWM stops animating maximize and restore for good once a
  client rect fills the whole window, and the animations are what the native frame is being kept for.
- Only the top edge needs a hit test, because the client area covers the strip where the caption and its resize band
  would sit. The other three edges are hit-tested natively.
- Flags and margins are read once, when the native window is created, so the property has to be set before that and the
  code forces creation right after. Qt then updates its own frame bookkeeping only on a geometry event, so the first
  scene would keep the stale margins; a one-pixel resize and back settles it.
- The caption inset is measured once, from the primary monitor, at startup. Moving the window to a monitor with a
  different DPI does not remeasure it.
