---
name: manual-checks
description: Use when the user asks what to verify by hand after a package of work, when they ask to update the manual checks, or when the committing skill hands off after a chunk lands.
---

# Manual checks

Automated tests stop at the process boundary. Past it sits everything a human has to look at: what the compositor does
with a size request, whether a native module even loads, what the window looks like. This skill names that work for one
branch and nothing else.

The deliverable is one section, checkboxes only, no prose.

## Blast radius

An item earns its place when all three hold:

- The branch changed the code path behind it.
- No automated test covers it.
- A human can see it hold or fail in one action.

The branch decides the list. A check that was worth running last month but sits outside this diff belongs to no one.

## Steps

### 1. Read the diff

Diff the branch against its merge base with `main`. That is the blast radius, not the last commit.

Done when you have the full file list and have read every changed hunk that can reach running code.

### 2. Read the arrangement catalogue

`select_platform_backend` picks one arrangement per run, and each branch is one arrangement the app supports. Read it,
don't recall it. `CONTEXT.md` defines the platform terms the checks will use.

Done when you can name every arrangement, the branch that selects it, and what makes it different.

### 3. Fan out

Spawn subagents to confirm the blast radius. Split the changed files into areas and give each subagent one. Ask each
for:

- The arrangements that reach this change, and the flags or branches that decide it.
- What a user sees in the app when it works, and what they see when it breaks.
- The tests that already cover it, named.

Spawn as many as the diff needs. Two changed files is one subagent; a rewrite across the window stack is a dozen.

Done when every changed file sits in exactly one report, and every report either names items or names why the change
cannot be seen in the app.

### 4. Build the section

Group by arrangement, then by area. Skip an arrangement no subagent reached: a Linux-only branch gets no Windows
heading.

Every heading is one arrangement. There is no shared bucket, no `Any arrangement`, no `All platforms`, no item parked
outside an arrangement. The boxes are how the user records which machine they sat at, so a box that spans arrangements
records nothing and they have to start over.

Repetition is the point, not waste. Write the same check under every arrangement it reaches, and where an arrangement
changes what the user should see, say that in its copy rather than bolting a parenthetical onto a shared line.

Lead every arrangement heading with its emoji, so the user finds their machine by shape before they read a word:
🪟 Windows, 🐧 Linux desktop, 🧱 Linux tiling. An arrangement the catalogue grows later picks up its own emoji and
keeps it from then on.

Name an area after the thing the user touches: `Window controls`, `Video resize`, `Overlays`. Not after the module.

Write each item as the state that should hold, present tense, one observable per line:

```markdown
## Manual checks before merging

### 🪟 Windows

#### Window controls

- [ ] Loading a video resizes the window to fit it
- [ ] Escape leaves fullscreen

### 🧱 Linux tiling

#### Window controls

- [ ] Escape leaves fullscreen
- [ ] Known and accepted: loading a video leaves the window alone, the compositor decides the size
```

Escape repeats because it reaches both arrangements. Resize is written twice, differently, because the two
arrangements owe the user different behaviour.

Every line under a heading is a checkbox. Setup a check needs rides inside the item. A quirk the branch knowingly
leaves behind is still an item, marked `Known and accepted:`.

Boxes ship unchecked. The user ticks them.

Done when every item passes the blast radius filter, and every item sits under exactly one emoji-led arrangement
heading.

### 5. Place it

Read the PR body. Splice the section in and leave every other line alone. The description belongs to the user; this
skill never writes or rewrites it.

- No section yet: append it to the end of the body.
- Section already there: replace it from its `## Manual checks before merging` heading to the next `##` heading or the
  end of the body. Items that survive keep the box state they had. New items come in unchecked.
- No PR: print the section in chat.

When nothing survives the filter, say so and write nothing.

Done when the section appears exactly once in the body, every surviving item kept its box state, and every other line
of the body is byte-identical to what you read.
