# Issue tracker: where work is written down

Three destinations, and this document is the authority on which one a given thing goes to. Everything else — the
`filing-tickets` skill, `what-next`, `triage`, `to-tickets`, `to-spec`, `implement`, `qa` — defers here rather than
carrying its own copy of the routing rules.

| Destination                     | What lives there                                             | Who writes there                              |
| ------------------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| `mpvqc/mpvQC` (public)          | User reports, triage, discussion with reporters               | Users. An agent never opens an issue here.    |
| `mpvqc/internal-tickets` (private) | Every internal work item: findings, tickets, epics, specs   | The maintainer, or an agent they direct       |
| `.scratch/` (local, gitignored) | Disposable artifacts: review reports, prototypes, surveys     | Anyone. Also the contributor and fallback path for tickets. |

The rule: **nothing with a status stays local.** If a thing can be open or closed, it belongs in a tracker.

The test for "is this scratch?": _if it has to survive a machine switch, it isn't scratch._ `.scratch/` is gitignored,
so it exists on one machine, in one working directory. A background agent in `.claude/worktrees/<x>` cannot see it at
all.

## Substrate resolution

Which of the three you get is probed, not configured, and the probe is **silent on the happy paths**. Identity is
decided on the **public** repo, because a private repo returns 404 rather than 403 to anyone who cannot see it — probe
the private one and a lost token looks exactly like a contributor.

1. `gh api repos/mpvqc/mpvQC --jq .permissions.push`
   - no `gh`, or no authenticated account → **contributor**
   - `false` → **contributor**
   - `true` → maintainer, go to 2
   - anything else — a `401` from a stale token, a network failure, output you did not expect → **degraded**, go to 3
2. `gh api repos/mpvqc/internal-tickets`
   - `200` → file in `mpvqc/internal-tickets`
   - anything else at all — 404, 401, a lost scope, the repo renamed → **degraded**, go to 3
3. **Degraded.** Write the ticket to `.scratch/` with a `Substrate: fallback` line near the top, and print one visible
   line: _"GitHub unreachable, filed to `.scratch/`, re-file once auth is fixed."_ Then carry on. An agent mid-task
   cannot fix auth, and a misplaced ticket beats a lost one. `what-next` finds the marker later and offers to push it
   to `internal-tickets`.

For a contributor, `.scratch/` is the terminal answer, not a fallback: file there, say nothing about the probe, and
write no marker. Only degraded filings carry `Substrate: fallback`.

## `mpvqc/internal-tickets` (private tracker)

Everything that starts inside the project. See the `filing-tickets` skill for what earns a ticket and what one looks
like; the mechanics live here.

- **Create**: `gh issue create --repo mpvqc/internal-tickets --title "..." --body-file <file>`
- **Read**: `gh issue view <n> --repo mpvqc/internal-tickets --comments`
- **Read a spec**: `gh issue view <n> --repo mpvqc/internal-tickets --json body --jq .body` — the whole spec, on any
  machine, without a clone
- **Write a spec**: draft locally, then `gh issue edit <n> --repo mpvqc/internal-tickets --body-file spec.md`
- **Close**: `gh issue close <n> --repo mpvqc/internal-tickets --comment "..."`

### The agent footer

Every issue body and every comment an agent writes here ends with a rule and one line, both after a blank line:

```text
---

🤖&nbsp;&nbsp;_Written by Claude Opus 5_
```

Name whichever model is writing, italic, with the emoji left out of the italics. The two `&nbsp;` are deliberate:
plain spaces collapse to one and the emoji ends up crowding the text. The plain display name is enough —
no version suffix, no context-window variant, none of which mean anything to a reader a year from now.

Agents file through the maintainer's token, so the author field says nothing about who wrote the text. The footer is
the only thing that does, and a reader deciding how much to trust a wall of confident prose needs it. It goes on
anything with a body: a new ticket, a spec rewrite, a comment, a closing comment. It means an agent had a hand in the
text, so an agent that rewrites a body a human wrote adds it as well, under its own name.

Nothing else carries it. Titles, labels and board fields have nowhere to put a footer, and an emoji in a title wrecks
every list the title appears in.

Sub-issues and dependencies are keyed by the **database id**, never the issue number:

