---
name: committing
description: Use when about to commit in this repo.
---

# Committing

## Before

The user reviews before you commit. Never run `git commit` on work they haven't seen.

`git add` the new files this change brings, and only those. `just fmt` reads the working tree, but only for files git
already tracks, so a file that was never added is invisible and every hook passes without having read it. A file git
already tracks is read whether or not its changes are staged.

Leave everything else where it is. The tree can hold new or already-staged files belonging to other work, and they
stay out of this commit.

Now run `just build-develop`. It rewrites the pyside6 project file list in `pyproject.toml` from what is on disk, and
nothing else does: a file this change adds, removes, or renames leaves that list stale, and nothing warns. The rewrite
belongs in this commit. It has to run before the formatter, which is what formats the list it wrote.

Then run `just fmt`. It has to come back clean, not merely run. It works over the whole repo and several of its hooks
rewrite files in place, so check what it touched: a fix that lands outside this change is someone else's, and it stays
out of the commit too.

## Docs a change can strand

Docs go stale quietly, so check the ones your change reaches:

| What you changed          | What to update                |
| ------------------------- | ----------------------------- |
| A domain term, new or renamed | `CONTEXT.md`              |
| An architectural decision | a new ADR under `docs/adr/`   |
| Setup steps or commands   | `docs/development.md`         |
| The layer split           | `docs/architecture.md`        |
| An environment variable   | `docs/configuration.md`       |
| How translations are handled | `docs/internationalization.md` |
| The release steps         | `docs/releasing.md`           |
| The QC document format    | `docs/document-format/`       |

Agent-facing rules live in `CLAUDE.md` and the skills beside this one. A rule that changed belongs there too.

## The message

[Conventional Commits](https://www.conventionalcommits.org/) format, 50/72 where it fits.

The body says why, not what. The diff already shows what. No bullet list of individual changes.

Plain, everyday English, the casual register of an open source log: common words and short sentences a non-native
reader follows on the first pass. When the work came from a plan, the message stands without it: a reader who never
saw the plan still understands it.

Modest claims: the message promises only what you verified. A change that narrows a symptom narrows it; "fixes" is
for behaviour you watched fail and then pass.

Faults are behaviour, not blame: say what the code did and stop there. No author, no culprit commit, no project at
fault, no talk of reporting anything upstream.

## After

A ticket this commit completes gets its closing comment now — see the `filing-tickets` skill.

When a larger chunk of work is done, offer to push, and to write the manual checks with the `manual-checks` skill.

## Done when

- The new files this change brings are added, and nothing else is.
- `just build-develop` ran, and the file list it rewrote in `pyproject.toml` is in the commit.
- `just fmt` came back clean, and whatever it rewrote outside this change stayed out of the commit.
- Each doc in the table that the change reaches now describes what the code does.
- The message claims only what was verified, in everyday words, and names no culprit.
- A ticket this commit completes is closed.
