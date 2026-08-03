---
name: filing-tickets
description: File a ticket where it belongs, in the shape the tracker expects. Use when the user directs you to file something, to file the findings from a review report, to record a finding they rejected, or to close out a ticket whose work has landed. Fires only when directed.
---

# Filing tickets

A tracker is worth reading only while everything in it is worth doing. An agent that files what it notices fills the
list with its own opinions, and then nobody trusts the list. So **file only when the user directs it**, and expect most
of what you find to leave through some other door.

## Something you found while doing other work

Say it in your **final message**: a title and a `file:line`, worded so the user can hand it straight back as "file
these". Write nothing, anywhere. If it matters, they will tell you.

## The four outlets

When you find something, you have four moves, not two:

1. **Fix it now** — inside the current change's blast radius, and small. No ticket.
2. **File it** — it clears the bar below, and the user asked for it.
3. **Record a decline** — only for a finding the _user_ rejected. See below.
4. **Say it and let it go** — observations, opinions, "we could maybe someday". It goes in your response or the PR
   body and dies there.

Outlet 4 is a real outcome, not a failure to decide. Most of what a review turns up leaves through it.

## The bar

A **defect** gets a ticket. An **opinion** does not, and a review report emits both in the same confident voice. Three
tests, and all three have to pass:

1. It names **a change to make**, not a fact that is true.
2. You can tell when it is **done** without redoing the analysis that found it.
3. **If nobody ever does it, something is actually wrong.**

Test 3 carries the weight. The one-line form: _what breaks, degrades, or misleads if this is never done?_ When the
honest answer is _"nothing, it would just be nicer"_, you are holding an opinion.

- **Defect**: "`accent_color_preference_for` is public but has no caller outside its own file." Never done, the
  service permanently advertises a method nobody uses, and the next reader wires against it.
- **Defect**: "'Overlay' means two different things in the glossary." Never done, every future agent that reads
  `CONTEXT.md` picks one of the two at random.
- **Opinion**: "The appearance package has more files than the other feature packages." Never done, nothing breaks,
  degrades or misleads. It is an observation about shape.
- **Opinion**: "`MpvqcAppearance` might deserve a better name someday." Never done, the name is exactly as good as it
  is now.

## Where it goes

Resolve the substrate before writing anything. `docs/agents/issue-tracker.md` holds the probe, the three destinations
and every `gh` recipe this skill names. The probe is silent on the happy paths, so run it and say nothing about it.

## The ticket

- **Title**: plain, and it states the change.
- **Body**: **self-contained.** The analysis that produced it gets deleted, so the body carries the whole argument —
  file and line, what is wrong, why it is wrong, and what "done" looks like.
- **Provenance**: one prose line at most, _"found during an architecture review, 2026-08-03"_. The only reason to
  record a source is to go back and read it, and the source is thrown away.
- **Footer**: on the private tracker, the body ends with the agent footer, and so does every comment you leave —
  including the closing one. `docs/agents/issue-tracker.md` has the exact line.
- **Platform**: when the work can only be done on one OS, the body says which. `what-next` reads this.
- **Labels**: one readiness label, and nothing else. Area labels are not used — the body says what a ticket touches
  better than `python` vs `qml` does, and most work crosses both anyway.

| The ticket is                                                                             | Label                                |
| ----------------------------------------------------------------------------------------- | ------------------------------------ |
| Something an agent can take unattended                                                     | `ready-for-agent`                    |
| An accepted finding, not yet broken down                                                   | `ready-for-human` + `needs-grilling` |
| Work needing a human for another reason: manual testing, the Windows box, design taste     | `ready-for-human`                    |

An issue **with children carries no readiness label**. An epic is not work — its readiness is whatever its children
say, and labelling it would let one effort fill several slots in `what-next`'s capped list. That makes a _childless_
issue with no readiness label a detectable filing bug, which `what-next` flags.

`needs-grilling` is the only qualifier. Add a second one only after wanting it twice: a wrong qualifier is worse than
none, because it sends the recommendation the wrong way.

## Structure

- **The spec is the epic.** An effort's spec is the parent issue's body, so any agent on any machine gets the whole
  thing from one `gh issue view`, with no clone.
- **An epic is not a kind of issue. It is an issue that has children.** No type, no label, no ceremony. A finding filed
  as a plain ticket becomes an epic the day a grilling session rewrites its body into a spec and hangs sub-issues off
  it.
- **Three levels is the norm**: epic (the spec) → ticket (planned work) → split (a ticket you _started_ that turned out
  to be two). Level 3 is for decomposition you discover, not decomposition you plan.
- **The rule that keeps a hierarchy honest**: _finishing the children finishes the parent._ Where that sentence is
  false it is not a sub-issue. Grouping by topic, or by which afternoon the findings came from, is the mistake to watch
  for.
- **Order is recorded, not implied.** A grilling session that produces ordered tickets records the order through the
  dependencies API, which is what lets `what-next` compute whether a ticket is startable.
- **Every filed issue goes on the board.**

## Declines

A finding the user rejected — one that is real, and that the next review will find again — is **filed as an issue and
immediately closed as not planned**, with the reasoning in the body:

```bash
gh issue close <n> --repo mpvqc/internal-tickets --reason "not planned" --comment "..."
```

- Only a finding the **user** rejected earns a record. A finding you filtered out yourself under the bar leaves
  nothing behind, and that is correct: they never saw it, so there is nothing to stop from being re-proposed.
- **A comment earns its place on the `load-bearing-comments` test alone.** Where the _why_ is a fact from outside the
  code ("Qt ignores `setColorScheme` from then on"), it was worth writing before any review ran. The review is the
  occasion, never the justification — a code comment written because a review flagged something is comment sprawl, and
  comment sprawl is invisible where a closed issue is visible and prunable.
- Where the same argument keeps coming back and keeps being re-argued, it graduates to an **ADR**. ADRs are numbered
  and curated, so inflation shows.

## Closing a ticket

**A ticket closes when the work is done and pushed, not when it is merged.** Many tickets land on one feature branch,
and the branch merges once the user has tested it, sometimes through a different PR, sometimes as a cherry-pick. Merge
state belongs to the branch rather than to twelve tickets, and it already has a perfect display: the open PR list.

The closing comment records **branch and SHA**:

```bash
gh issue close <n> --repo mpvqc/internal-tickets --comment "Done on \`appearance-domain\`, \`abc1234\`"
```

That stays true after a cherry-pick, because it states something about the past instead of being a pointer that has to
keep resolving.

**The link runs from the internal ticket out to the public side, and only that way.** Keep internal issue references
out of public PRs and commit messages: they are plain, permanent text that everyone can read and nobody outside can
open.

**Claiming**: an agent picking up a ticket sets the board `Status` to `In Progress` before starting. That is the claim
signal — branch names cannot carry it, because many tickets share one branch.

## Filing a batch

More than one finding at once — anything out of a review report, a survey or a sweep — goes through
[`batch.md`](batch.md) **before the user sees any of it**. It puts a dedupe pass in front of everything above, and
without it you will re-file things that were filed, fixed or declined months ago. Read it now if that is the job.

## Done when

- The user directed this filing.
- Every finding left through exactly one of the four outlets, and the ones that left through outlet 4 were said out
  loud.
- Every filed ticket clears all three tests, and its body still stands once the analysis behind it is deleted.
- Every childless ticket carries exactly one readiness label, and every epic carries none.
- Every body and every comment you wrote on the private tracker ends with the agent footer.
- Every filed issue is on the board.
