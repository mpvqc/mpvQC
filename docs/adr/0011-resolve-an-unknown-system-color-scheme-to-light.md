# Resolve an unknown system color scheme to light

A color scheme preference that follows the system needs an answer for the case where the system gives none.
Under System, unknown renders light.

Light, because GNOME's settings only offer two of the three values: no preference and prefer-dark. Prefer-light is
reserved for future use, so a GNOME desktop set to light is one that reports no preference.
Windows and KDE Plasma never report unknown: Windows answers light when no app mode is set, and Plasma always answers.

## Consequences

- On GNOME, System follows both values the desktop offers, and follows them live.
- Dark is no longer a default the app defends. It renders when the user asked for it or the desktop did.
- A session with no settings portal comes up light and stays light, since unknown is the answer for as long as the
  session lasts.

## Dropped alternatives

- **Keep the historic dark** — it defends a default nobody picked against an answer the desktop actually gave, and
  leaves the app looking out of place on the desktop most of its users run. Being wrong on the value real desktops sit
  in is worse than being wrong on a value nobody selects.
- **Own a D-Bus client for `org.freedesktop.appearance`** — reading `color-scheme` ourselves would separate the two
  answers Qt hands over as one, and would reach the portal even where Qt's own theme never asks it. It changes no
  rendering this rule decides: no preference resolves light either way, and where no portal runs there is still nothing
  to read. It costs a subscription and a fallback path to maintain, forever, for an answer we already have.
