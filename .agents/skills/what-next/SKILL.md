---
name: what-next
description: An overview of everything open, with one recommendation.
disable-model-invocation: true
---

# What next

One picture of everything that is open, so the user can see where they are. It keeps them organised; it does not
dispatch agents, and it never starts work.

## 1. Resolve the substrate and the board

`docs/agents/issue-tracker.md` holds the probe, the board lookup and every `gh` recipe below. Run it silently.

On the contributor substrate there is no private tracker and no board, so sources 1 and 4 come back empty and the
overview is whatever the rest of the sources give. That is a normal run, not a degraded one — say nothing about it.

## 2. Gather

Five sources. Fetch them concurrently.

1. **Open issues in `mpvqc/internal-tickets`.** Readiness labels drive everything. Fetch sub-issue counts for progress,
   and `blocked_by` so a blocked ticket can be kept out of the recommendation.
2. **Open PRs in `mpvqc/mpvQC`.** The only place "done but not merged" lives.
3. **The current branch and working tree.** What the user is already mid-way through.
4. **`.scratch/` files carrying `Substrate: fallback`.** Offer to migrate each into `internal-tickets`.
5. **The public tracker, split by triage label:**

   | Label                                | Treated as                                        |
   | ------------------------------------ | ------------------------------------------------- |
   | `ready-for-agent`, `ready-for-human` | Real work, and a candidate for the recommendation  |
   | `needs-triage`                       | Its own bucket: cheap, time-sensitive, someone is waiting |
   | `needs-info`                         | Blocked on the reporter, excluded                  |
   | `wontfix`                            | Excluded                                           |

   Most of those labels do not exist on the public tracker yet — see `triage-labels.md`. The rule holds as they appear.

   `needs-triage` stays its own bucket instead of being ranked with the rest, because it is cheap and time-sensitive
   while backlog work is expensive and patient. Ranked together, one always buries the other.

`TODO` comments and the rest of `.scratch/` are not sources. Leave them alone.

## 3. Reconcile drift

Agents forget to update tickets, and the instruction telling them to is advisory. So assume non-compliance and detect
it instead of trusting the state:

| What you see                                                                | What it means            | Where it prints              |
| --------------------------------------------------------------------------- | ------------------------ | ---------------------------- |
| `In Progress`, no closing comment, no recent commits                         | Started and dropped      | In flight, marked stalled    |
| Closed with a recorded SHA that is not on `main` (`git merge-base --is-ancestor <sha> main`), on a branch that still exists | Unmerged work the branch's own row already covers | Nowhere of its own |
| The same, but the recorded branch is gone from the remote                    | The cherry-pick case     | In flight, flagged for a human to check rather than guessed at |
| A childless issue with no readiness label                                    | A filing bug             | One line under Backlog       |

## 4. Rank

Fixed precedence:

1. **Land what exists.** Unmerged work decays — it conflicts, it goes stale, and only the user can test it.
2. **Their flow.** What they are already doing beats starting something new.
3. **Handoff-ready work.** `ready-for-agent` items, presented as information — "these could be handed off" — never as a
   dispatch queue.

A ticket with a live `blocked_by` cannot be the recommendation. It still counts in the backlog.

**Platform.** An item that can only be done on the other OS stays **visible but demoted**: it is marked "not here" and
never becomes the recommendation. Hiding it would make the same overview report different totals on different
machines, which is the exact disorientation this skill exists to remove.

## 5. Print it

Straight to the terminal as markdown. No artifact, no file: an overview is true for about an hour, and writing one
would leave a stale copy behind on every run, which is `.scratch/` failing all over again.

Four layers, and the detail in each is proportional to how soon it matters:

1. **In flight** — one row per piece of unmerged work. A branch and the PR carrying it are one piece, so they share a
   row: branch, arrow, PR, then its state. Usually 1 to 3 rows. Everything here is still open; work that is closed is
   done with, and the user is reading this to find what is left.
2. **Waiting on you** — listed, **capped at 10**, then `+N more`. `needs-grilling`, `ready-for-human`, and the public
   `needs-triage` bucket.
3. **Backlog** — not listed. One line per epic with its progress, then counts for loose tickets and `ready-for-agent`.
4. **Next** — one sentence, plus why.

**Every section's last line is a bare URL** opening that same view on GitHub with the filter already applied — written
out in full, starting `https://`, on a line of its own. Bare, because this skill ships to whatever terminal a
contributor runs and a plain URL survives one that renders no links at all, as well as being copy-pasteable.

Items stay plain `#31` text. Twenty lines of link syntax is harder to read than twenty lines of numbers, and the
section footer is what carries the user to GitHub.

Fill these in, one per section:

| Section        | URL                                                                                  |
| -------------- | ------------------------------------------------------------------------------------ |
| In flight      | `https://github.com/mpvqc/mpvQC/pulls`                                                 |
| Waiting on you | `https://github.com/mpvqc/internal-tickets/issues?q=is%3Aopen+label%3Aneeds-grilling` and `https://github.com/mpvqc/mpvQC/issues?q=is%3Aopen+label%3Aneeds-triage` |
| Backlog        | the board's `url`, from `gh project list --owner mpvqc --format json`                  |
| Next           | whichever of the above the recommendation came from                                    |

The overview is a jumping-off point, not a dead end.

````markdown
## In flight

- `appearance-domain` → PR #31 Colour scheme follows the system — draft, 12 commits, 2 unpushed, waiting on your testing
- #7 closed on `abc1234`, and the branch that carried it is gone from the remote — check whether it landed

https://github.com/mpvqc/mpvQC/pulls

## Waiting on you

- #1 Colour scheme — `needs-grilling`
- #9 Window resize on a tiling compositor — `ready-for-human`, **not here** (Windows)
- mpvQC#204 Crash when opening a document — `needs-triage`

https://github.com/mpvqc/internal-tickets/issues?q=is%3Aopen+label%3Aneeds-grilling
https://github.com/mpvqc/mpvQC/issues?q=is%3Aopen+label%3Aneeds-triage

## Backlog

- #1 Colour scheme — 0/5
- #2 View model dataflow — 0/2
- 3 loose tickets, 4 `ready-for-agent`
- #22 has no readiness label

https://github.com/orgs/mpvqc/projects/4

## Next

Test PR #31 and land `appearance-domain`. Nobody else can test it, and it goes stale while it waits.

https://github.com/mpvqc/mpvQC/pull/31
````

The four sections are the whole reply, and the URL under **Next** is the last thing you print. Deeper detail is a
follow-up question in the same session — "show me the loose ones" — rather than something every run prints.

## Done when

- Every one of the five sources was read, or was empty because the substrate says so.
- Every open in-flight item appears in section 1, including the ones drift reconciliation found rather than the tickets
  claimed, and each branch shares its row with the PR that carries it.
- Nothing is hidden for being on the other OS; those items are listed and marked "not here".
- Each of the four sections ends on a bare `https://` URL of its own, on its own line.
- The recommendation is one sentence with its reason, and nothing was written to disk.
- The reply ends on the **Next** URL.
