# Releasing

Paste this file into a `Release VERSION` issue on <https://github.com/mpvqc/mpvQC/issues> and tick the boxes there.
The manual checks below are the durable ones: what the OS, the compositor or the package does with the app. They
don't change from release to release. Checks for what changed since the last release go into the same issue, written
per release with the `manual-checks` skill.

## Pre-release

### Update metadata, dependencies, config, and translations

- [ ] Version in pyproject.toml updated
- [ ] Development status in pyproject.toml updated:
  - For beta: `"Development Status :: 4 - Beta"`
  - For stable: `"Development Status :: 5 - Production/Stable"`
- [ ] Old version strings found and replaced: `X.Y.Z`
- [ ] Python dependencies updated: `just update-python-dependencies`
- [ ] Pre-commit hooks updated: `just update-git-hook-dependencies`
- [ ] libmpv in CI updated: `.github/actions/install-libmpv/action.yml`
  - Visit <https://github.com/shinchiro/mpv-winbuild-cmake/releases>
  - Find the latest `mpv-dev-x86_64-*-git-*.7z` asset
  - Copy URL and SHA256 hash
  - Update the `default` values of the action's `url` and `sha256` inputs
- [ ] mpv.conf for Linux reviewed against the mpv version the Flatpak manifest builds: `data/config/mpv-linux.conf`
- [ ] mpv.conf for Windows reviewed against the libmpv build above: `data/config/mpv-windows.conf`
- [ ] input.conf reviewed: `data/config/input.conf`
- [ ] Translation catalogs regenerated: `just update-translations`
- [ ] Unfinished translations counted and accepted: `rg -c 'type="unfinished"' i18n/*.ts`

Run the formatter before committing.

### Update documentation, visuals, and release notes

- [ ] Splash updated: `build-aux/windows-splash.svg`, then `just generate-splash-png` in `build-aux/`
- [ ] README.md updated
- [ ] NOTICE.txt verified:
  - [ ] All dependencies match `pyproject.toml`
  - [ ] License identifiers match each package's actual metadata, not the project's umbrella license
  - [ ] The Windows and Flatpak build sources are still named correctly
  - [ ] `REUSE.toml` aggregate and `LICENSES/` texts are in sync: `uvx reuse lint`
- [ ] Screenshots checked, retaken in both color schemes if the UI changed: README, website, Flatpak
- [ ] Release notes drafted

### Verify build

- [ ] CI verified green for the commit under test: <https://github.com/mpvqc/mpvQC/actions>
- [ ] Windows zip of that run downloaded: `mpvQC-{tag}-{commit}-win-x86_64.zip`. Untagged builds report
      `unofficial`. That is expected here