```bash
gh api repos/mpvqc/internal-tickets/issues/<n> --jq .id

# hang a child off a parent
gh api --method POST repos/mpvqc/internal-tickets/issues/<parent>/sub_issues -F sub_issue_id=<child database id>

# record that <n> waits for another ticket
gh api --method POST repos/mpvqc/internal-tickets/issues/<n>/dependencies/blocked_by -F issue_id=<blocker database id>

# read them back
gh api repos/mpvqc/internal-tickets/issues/<n>/dependencies/blocked_by
```

Use `-F`, not `-f`: the API wants an integer and `-f` sends a string.

Sub-issues nest 8 levels deep with 100 children per parent, and an issue has at most one parent, so the structure is a
tree. A parent does not auto-close when its last child closes.

### Finding the board

By convention, not configuration. `gh project list --owner mpvqc` and use the single project it returns.

- Exactly one project → that is the board.
- None → normal and quiet. Contributors cannot see org projects at all, so say nothing and skip every board step.
- More than one → say which ones you found and skip the board steps rather than guess.

Add an issue with `gh project item-add <number> --owner mpvqc --url <issue url>`. The board's own workflows
already pull in new issues and sub-issues, so this is a safety net for what they miss, not the thing that puts
work on the board.

Field ids differ per board, so read them rather than hardcoding them:
`gh project field-list <number> --owner mpvqc --format json`. `Status` is a single-select with `Todo`, `In Progress`
and `Done`; setting it needs `gh project item-edit` with the project id, the field id and the option id from that
listing.

## `mpvqc/mpvQC` (public tracker)

Users report bugs and request features here, and triage happens here. Only reports from users open issues on this
tracker; an agent comments, labels and closes, but never files.

- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments` with the `--label` and
  `--state` filters you need; use `--jq` to compact the output
- **Comment**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Inside a clone, `gh` infers this repo from `git remote -v`, so these need no `--repo`.

Triage labels apply here — see `triage-labels.md`.

**PRs as a request surface: no.**
_(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

## `.scratch/` (local)

Disposable artifacts need no format. Tickets written here — by a contributor, or by a degraded filing — use this one:

- One effort per directory: `.scratch/<effort-slug>/`, with the spec at `spec.md`
- One file per ticket at `.scratch/<effort-slug>/issues/<NN>-<slug>.md`, numbered from `01` — never a single combined
  tickets file
- A ticket belonging to no effort: `.scratch/tickets/<NN>-<slug>.md`, numbered the same way
- A `Status:` line near the top of every ticket file
- A `Blocked by: NN, NN` line near the top where order matters. A ticket is unblocked when every file it lists is
  `resolved`
- Comments and conversation history append to the bottom under a `## Comments` heading
- If the effort stems from a public report, a `Tracks: #<number>` line near the top of the spec, so the public issue
  can be closed when the work lands
- `Substrate: fallback` near the top when a degraded filing put it here

## When a skill says "publish to the issue tracker"

- Triage outcomes, or comments and labels on a user report → the public tracker, via `gh`.
- A finding, a ticket, a spec, or anything else that starts inside the project → resolve the substrate, then file it
  there. The `filing-tickets` skill owns this path.

## When a skill says "fetch the relevant ticket"

- A bare `#<number>` → the substrate you resolved. On the private tracker,
  `gh issue view <n> --repo mpvqc/internal-tickets --comments`.
- An `mpvqc/mpvQC#<number>` reference, or a number the user names as a user report → the public tracker.
- A file path or `NN` ticket number → read the file under `.scratch/`. The user will normally pass the path directly.

## Wayfinding operations

Used by `/wayfinder`. Wayfinding is internal working state, so it lives on the substrate the probe resolved. On the
private tracker there is nothing wayfinding-specific to build — the tracker already has every piece:

| Wayfinding term | On `mpvqc/internal-tickets`                                                |
| --------------- | -------------------------------------------------------------------------- |
| Map             | The epic's body — the Notes / Decisions-so-far / Fog sections               |
| Child ticket    | A sub-issue, with the question in its body                                  |
| Ticket type     | A prose line in the body (`research` / `prototype` / `grilling` / `task`)   |
| Blocking        | The `blocked_by` dependencies API                                           |
| Frontier        | Open sub-issues that no `blocked_by` entry holds and nobody is assigned to  |
| Claim           | Assign yourself, and set the board `Status` to `In Progress`                |
| Resolve         | Comment the answer, close the issue, then append the gist and its link to the epic's Decisions-so-far |

On `.scratch/`, the same operations run against the file format above: `Status: claimed` / `Status: resolved`, the
`Blocked by:` line, and an `## Answer` heading for the resolution.
