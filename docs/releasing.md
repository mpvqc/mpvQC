<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Building a New Release

This guide is intended for mpvQC developers preparing a new release.

## Pre-release Checklist

- Update libmpv in the CI pipeline
- Check if default mpv.conf and input.conf are up-to-date
- Ensure there are no Python linter issues.
- Confirm translations are complete and up-to-date.
  - Run `just update-translations`. There should **not** be any new translation
- Recommended: Manually verify that a recent CI build runs on Windows.
- Recommended: Manually verify that a recent build runs on Linux.

## Release Build Process

1. **Tag a commit**: Tagging initiates a new CI build that generates three artifacts:

   - `mpvQC-0.9.0-beta-7fa34c9d-win-x86_64.zip`: This is the finalized Windows build, containing the project name
     `mpvQC`, release version `0.9.0-beta`, and git commit `7fa34c9d`.
   - `release-build-linux.zip`: Compiled sources including resources for Linux.
   - `release-build-windows.zip`: Compiled sources including resources for Windows.

2. **Download all artifacts**.

3. **Draft a new release** in the GitHub Releases section.

4. **Upload all three artifacts**.

5. **Add release notes** detailing new features, updates, and changes.

6. **Publish the release**.

With this, the Windows release process is complete. Additional steps are required for Linux, detailed below.

## Additional Linux Release Steps

The following instructions apply to the [mpvQC-flatpak](https://github.com/mpvqc/mpvQC-flatpak) repository.

1. **Update the flatpak manifest** (`io.github.mpvqc.mpvQC.yml`):

   - Confirm the latest mpv and dependency versions and any specific build changes.
   - Update pypi dependencies using the `flatpak-pypi-checker.py` script.
   - Update mpvQC sources used in the build, linking to the `release-build-linux.zip` file in the release.

2. **Update flatpak metadata** (`io.github.mpvqc.mpvQC.metainfo.xml`):

   - Add the latest changelog.
   - Update screenshots and other relevant metadata if needed.

3. **Trigger a new flatpak build** via GitHub Actions in the `Build Flatpak` section.

Once the build succeeds, it will be automatically committed to the flatpak repository, allowing users to access the
latest version through regular updates.

### Tips

To minimize release delays from flatpak build issues, consider testing the flatpak build locally first:

- Run `just build` in the mpvQC repository
- For local testing, replace the `https://` URL with a `file://` URL to verify the local build of mpvQC is
  successful.
