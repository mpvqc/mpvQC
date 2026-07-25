<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

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

## Build origin

- **Channel**: the store an official build ships through, stamped into build-info at build time (`github-releases`,
  `mpvqc-flatpak`). Empty in git and in every build the release pipelines did not stamp. A channel names a store,
  never a packaging format ("flatpak" is not a channel; Flathub would be a different channel).
- **Build origin**: whether this binary came from a project release pipeline: `ChannelRelease(channel)` or
  `Unofficial`. Declared by the pipeline, never inferred at runtime; the Flatpak app ID can veto an official claim
  but never grant one.
