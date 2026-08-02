# Resolve an unknown system color scheme to light

Under System, an unknown system color scheme resolved to dark, because dark was mpvQC's historic default. That left the
app as the one dark window on a light GNOME desktop. GNOME set to `default` is not a desktop with no opinion; it is a
desktop saying light, in the only spelling GNOME has for it. The settings portal's `color-scheme` carries `0` no
preference, `1` prefer-dark and `2` prefer-light, and a GNOME desktop nobody has touched sits at `0`. libadwaita
renders `0` as light, which is why every GTK window around ours was light while ours was dark.

Under System, unknown renders light.

Qt hands both cases over as the same value. `Qt::ColorScheme` has no third state, so *the desktop said no preference*
and *nobody answered* arrive identically, and nothing downstream can tell them apart. That is what makes this one rule
rather than two.

Only two situations produce unknown at all: a GNOME-like desktop set to `default`, and a session with no settings
portal. KDE Plasma never answers unknown, because its portal derives light or dark from the active color scheme's own
colors. Windows never does either, since an unset app mode reads as light already. So the rule turns the first
situation from wrong to right, and puts the second where Windows has been all along — an absent setting means light on
both platforms.

## Consequences

- On GNOME-like desktops, System follows all three values the desktop offers, `default` included, and follows them
  live.
- Dark is no longer a default the app defends. It renders when the user asked for it or the desktop did, and not
  otherwise.
- A flip from dark to `default` is a real change now rather than one the app dedupes away, so the retint reaches the
  window.
- A session with no settings portal comes up light and stays light through every flip, because Qt reports unknown
  there forever: outside a sandbox on a desktop Qt has no theme for, it falls back to its generic theme, which never
  asks the portal. That is running from source on a tiling desktop. The shipped Linux artifact is the Flatpak, where
  Qt puts its `xdgdesktopportal` theme first and reads the portal properly.

## Dropped alternatives

- **Keep the historic dark** — it defends a default nobody picked against an answer the desktop actually gave, and
  leaves the app looking out of place on the desktop most of its users run. Being wrong on the value real desktops sit
  in is worse than being wrong on a value nobody selects.
- **Own a D-Bus client for `org.freedesktop.appearance`** — reading `color-scheme` ourselves would separate the two
  answers Qt hands over as one, and would fix the unsandboxed session above. It costs a subscription and a fallback
  path to maintain, for a way of running the app we do not ship.
