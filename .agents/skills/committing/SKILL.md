---
name: committing
description: Use when about to commit in this repo.
---

# Committing

## The gate

Run a code review over the working tree against `HEAD`, staged and unstaged, new files included, and settle every
finding: fix it, or say why it stands. A review from earlier in the session covers only code unchanged since. Only the
user can waive the review, by asking for the commit, and every commit holds work the user has already seen.

## Steps

1. `git add` the new files this change brings, and nothing else. `just fmt` skips untracked files, and other work in
   the tree stays out of this commit.
2. Run `just build-develop`. It regenerates the file list in `pyproject.toml`, which goes stale silently when a file is
   added, removed, or renamed. The rewrite belongs in this commit.
3. Run `just fmt` until it comes back clean. Its hooks rewrite files across the repo; rewrites outside this change
   stay out of the commit.
4. Update the docs the change reaches: `GLOSSARY.md` for a domain term, the guide under `docs/` that covers what
   changed, `AGENTS.md` or the skills for an agent-facing rule.
5. Write the message with `commit-conventions`: Conventional Commits, 50/72. Claim only what you verified; "fixes" is
   for behaviour you watched fail and then pass. Say what the code did, with no author, culprit commit, or upstream
   project to blame.
6. Close the ticket this commit completes, per `filing-tickets`.
7. When a larger chunk of work is done, offer to push and to write the manual checks with `manual-checks`.

## Done when

Every step ran, and the commit holds exactly this change and its `pyproject.toml` rewrite.
