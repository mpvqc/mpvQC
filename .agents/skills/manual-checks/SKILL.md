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

The fork call places every item: an item stays shared when one run on any arrangement vouches for every arrangement
it reaches, and it forks when arrangements owe the user different behaviour, or when a pass on one machine says
nothing about another because the failure is platform-flavoured: fonts, compositors, native modules.

- A shared item is written once, under the `### 🌐 Anywhere` heading: the user checks it on whichever machine they
  sit at, and that one tick vouches for the rest. When its reach is narrower than every arrangement, the item names
  it: `On Linux, …`.
- A forked item is written once per arrangement it reaches, under that arrangement's heading, each copy stating what
  its arrangement owes — never one shared line with parentheticals bolted on.

Group each heading by area, and skip an arrangement no subagent reached: a Linux-only branch gets no Windows heading.

Lead every heading with its emoji, so the user finds their machine by shape before they read a word: 🌐 Anywhere,
🪟 Windows, 🐧 Linux desktop, 🧱 Linux tiling. An arrangement the catalogue grows later picks up its own emoji and
keeps it from then on.

Name an area after the thing the user touches: `Window controls`, `Video resize`, `Overlays`. Not after the module.

Write each item as the state that should hold, present tense, one observable per line:

```markdown
## Manual checks before merging

### 🌐 Anywhere

#### Overlays

- [ ] The search overlay opens above the table

### 🪟 Windows

#### Window controls

- [ ] Loading a video resizes the window to fit it

### 🧱 Linux tiling

#### Window controls

- [ ] Known and accepted: loading a video leaves the window alone, the compositor decides the size
```

The overlay is written once: its layout owes nothing to the platform, so one run on any machine vouches for all.
Resize forks, written twice and differently, because the two arrangements owe different behaviour.

Every line under a heading is a checkbox. Setup a check needs rides inside the item. A quirk the branch knowingly
leaves behind is still an item, marked `Known and accepted:`.

Boxes ship unchecked. The user ticks them.

Done when every item passes the blast radius filter and sits where the fork call puts it: shared items once under
🌐, forked items once per arrangement, and no behaviour written both shared and forked.

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
