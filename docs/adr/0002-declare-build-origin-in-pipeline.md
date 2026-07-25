<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Declare build origin in the release pipeline instead of detecting it at runtime

Bug reports need to tell official builds (the Windows zip on GitHub Releases, the project's Flatpak remote) apart from
rebuilds and repackages, which link against a different media stack. The obvious approach, comparing the app ID in
`/.flatpak-info` against the official ID at runtime, marks the wrong builds as official: honest rebuilds keep the
upstream ID (Fedora Flatpaks reuse it, and Flathub derives IDs from the upstream domain). Cryptographic
self-verification fails too: the verifier ships inside the third-party binary, and a signature over a constant can be
copied along with it.

So the pipeline declares the origin at build time. `data/build-info.toml` carries a `channel` field that is empty in
git and written only by `build-aux/set_build_info.py`, from the `MPVQC_BUILD_CHANNEL` environment variable. Exactly
two workflow steps set the variable: the tag-gated `build_windows` job in `release.yml` (`github-releases`) and the
main-gated flatter step in the mpvQC-flatpak repository (`mpvqc-flatpak`, carried into the build sandbox via the
manifest's `secret-env`). At runtime the app treats the channel as an opaque string: a build is official when the
channel is non-empty and, inside Flatpak, the `/.flatpak-info` app ID matches the app ID in build-info. The ID can
veto a claim, never grant one.

## Consequences

- Honest rebuilds (distro packages, forks, branch CI, source builds, manifest copies) report unofficial without doing
  anything. Deliberate impersonation stays possible and is out of scope.
- The app never learns channel names. Adding or moving a channel (for example to Flathub: plain `env` in the Flathub
  manifest, since their builders accept no host environment) touches pipelines only, never application code. Until the
  new pipeline sets a channel, its builds report unofficial: the mechanism fails toward "unofficial", never toward
  "official".
- The stamp must stay constant within a CI cache scope, because flatpak-builder's module cache ignores `secret-env`
  value changes (verified with flatpak-builder 1.4.10). Gating the variable on tags and `main` satisfies this.
