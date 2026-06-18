<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

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
- [ ] No new untranslated strings verified: `just update-translations`

Run the formatter before committing.

### Update documentation, visuals, and release notes

- [ ] Splash updated
- [ ] README.md updated
- [ ] NOTICE.txt verified:
  - [ ] All dependencies match `pyproject.toml`
  - [ ] License identifiers match each package's actual metadata, not the project's umbrella license
  - [ ] `REUSE.toml` aggregate and `LICENSES/` texts are in sync: `reuse lint`
- [ ] New screenshots created (both light and dark themes) for Website and Flatpak
- [ ] Release notes drafted

### Verify build and manual testing

This is the final gate before tagging.

- [ ] libmpv in CI updated: `.github/workflows/release.yml`
  - Visit https://github.com/shinchiro/mpv-winbuild-cmake/releases
  - Find latest `mpv-dev-x86_64-*-git-*.7z` asset
  - Copy URL and SHA256 hash
  - Update `LIBMPV_URL` and `LIBMPV_SHA256` in workflow file
- [ ] CI verified green: https://github.com/mpvqc/mpvQC/actions
- [ ] Manual testing on Windows (areas the test suite cannot exercise):
  - [ ] Video playback works
  - [ ] Basic export writes a real file via the native file dialog
  - [ ] Smoke-click each menu and the window chrome (close/minimize/maximize)
- [ ] Manual testing on Linux (on the locally built Flatpak):
  - [ ] Flatpak builds locally
  - [ ] Flatpak installs locally
  - [ ] Flatpak runs locally
  - [ ] Windows manual tests above also pass on Linux
  - [ ] Window chrome verified on both setups (see below)

#### Window chrome verification

The Linux window chrome (drop shadow, rounded corners, frameless resizing) is self-drawn and compositor-dependent, so CI cannot cover it. Verify it on the locally built Flatpak before tagging, on both setups:

**Desktop environment (e.g. GNOME, KDE Plasma)**

- [ ] Drop shadow is drawn around the window and strengthens while it is focused
- [ ] Corners are rounded (top corners and bottom-right; the video corner may stay square in the horizontal layout)
- [ ] Menu bar, close button and footer hover highlights stay within the rounded corners
- [ ] Maximize, fullscreen and back to normal land in the expected state (no flicker back to normal)
- [ ] Window drags to the top edge and resizes from every edge and corner

**Tiling window manager (e.g. Sway, Hyprland, niri)**

- [ ] Window sits flush with no transparent margin and no drop shadow
- [ ] Corners are square

## Release

### Tag and CI build

- [ ] Create annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Push tag to trigger CI: `git push origin vX.Y.Z`
- [ ] Download `mpvQC-X.Y.Z-{commit}-win-x86_64.zip`
- [ ] Download `release-build-linux.zip`
- [ ] Download `release-build-windows.zip`
- [ ] Download complete CI build-log and upload to release issue on GitHub

### GitHub release

- [ ] Draft new release on GitHub
- [ ] Upload all three artifacts
- [ ] Publish release

With this, the Windows release process is complete. Additional steps are required for Linux, detailed below.

## Post-release

### Flatpak distribution

These steps apply to the [mpvQC-flatpak](https://github.com/mpvqc/mpvQC-flatpak) repository.

- [ ] In the manifest update the mpvQC source tag to `vX.Y.Z`
- [ ] Update `io.github.mpvqc.mpvQC.metainfo.xml`:
  - [ ] Bump the top-level `version`
  - [ ] Add a `<release version="X.Y.Z" date="YYYY-MM-DD">` entry with changelog
  - [ ] Update screenshots if UI changed
- [ ] Commit changes to mpvQC-flatpak repository
- [ ] Trigger a new flatpak build **manually** via GitHub Actions in the `Build Flatpak` section.

Once the build succeeds, it will be automatically committed to the flatpak repository. Users will receive the new version via regular updates.

### Website update

- [ ] Screenshots updated
- [ ] New version for api calls updated: `static/api/v1/public/version`
