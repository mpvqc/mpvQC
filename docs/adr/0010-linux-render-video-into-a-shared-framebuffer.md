# Render Linux video into a shared framebuffer instead of embedding natively

On Windows the player embeds mpv as a native child window. Wayland has no protocol for embedding a foreign window at
all, so Linux instead renders mpv through libmpv's render API: it draws video frames into the same framebuffer Qt
renders its own UI into, in-scene rather than as a separate window. X11 does support native embedding, but a second
path just for it isn't worth building: X11 gets no further investment either way (ADR 0011), so it takes the same
framebuffer path as Wayland instead of its own. The render context takes Qt's native display handle for the active
backend, `wl_display` on Wayland or the X11 `Display` under xcb, so mpv can reach hardware decode.

Sharing one framebuffer between the UI and the video ties Qt's paint rate to the video's: at 24 fps, menus and other
UI animations paint no faster than the video does. We built a second, offscreen framebuffer for mpv once, decoupled
from Qt's own paint cadence, to fix this, then reverted it. The current stopgap is tuning mpv's `video-timing-offset`
in the bundled `mpv-linux.conf`, trading a wider frame-delay tolerance for tighter sync with the monitor's actual
refresh rate — a workaround, not a fix.

## Consequences

- Revisit this when a superior alternative to rendering into a shared framebuffer exists.
