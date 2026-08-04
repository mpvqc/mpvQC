# Filing a batch

Same bar, same four outlets, applied to N findings — with a dedupe pass in front of everything else.

The dedupe has to live here. A review skill that comes from a marketplace cannot be taught about this tracker, so it
will re-find the same things forever. Nothing upstream will ever stop it.

## 1. Dedupe on intake

Before the user sees a single finding, fetch what the tracker already holds and match the report against it:

```bash
gh issue list --repo mpvqc/internal-tickets --state all --limit 500 \
  --json number,title,body,state,stateReason,labels
```

Match on what a finding _claims_, not on wording — the review re-words the same defect every run.

| The finding matches an issue that is | It means             | Do                                        |
| ------------------------------------ | -------------------- | ----------------------------------------- |
| Open                                 | Already on the backlog | Drop it                                 |
| Closed, `not planned`                | Already declined     | Drop it                                   |
| Closed, `completed`                  | Already fixed        | The review still sees it: **a regression** |

A regression is the one thing in this pass that gets louder rather than quieter. Say which issue closed it, and put it
in front of the user first — a fix that came undone outranks anything new the report found.

## 2. Report every drop

One line per group, before the walkthrough:

> Skipped 3 already on the backlog: #4, #7, #9.
> Skipped 3 already declined: #12, #18, #23.

A finding declined in March can be valid in August, because the code moved underneath it. A silent filter hides
exactly that, so the drops are always spoken.

## 3. Walk through what is left

One at a time, with the user: accept, decline, or noise. The bar in `SKILL.md` decides what you even bring — a finding
that fails it is an opinion, and opinions go through outlet 4 rather than into the walkthrough.

## 4. File the accepted findings

All at once, each as its own ordinary ticket in the shape `SKILL.md` describes.

Not an epic with sub-issues. A review is a _source_, not a goal: its findings have nothing in common but the afternoon
they were found, so "finishing the children finishes the parent" is false and nobody can ever finish the epic. It also
burns the level you need for splitting one big finding into real work.

No per-review label either. One label per review is unbounded growth.

## 5. File the declines

Each one closed as not planned, per the Declines section of `SKILL.md`. Only findings the user rejected in step 3 —
never the ones you dropped in step 1 or filtered out under the bar.

## 6. Say the report can go

End with it plainly: the report is now safe to delete. Everything worth keeping is in the tracker, which is the thing
that survives a machine switch. That is the whole point of the pass.

## Done when

- Every finding in the report is accounted for: dropped with its reason spoken, filed, declined, or named as noise.
- Any regression was surfaced before the walkthrough, with the issue that closed it.
- Every accepted finding is its own ticket — no epic, no per-review label.
- You told the user the report can be deleted.
