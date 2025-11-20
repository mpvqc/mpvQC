<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

## Pre-release Requirements

### Update Metadata, Dependencies, Configuration Files, and Translations

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

### Verify Build

- [ ] libmpv in CI updated: `.github/workflows/release.yml`
  - Visit https://github.com/shinchiro/mpv-winbuild-cmake/releases
  - Find latest `mpv-dev-x86_64-*-git-*.7z` asset
  - Copy URL and SHA256 hash
  - Update `LIBMPV_URL` and `LIBMPV_SHA256` in workflow file
- [ ] CI verified green: https://github.com/mpvqc/mpvQC/actions
- [ ] Manual testing on Windows:
  - [ ] All menus open correctly
  - [ ] All clickable elements trigger expected actions
  - [ ] Video playback works
  - [ ] Comment creation/editing/deletion works
  - [ ] Basic export works
  - [ ] Extended export works
  - [ ] Extended export error handling works
  - [ ] Basic import works
  - [ ] Import with video file works
  - [ ] Import with subtitle file works
- [ ] Manual testing on Linux:
  - [ ] Flatpak builds locally
  - [ ] Flatpak installs locally
  - [ ] Flatpak runs locally
  - [ ] Manual tests (see above) for Windows also pass on Linux

### Update Documentation, Visuals, Draft Release Notes

- [ ] Splash updated
- [ ] README.md updated
- [ ] NOTICE.txt verified: All dependencies match `pyproject.toml`
- [ ] New screenshots created (both light and dark themes) for Website and Flatpak
- [ ] Release notes drafted

## Release Process

### CI Build

- [ ] Create annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Push tag to trigger CI: `git push origin vX.Y.Z`
- [ ] Download `mpvQC-X.Y.Z-{commit}-win-x86_64.zip`
- [ ] Download `release-build-linux.zip`
- [ ] Download `release-build-windows.zip`
- [ ] Download complete CI build-log and upload to release issue on GitHub

### GitHub Release

- [ ] Draft new release on GitHub
- [ ] Upload all three artifacts
- [ ] Publish release

With this, the Windows release process is complete. Additional steps are required for Linux, detailed below.

## Post-release - Flatpak Distribution

These steps apply to the [mpvQC-flatpak](https://github.com/mpvqc/mpvQC-flatpak) repository.

- [ ] In the manifest update mpvQC source URL to `release-build-linux.zip` from GitHub release
- [ ] In the manifest update mpvQC source SHA256 hash
- [ ] Update `io.github.mpvqc.mpvQC.metainfo.xml`:
  - [ ] Add release entry and add changelog
  - [ ] Update screenshots if UI changed
- [ ] Commit changes to mpvQC-flatpak repository
- [ ] Trigger a new flatpak build **manually** via GitHub Actions in the `Build Flatpak` section.

Once the build succeeds, it will be automatically committed to the flatpak repository. Users will receive the new version via regular updates.

## Post-release - Website Update

- [ ] Screenshots updated
- [ ] New version for api calls updated: `static/api/v1/public/version`