- [ ] Flatpak built locally from the checkout, on the runtime the manifest names, with `MPVQC_BUILD_CHANNEL` unset
      (see the [mpvQC-flatpak](https://github.com/mpvqc/mpvQC-flatpak) manifest, `type: dir` source)

### Manual testing

Write every item as `Do: … → Expect: …`. Prefix them per platform (`W`, `D`, `T`) and number them in the ticket so you
can name a failure. Keep the same order on every platform. Windows runs on the zip. Linux runs on the local Flatpak
only, on one floating desktop and one tiling compositor, both named at the top of the list. Linux tests target Wayland
(ADR 0011).

#### 🪟 Windows

##### Packaging

- [ ] W Do: double-click `mpvQC.exe`, once cold, once warm → Expect: splash shows and vanishes exactly when the main
      window appears
- [ ] W Do: `mpvQC.exe --version` in a terminal → Expect: one line `mpvQC {version} ({commit}) {origin}`, no window
- [ ] W Do: Help → About mpvQC… → Expect: version line matches `--version`; `Powered by Python` names the version the
      pipeline ships
- [ ] W Do: keep `portable` next to the exe, start → Expect: `appdata/` beside the exe. Rename `portable` away,
      start → Expect: data under `%APPDATA%\mpvQC`
- [ ] W Do: open Help → Expect: Check for Updates… is present in the zip and absent in a dev run without `MPVQC_DEBUG`
- [ ] W Do: start on a dark scheme → Expect: no white flash before the first frame
- [ ] W Do: load a video, close the app, ten times → Expect: no Windows Error Reporting dialog, nothing in Event
      Viewer
- [ ] W Do: open `logs/mpvQC.log` → Expect: one `Startup took N ms` line

##### Window controls

- [ ] W Do: click close, minimize, maximize → Expect: each does its job
- [ ] W Do: double-click the title bar twice → Expect: maximizes, then restores
- [ ] W Do: Win+Up, then drag the window down → Expect: maximize icon flips with each state
- [ ] W Do: load a video → Expect: window resizes to video + table with no extra border
- [ ] W Do: enter fullscreen from normal and from maximized, leave with Esc and with the fullscreen key → Expect: header
      and footer hide; window returns to the exact state it left from

##### Frame, resize, DPI

- [ ] W Do: look at the window edge → Expect: Windows draws border, shadow and rounded corners; the accent line sits
      on the first row of the title bar like a native window
- [ ] W Do: resize from left, right, bottom and the bottom corners → Expect: native cursor, band outside the content
- [ ] W Do: resize from the top edge and top corners → Expect: works from inside the title strip, diagonal cursor at
      corners
- [ ] W Do: maximize, hover the top pixel row → Expect: no resize cursor; content fills the work area
- [ ] W Do: drag the edge of a menu, a dialog and a message box; open the same menu twenty times and try again →
      Expect: none resizes
- [ ] W Do: change display scale (100 % → 150 %) without signing out, relaunch → Expect: title strip matches the
      caption height, no gap, no doubled strip
- [ ] W Do: drag across two monitors with different scales → Expect: title bar usable, buttons aligned. Note: the app
      measures the caption inset once, from the primary monitor (ADR 0004)

##### Reveal and flicker

- [ ] W Do: open and close every dialog and message box on a dark scheme, normal and maximized → Expect: no white
      flash on open or close
- [ ] W Do: open the row context menu twenty times → Expect: no white flash, no late flash of an emptied popup
- [ ] W Do: minimize → Expect: native minimize animation plays; the player does not animate separately
- [ ] W Do: maximize, minimize, restore from the taskbar → Expect: comes back maximized; video not offset

##### Fullscreen, snapping, monitors

- [ ] W Do: fullscreen from maximized → Expect: instant, no restore animation
- [ ] W Do: leave fullscreen to normal, then maximize and restore → Expect: native animations still play
- [ ] W Do: fullscreen with auto-hide taskbar on, then off → Expect: taskbar hidden both times
- [ ] W Do: Win+D while fullscreen, restore → Expect: back in fullscreen
- [ ] W Do: Win+Up while fullscreen → Expect: maximized with title bar; maximize button restores; fullscreen key works
      again
- [ ] W Do: Win+Left while fullscreen → Expect: snapped to half, title bar, corners and border back
- [ ] W Do: Win+Shift+Right while fullscreen (two monitors) → Expect: fullscreen ends, window on the other monitor
      with its frame
- [ ] W Do: Win+Shift+Right with a maximized window to a monitor with a different resolution → Expect: content fills
      that work area
- [ ] W Do: fullscreen on the secondary monitor → Expect: covers exactly that monitor
- [ ] W Do: set the taskbar to auto-hide, maximize, move the mouse to the taskbar edge → Expect: taskbar reveals
- [ ] W Do: drag to the top, drag to a side → Expect: maximizes, snaps; maximize icon reflects the result. Note: the
      app's own maximize button does not open Snap Layouts

##### Color scheme

- [ ] W Do: with preference System, switch Settings → Personalization → Colors app mode → Expect: app retints live
- [ ] W Do: open Options → Appearance…, pick an accent → Expect: main window and the dialog retint together
- [ ] W Do: pick an explicit Light or Dark, switch the Windows app mode again → Expect: app stays as picked
- [ ] W Do: with explicit Dark while Windows is light → Expect: OS border, shadow and corners still look right

##### Popups

- [ ] W Do: open the File menu and the About dialog next to main-window text → Expect: same font, not Segoe UI
- [ ] W Do: switch the language to Hebrew, open a dialog and a message box → Expect: contents, header and footer
      buttons mirror
- [ ] W Do: open a dialog, click the main window → Expect: nothing happens; Escape closes the dialog
- [ ] W Do: right-click a row near the right and bottom edge → Expect: menu flips inward, fully on screen

##### Video and files

- [ ] W Do: load a video → Expect: plays, fills the pane, resizes with the split handle
- [ ] W Do: focus another app, click the video → Expect: first click activates the window and toggles pause
- [ ] W Do: on a German layout, AltGr+Q with the video focused → Expect: no ctrl+alt binding fires
- [ ] W Do: File → Save QC Document As… → Expect: native dialog, proposed name pre-filled, `json` filter selected,
      file written where chosen
- [ ] W Do: click through every menu → Expect: every entry opens what it names

#### 🐧 Linux desktop

Name the desktop at the top of the list. Run every 🪟 item that is not about the Windows frame, DPI, taskbar or
Segoe UI here too, then these.

##### Packaging

- [ ] D Do: build, install and run the Flatpak locally → Expect: starts (a missing `project.rcc` aborts with
      `FileNotFoundError`)
- [ ] D Do: `flatpak run io.github.mpvqc.mpvQC --version` → Expect: `unofficial` for the local build; About agrees
- [ ] D Do: Help → About mpvQC… → Expect: `Powered by Python` names the runtime's version; Help has no Check for
      Updates…
- [ ] D Do: Help → Open App Data Folder… → Expect: `~/.var/app/io.github.mpvqc.mpvQC/config/mpvQC` opens through the
      portal
- [ ] D Do: File → Save QC Document As… → Expect: portal dialog, proposed name pre-filled, file lands where chosen
- [ ] D Do: click a link in About → Expect: host browser opens
- [ ] D Do: open a menu, a dialog and Options → Edit mpv.conf… → Expect: app font in popups, monospace in the editor
- [ ] D Do: open `logs/mpvQC.log` → Expect: `Using Linux desktop platform backend`, no Wayland symbol warning
- [ ] D Do: quit while a video plays → Expect: clean exit, no mpv or GL error in the log

##### Drop shadow and corners

- [ ] D Do: focus and unfocus the window → Expect: soft shadow on focus, nearly gone unfocused
- [ ] D Do: click a few pixels outside the resize edge → Expect: click reaches the window behind
- [ ] D Do: look at the corners → Expect: top corners and bottom-right rounded; video corner may stay square in the
      horizontal layout
- [ ] D Do: hover the menu bar ends, the close button and the footer ends → Expect: highlights stay inside the corners
- [ ] D Do: maximize, then fullscreen, then restore → Expect: square corners, no shadow, no margin while maximized or
      fullscreen; all three return on restore
- [ ] D Do: shrink to the minimum size → Expect: table never paints into the transparent margin
- [ ] D Do: load a video → Expect: video clips to the rounded corner; shadow stays outside
- [ ] D Do: open a dialog → Expect: stays inside the border; margin stays transparent
- [ ] D Do: right-click a row near the bottom-right corner → Expect: menu stays inside the frame

##### Maximize, fullscreen, restore

- [ ] D Do: maximize and restore via title-bar button, double-click, Super+Up/Down, drag to top, drag the maximized
      window down → Expect: lands in the expected state each time, no frame with content offset by the margin.
      Note: the compositor's animation scales a snapshot that still holds the shadow band; a brief squeeze is expected
- [ ] D Do: maximize, minimize with the title-bar button, restore from the overview → Expect: back maximized, square
      corners, no shadow
- [ ] D Do: fullscreen from maximized, leave → Expect: back to maximized, not normal

##### Placement and resize

- [ ] D Do: drag to the top edge; resize from every edge and corner → Expect: all work
- [ ] D Do: drag against the left and right screen edges; Super+Left/Right → Expect: visible border sits flush, not
      the margin
- [ ] D Do: launch with `QT_SCALE_FACTOR=1.5`, snap and maximize → Expect: aligned to the visible border
- [ ] D Do: drag across two monitors with different scale factors → Expect: border aligned, resize band at the visible
      edge on both

##### Window buttons and color scheme

- [ ] D Do: on GNOME `gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:close'`, relaunch →
      Expect: only the close button; default layout: all three
- [ ] D Do: with preference System, flip the desktop: GNOME
      `gsettings set org.gnome.desktop.interface color-scheme prefer-dark`, KDE `plasma-apply-colorscheme BreezeDark`
      (`prefer-light`, `BreezeLight` flip back) → Expect: app retints live
- [ ] D Do: set Light accent red and Dark accent green, choose System, flip → Expect: accent follows the scheme
- [ ] D Do: flip while Options → Appearance… is open under System → Expect: nothing moves in the dialog; app retints
- [ ] D Do: on GNOME `gsettings set org.gnome.desktop.interface color-scheme default` → Expect: renders light
- [ ] D Do: choose Light, then System → Expect: follows the desktop again without a restart
- [ ] D Do: choose an explicit Light or Dark, flip the desktop → Expect: app stays as picked. Run this one last

##### Hardware decoding

- [ ] D Do: load a video, press `i` → Expect: stats report a hwdec method for a codec the GPU supports. Note: UI
      animations paint no faster than the video frame rate while a video plays (ADR 0010)

#### 🧱 Linux tiling

Name the compositor at the top of the list. Run the same shared items as on the desktop, then these.

- [ ] T Do: look at the window → Expect: flush, no transparent margin, no shadow, square corners
- [ ] T Do: open `logs/mpvQC.log` → Expect: `Using Linux tiling desktop platform backend`
- [ ] T Do: load a video → Expect: window neither resizes nor floats
- [ ] T Do: fullscreen via key and via double-click on the player, then leave → Expect: fills the output, returns to
      the tile
- [ ] T Do: hover the 8 px band inside the window edge → Expect: no resize cursor
- [ ] T Do: resize the tile → Expect: video follows, no stale frame at the edges
- [ ] T Do: make the tile narrower than ~420 px, open Options → Comment Types…, Export Settings…, Import Settings… →
      Expect: dialogs shrink to the tile width; other dialogs usable
- [ ] T Do: open a dialog, resize the tile → Expect: dialog stays inside
- [ ] T Do: delete a 30-line comment in a small tile → Expect: confirmation fits with a scroll bar, buttons reachable
- [ ] T Do: open each header menu and the footer dropdown → Expect: nothing bleeds outside the window
- [ ] T Do: on a session without a settings portal → Expect: System renders light; Dark can still be chosen

## Release

### Tag and CI build

- [ ] Create annotated tag: `git tag -a VERSION -m "Release VERSION"`
- [ ] Push tag to trigger CI: `git push origin VERSION`

The rest comes from the Actions run for that tag, at <https://github.com/mpvqc/mpvQC/actions>:

- [ ] Download `mpvQC-VERSION-{commit}-win-x86_64.zip`
- [ ] Tagged Windows build reports `mpvqc-github` in `--version` and in Help → About mpvQC…
- [ ] Tagged Windows build shows the new splash
- [ ] Download `release-build-windows.zip`
- [ ] Download the complete build log and attach it to the `Release VERSION` issue on
      <https://github.com/mpvqc/mpvQC/issues>

### GitHub release

- [ ] Draft new release on GitHub
- [ ] Upload both artifacts
- [ ] Publish release

## Post-release

### Flatpak distribution

These steps apply to the [mpvQC-flatpak](https://github.com/mpvqc/mpvQC-flatpak) repository.

- [ ] In the manifest, point the mpvQC source `tag` and `commit` at `VERSION`
- [ ] Update `io.github.mpvqc.mpvQC.metainfo.xml`:
  - [ ] Bump the top-level `version`
  - [ ] Add a `<release version="VERSION" date="YYYY-MM-DD">` entry with the changelog
  - [ ] Update screenshots if the UI changed
- [ ] Commit changes to the mpvQC-flatpak repository
- [ ] Run the `Build Flatpak` workflow manually from the Actions tab (it only triggers on workflow dispatch)
- [ ] Updated Flatpak reports `mpvqc-flatpak`: `flatpak run io.github.mpvqc.mpvQC --version`

When the build succeeds, the workflow commits the result to the flatpak repository.

### Website update

These steps apply to the [mpvqc.github.io](https://github.com/mpvqc/mpvqc.github.io) repository.

- [ ] Screenshots updated
- [ ] Version endpoint updated: `static/api/v1/public/version`
