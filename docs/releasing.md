# Releasing

## Pre-release

### Update metadata, dependencies, config, and translations

- [ ] Version in pyproject.toml updated
- [ ] Development status in pyproject.toml updated:
  - For beta: `"Development Status :: 4 - Beta"`
  - For stable: `"Development Status :: 5 - Production/Stable"`
- [ ] Old version strings searched and updated: `X.Y.Z`
- [ ] Python dependencies updated: `just update-python-dependencies`
- [ ] Pre-commit hooks updated: `just update-git-hook-dependencies`
- [ ] mpv.conf for Linux updated: `data/config/mpv-linux.conf`
- [ ] mpv.conf for Windows updated: `data/config/mpv-windows.conf`
- [ ] input.conf updated: `data/config/input.conf`
- [ ] Verify there are no new untranslated strings: `just update-translations`

Run the formatter before committing.

### Update documentation, visuals, and release notes

- [ ] Splash updated
- [ ] README.md updated
- [ ] NOTICE.txt verified:
  - [ ] All dependencies match `pyproject.toml`
  - [ ] License identifiers match each package's actual metadata, not the project's umbrella license
  - [ ] The Windows and Flatpak build sources are still named correctly
  - [ ] `REUSE.toml` aggregate and `LICENSES/` texts are in sync: `uvx reuse lint`
- [ ] New screenshots created (both light and dark color schemes) for Website and Flatpak
- [ ] Release notes drafted

### Verify build and manual testing

- [ ] libmpv in CI updated: `.github/actions/install-libmpv/action.yml`
  - Visit <https://github.com/shinchiro/mpv-winbuild-cmake/releases>
  - Find latest `mpv-dev-x86_64-*-git-*.7z` asset
  - Copy URL and SHA256 hash
  - Update the `default` values of the action's `url` and `sha256` inputs
- [ ] CI verified green: <https://github.com/mpvqc/mpvQC/actions>
- [ ] Manual testing on Windows (areas the test suite cannot exercise):
  - [ ] Video playback works
  - [ ] Basic export writes a real file via the native file dialog
  - [ ] Smoke-click each menu and the window chrome (close/minimize/maximize)
  - [ ] Minimize a maximized window with the title-bar button: it restores from the taskbar as maximized
  - [ ] Enter and exit fullscreen from both a normal and a maximized window: both transitions are clean
  - [ ] Press Win+D while fullscreen: restoring the window returns it to fullscreen
  - [ ] With the app running, switching the app mode under Settings → Personalization → Colors retints it live
  - [ ] An explicit Light or Dark under Options → Appearance... survives that switch untouched
- [ ] Manual testing on Linux, on a locally built Flatpak (see below):
  - [ ] Flatpak builds, installs and runs locally
  - [ ] Windows manual tests above also pass on Linux
  - [ ] Window chrome and color scheme verified on both setups

#### Window chrome and color scheme verification

The Linux window chrome is self-drawn and compositor-dependent, and the color scheme comes from the desktop's settings
portal. CI runs neither, so verify both on the locally built Flatpak, on both setups:

##### Desktop environment (e.g. GNOME, KDE Plasma)

- [ ] Drop shadow is drawn around the window and strengthens while it is focused
- [ ] Corners are rounded (top corners and bottom-right). The video corner may stay square in the horizontal layout
- [ ] Menu bar, close button and footer hover highlights stay within the rounded corners
- [ ] Maximize, fullscreen and back to normal land in the expected state (no flicker back to normal)
- [ ] Window drags to the top edge and resizes from every edge and corner
- [ ] With the app running, a desktop flip retints it live: on GNOME
      `gsettings set org.gnome.desktop.interface color-scheme prefer-dark`, on KDE Plasma
      `plasma-apply-colorscheme BreezeDark` (`prefer-light` and `BreezeLight` flip back)
- [ ] An explicit Light or Dark under Options → Appearance... survives that flip untouched
- [ ] On GNOME, `gsettings set org.gnome.desktop.interface color-scheme default` renders light

##### Tiling compositor (e.g. Sway, Hyprland, niri)

- [ ] Window sits flush with no transparent margin and no drop shadow
- [ ] Corners are square

## Release

### Tag and CI build

- [ ] Create annotated tag: `git tag -a VERSION -m "Release VERSION"`
- [ ] Push tag to trigger CI: `git push origin VERSION`

The rest comes off the Actions run for that tag, at <https://github.com/mpvqc/mpvQC/actions>:

- [ ] Download `mpvQC-VERSION-{commit}-win-x86_64.zip`
- [ ] Downloaded Windows build reports `mpvqc-github` (version line in Help → About mpvQC...)
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

- [ ] In the manifest point the mpvQC source `tag` and `commit` at `VERSION`
- [ ] Update `io.github.mpvqc.mpvQC.metainfo.xml`:
  - [ ] Bump the top-level `version`
  - [ ] Add a `<release version="VERSION" date="YYYY-MM-DD">` entry with changelog
  - [ ] Update screenshots if UI changed
- [ ] Commit changes to mpvQC-flatpak repository
- [ ] Run the `Build Flatpak` workflow manually from the Actions tab (it only triggers on workflow dispatch)
- [ ] Updated Flatpak reports `mpvqc-flatpak`: `flatpak run io.github.mpvqc.mpvQC --version`

When the build succeeds, the workflow commits the result to the flatpak repository.

### Website update

These steps apply to the [mpvqc.github.io](https://github.com/mpvqc/mpvqc.github.io) repository.

- [ ] Screenshots updated
- [ ] Version endpoint updated: `static/api/v1/public/version`
