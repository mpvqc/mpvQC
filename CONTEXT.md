# Domain glossary

Terms the code uses. Keep entries short. Add a term when you name a module after a concept that is not listed here.

## Import pipeline

- **Concern**: one dimension of an import that may need user input (`errors`, `session`, `video`, `subtitles`). Each is
  a tagged union with resolved variants (such as `Merge`, `Load`, `Skip`) and an `Unresolved` variant carrying the data
  a user needs to decide.
- **Resolve**: turn a Concern into one of its resolved variants, either from settings and scan results (`make_plan`) or
  from wizard input (`build_finished_plan`).
- **UnfinishedPlan**: scan output with at least one Concern unresolved or errors present. Presented to the user as the
  import wizard.
- **FinishedPlan**: every Concern resolved. The only input `ImporterService.execute()` accepts.
- **Wizard step**: one page of the import wizard, one per unresolved Concern, in canonical order: errors, session,
  video, subtitles.
- **Close-only mode**: wizard state when errors are the only step and nothing importable remains. The user can only
  close the wizard. `WizardDialogPolicy` decides this once for both title and footer.

## UI

4- **Overlay**: a dialog, file dialog, or message box that floats above the app, is loaded on demand, and returns focus
  on close. Behavior defines it, not rendering. In windowed-popup mode some overlays are real OS windows and still
  count.

## Platform

- **Window manager**: on X11, a separate client that places and sizes windows. Wayland has no such separate process.
- **Compositor**: the process that composites the screen. On Wayland it also places and sizes windows, so it absorbs
  the window manager role. On Windows, DWM composites but does not place or size.
- **Tiling desktop**: a session where the compositor or window manager places and sizes windows for the user, so the
  app must not resize itself. The name says neither compositor nor window manager because both kinds tile.
- **Window geometry**: the visible bounds of the window, what the compositor aligns, snaps and constrains against. Drop
  shadows sit outside it.
- **Decorations**: the border, title bar, shadow and resize band around the app content. Either the OS draws them or
  the app does. Wayland names the two modes server-side and client-side. mpvQC draws all of them itself on Linux, on
  X11 and Wayland alike. Its border is a rounded rectangle filling the window geometry. On Windows the OS keeps the
  border, the shadow and the rounded corners. The app draws the title bar into the caption strip it reclaims.
- **Surface**: the whole rectangle the client paints into. When the client draws its own decorations, it extends past
  the visible window by the shadow margin. Otherwise, the two are the same rectangle.
- **Shadow margin**: how far the surface extends past the window geometry, painted with the drop shadow and holding the
  resize band. Zero when maximized, fullscreen, on a tiling desktop, and on Windows.

**Linux desktop**, where the app draws its own decorations:

```text
┌───────────────────────────────────────┐  surface
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░╭─────────────────────────────────╮░░│  the border the app draws,
│░░│                                 │░░│  with rounded corners
│░░│           app content           │░░│
│░░│                                 │░░│  its edge is the window geometry
│░░╰─────────────────────────────────╯░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└───────────────────────────────────────┘

░ = shadow margin: transparent, carries the drop shadow and the resize band
```

**Windows**, and any Linux tiling desktop, where the app draws no border of its own:

```text
┌───────────────────────────────────────┐  surface and window geometry, one
│                                       │  rectangle: shadow margin 0, corner
│                                       │  radius 0, no border of the app's own
│              app content              │
│                                       │  on Windows the OS draws the border,
│                                       │  the shadow and the rounded corners
└───────────────────────────────────────┘
```

## Build origin

- **Channel**: the store a build ships through, stamped into build-info at build time. `mpvqc-github` and
  `mpvqc-flatpak` are the project's channels. Packagers may stamp their own. Empty in git and in every unstamped
  build, which reports `unofficial`. A channel names a store, never a packaging format. "flatpak" is not a channel.
  Flathub would be a different one.
- **Build origin**: whether this binary came from a project release pipeline: the declared channel name, or
  `unofficial` when no channel was declared. The pipeline declares it. Runtime never infers it. The Flatpak app ID can
  veto a declared channel but never grant one.
