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

- **Overlay**: a dialog, file dialog, or message box: a transient surface that floats above the app, is loaded on
  demand, and returns focus on close. Defined by behavior, not rendering; in windowed-popup mode some overlays are
  real OS windows and still count.

## Platform

- **Surface**: the whole rectangle the client paints into. When the client draws its own decorations it extends past
  the visible window by the shadow margin; otherwise the two are the same rectangle.
- **Window geometry**: the visible bounds of the window, what the compositor aligns, snaps and constrains against. The
  client declares it; drop shadows sit outside it.
- **Shadow margin**: how far the surface extends past the window geometry, painted with the drop shadow and holding the
  resize band. GTK calls the same quantity shadow width. Zero when maximized, fullscreen, on a tiling desktop, and on
  Windows.
- **Compositor**: the process that composites the screen. On Wayland it also places and sizes windows, so it absorbs
  the window manager role. On Windows, DWM composites but does not place or size; the system does.
- **Window manager**: on X11, a separate client that places and sizes windows. Wayland has no such separate process.
- **Tiling desktop**: a session where the compositor or window manager places and sizes windows for the user, so the
  app must not resize itself. The name says neither compositor nor window manager because both kinds tile.

## Build origin

- **Channel**: the store a build ships through, stamped into build-info at build time. `mpvqc-github` and
  `mpvqc-flatpak` are the project's channels; packagers may stamp their own. Empty in git and in every unstamped
  build, which reports `unofficial`. A channel names a store, never a packaging format ("flatpak" is not a channel;
  Flathub would be a different channel).
- **Build origin**: whether this binary came from a project release pipeline: the declared channel name, or
  `unofficial` when no channel was declared. Declared by the pipeline, never inferred at runtime; the Flatpak app ID
  can veto a declared channel but never grant one.
