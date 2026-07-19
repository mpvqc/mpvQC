<!--
SPDX-FileCopyrightText: mpvQC developers

SPDX-License-Identifier: MIT
-->

# Domain glossary

Terms the code uses for the import pipeline. Keep entries short. Add a term when you name a module after a concept that
is not listed here.

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
