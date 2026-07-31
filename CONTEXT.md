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

## Comments

- **Unknown comment type**: a type a comment carries that is not in the configured list. Imported documents introduce
  them; removing a configured type leaves them behind. They render and export verbatim, since they have no translation
  catalog entry.
- **Displayable comment types**: the types the comment table may show: every configured type plus every type present in
  the document. The table reserves label space for all of them. The new-comment menu (configured types only) and the
  edit-type menu (configured types plus the row's own type) show different sets by design.

## UI

- **Overlay**: a dialog, file dialog, or message box that floats above the app, is loaded on demand, and returns focus
  on close. Behavior defines it, not rendering: where the app prefers Qt's Window popup type, an overlay is a real OS
  window and still counts.
- **Overlay layer**: where an in-scene popup sits in the stack Qt's overlay keeps, picked through its `z`. Every popup
  is a sibling there, so the layer decides what covers what. Low to high: the inline editor, the search box, modal
  popups, tooltips.
- **Row popup**: a popup the user opened for one row: an editor, context menu or confirmation. The list holds still
  until it is dismissed. The search box is not one, no row opened it. Modal ones also take input away from everything
  beneath them, an inline editor does not.
- **Modal overlay**: anything that owns the window's input while open: a dialog, message box, modal menu, modal row
  popup, or native file dialog.
- **Long time format**: a time rendered with hours, `HH:MM:SS`; the short format is `MM:SS`. A surface uses the long
  format when any time it may display can reach one hour. Exported documents always use the long format.
- **Time display mode**: which time the footer shows: current, remaining, current over total, or none. Independent of
  the long and short time format, which only decides whether hours render.

## Platform

- **Window manager**: on X11, a separate client that places and sizes windows. Wayland has no such separate process.
- **Compositor**: the process that composites the screen. On Wayland it also places and sizes windows, so it absorbs
  the window manager role. On Windows, DWM composites but does not place or size.
- **Tiling desktop**: a session where the compositor or window manager places and sizes windows for the user, so app
  size requests might be ignored. The name says neither compositor nor window manager because both kinds tile.
- **Embedded player**: the player as a native child window of the app's own window, painted by the OS above the scene
  instead of into it. Only Windows does this. Everywhere else the player renders in-scene.
- **Window geometry**: the visible bounds of the window, what the compositor aligns, snaps and constrains against. Drop
  shadows sit outside it.
- **Decorations**: the border, title bar, drop shadow and resize band around the app content. The OS draws them, or the
  app does, or nobody does. Wayland names the first two server-side and client-side. mpvQC draws its own title bar
  everywhere. On Windows the OS keeps the border, the drop shadow and the rounded corners, and the app draws the title
  bar into the caption strip it reclaims. On a floating Linux desktop the app draws the rest too, on X11 and Wayland
  alike: a rounded border filling the window geometry, a drop shadow and a resize band. On a tiling desktop nobody
  draws them, because the compositor packs windows edge to edge and the app skips its border, shadow and resize band.
- **Caption strip**: on Windows, the band at the top of the window where the OS would draw the title bar, plus the
  resize border above it.
- **Surface**: the whole rectangle the client paints into. When the client draws its own decorations, it extends past
  the visible window by the drop shadow margin. Otherwise, the two are the same rectangle.
- **Drop shadow margin**: how far the surface extends past the window geometry, painted with the drop shadow and holding
  the resize band. Zero when maximized, fullscreen, on a tiling desktop, and on Windows. On Wayland the compositor draws
  no drop shadow for a frameless client, so an app that wants one has to paint it itself.

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

░ = drop shadow margin: transparent, carries the drop shadow and the resize band
```

**Windows**, and any Linux tiling desktop, where the app draws no border of its own:

```text
┌───────────────────────────────────────┐  surface and window geometry, one
│                                       │  rectangle: drop shadow margin 0,
│                                       │  corner radius 0, no border of its own
│              app content              │
│                                       │  on Windows the OS draws the border,
│                                       │  the drop shadow and the rounded corners
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
