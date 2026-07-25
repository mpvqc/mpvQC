# Issue tracker: GitHub + Local Markdown

This repo uses two trackers:

- **GitHub Issues** (`mpvqc/mpvQC`) — the public tracker. Users report bugs and request features here. Use the `gh` CLI.
- **Local markdown** under `.scratch/` — the working tracker for a larger chunk of work: the spec and the implementation
  tickets derived from it.

Routing rule: anything public-facing (user reports, triage, discussion with reporters) lives on GitHub. Internal working
state for a feature effort (specs, implementation tickets, wayfinder maps) lives in `.scratch/`.

## GitHub Issues (public tracker)

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments` with appropriate `--label`
  and `--state` filters; use `--jq` to compact the output to the fields you need.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

Triage labels apply here — see `triage-labels.md`.

**PRs as a request surface: no.**
_(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

## Local markdown (working tracker)

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` —
  never a single combined tickets file
- Ticket state is recorded as a `Status:` line near the top of each issue file
- Comments and conversation history append to the bottom of the file under a `## Comments` heading
- If the effort stems from a public report, put a `Tracks: #<number>` line near the top of the spec so the GitHub issue
  can be closed when the work lands

## When a skill says "publish to the issue tracker"

- Triage outcomes, or comments and labels on a user report → GitHub, via `gh`.
- A spec or implementation tickets for a feature effort → files under `.scratch/<feature-slug>/` (creating the directory
  if needed).

## When a skill says "fetch the relevant ticket"

- A `#<number>` reference → `gh issue view <number> --comments`.
- A file path or `NN` ticket number → read the file under `.scratch/`. The user will normally pass the path directly.

## Wayfinding operations

Used by `/wayfinder`. Wayfinding is internal working state, so it lives in the local tracker. The **map** is a file with
one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` — the Notes / Decisions-so-far / Fog body.
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A
  `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records
  `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number
  wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer
  (gist + link) to the map's Decisions-so-far in `map.md`.
