---
name: filing-tickets
description: File a ticket where it belongs, in the shape the tracker expects. Use when the user directs you to file something, to file the findings from a review report, to record a finding they rejected, when you pick up a ticket to work on, or when a commit completes a ticket. Filing fires only when directed.
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
  `GLOSSARY.md` picks one of the two at random.
- **Opinion**: "The appearance package has more files than the other feature packages." Never done, nothing breaks,
  degrades or misleads. It is an observation about shape.
- **Opinion**: "`MpvqcAppearance` might deserve a better name someday." Never done, the name is exactly as good as it
  is now.

## Where it goes

Resolve the substrate before writing anything. `docs/agents/issue-tracker.md` holds the probe, the three destinations
and every `gh` recipe this skill names. The probe is silent on the happy paths, so run it and say nothing about it.

## The ticket

Every ticket wears the same two headings, whether it came out of a review report, a grilling session or a one-line ask.
`to-tickets` publishes this shape too, so nobody has to work out which skill wrote which issue. An **epic** is the
exception: its body is a spec, not a ticket.

````markdown
## What to build

The end-to-end behaviour this ticket makes work, told from outside the code — not a layer-by-layer implementation
list.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

---

🤖&nbsp;&nbsp;_Written by <model>_
````

- **Title**: plain, and it states the change.
- **Self-contained.** The analysis that produced it gets deleted, so _What to build_ carries the whole argument: what
  is wrong, why that is worth anyone's afternoon, and what the code does instead.
- **Acceptance criteria are how you discharge test 2 of the bar.** Each one checkable by a reader who never saw the
  analysis. A criterion that needs the review report reopened to evaluate is not yet a criterion.
- **Name the thing, not where it lives.** A symbol, a component, a command — not `label_width_calculator.py:40-41`. Line
  numbers go stale before anyone picks the ticket up. A code snippet earns its place only where it pins a decision prose
  cannot — a state machine, a schema, a type shape — trimmed to the decision rather than left as a working demo.
- **One fresh context window.** A ticket an agent cannot finish in one is an epic, and the work is its children.
- **Relationships go through the API, never into the prose.** A parent is a sub-issue link, a blocker is a `blocked_by`
  edge, and `docs/agents/issue-tracker.md` has both calls. A body that names its own edges goes stale as the graph
  moves.
- **Provenance**: one line at most, at the end of _What to build_ — _"found during an architecture review,
  2026-08-03"_.
- **Platform**: when the work can only be done on one OS, _What to build_ says which.
- **Footer**: every body and comment on the private tracker ends with the agent footer from
  `docs/agents/issue-tracker.md`, the closing comment included.
- **Labels**: one readiness label, and nothing else.

| The ticket is                                                                             | Label                                |
| ----------------------------------------------------------------------------------------- | ------------------------------------ |
| Something an agent can take unattended                                                     | `ready-for-agent`                    |
| An accepted finding, not yet broken down                                                   | `ready-for-human` + `needs-grilling` |
| Work needing a human for another reason: manual testing, the Windows box, design taste     | `ready-for-human`                    |

An issue **with children carries no readiness label**: its readiness is whatever its children say. A _childless_ issue
with no readiness label is a filing bug.

`needs-grilling` is the only qualifier. Add a second one only after wanting it twice.

## Structure

- **An epic is an issue that has children**, and its body is the effort's spec. No type, no label. A plain ticket
  becomes an epic the day a grilling session rewrites its body into a spec and hangs sub-issues off it.
- **Three levels is the norm**: epic (the spec) → ticket (planned work) → split (a ticket you _started_ that turned out
  to be two). Level 3 is for decomposition you discover, not decomposition you plan.
- **A sub-issue passes one test**: _finishing the children finishes the parent._ Grouping by topic, or by which
  afternoon the findings came from, fails it.
- **Every filed issue goes on the board.**

## Declines

A finding the user rejected — one that is real, and that the next review will find again — is **filed as an issue and
immediately closed as not planned**, with the reasoning in the body:

```bash
gh issue close <n> --repo mpvqc/internal-tickets --reason "not planned" --comment "..."
```

- Only a finding the **user** rejected earns a record. A finding you filtered out yourself under the bar leaves
  nothing behind.
- A decline lives in the tracker. A code comment earns its place on the `load-bearing-comments` test alone, whatever
  a review flagged.
- Where the same argument keeps being re-argued, it graduates to an **ADR**.

## Working a ticket

A ticket moves the moment the work does:

**Claim**: picking up a ticket, set the board `Status` to `In Progress` before starting. Branch names cannot carry the
claim, because many tickets share one branch.

**Update**: comment the ticket when the work shifts under it — a decision taken, a dead end hit, scope cut or grown.
The bar: a reader who opens only the ticket knows where the work stands.

**Close**: a ticket closes with the commit that completes it, not when its branch merges. The closing comment records
**branch and SHA**, which stays true after a cherry-pick:

```bash
gh issue close <n> --repo mpvqc/internal-tickets --comment "Done on \`appearance-domain\`, \`abc1234\`"
```

**The link runs from the internal ticket out to the public side, and only that way.** Keep internal issue references
out of public PRs and commit messages: everyone can read them and nobody outside can open them.

## Filing a batch

More than one finding at once — anything out of a review report, a survey or a sweep — goes through
[`batch.md`](batch.md) **before the user sees any of it**. It puts a dedupe pass in front of everything above, and
without it you will re-file things that were filed, fixed or declined months ago. Read it now if that is the job.

## Done when

- The user directed this filing.
- Every finding left through exactly one of the four outlets, and the ones that left through outlet 4 were said out
  loud.
- Every filed ticket clears all three tests and follows every rule under _The ticket_ and _Structure_.
- A ticket you picked up is `In Progress` on the board, and a ticket a commit completed is closed with branch and SHA.
