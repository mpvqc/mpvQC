---
name: load-bearing-comments
description: Load-bearing comments and restatements. Use when reviewing code or a diff, when adding or trimming a comment or docstring, or when another skill needs the test for whether a comment earns its keep.
---

# Load-bearing comments

Good code needs few comments. A comment is load-bearing when it says something the code cannot say and nothing else
already records. The rest are restatements: they cost a read, and they go stale the moment someone changes the code
and not the text.

Be strict. Most comments do not survive this.

## The test

Both halves have to pass, or the comment goes:

1. **Could the code say it?** A name, a type, a match arm, a test.
2. **Is it already written down?** `CONTEXT.md` defines the domain terms. `docs/adr/` holds the decisions and their
   why. Read both before ruling on a comment, not just the one you remember.

## Move it rather than keep it

| What the comment holds       | Where it belongs |
| ---------------------------- | ---------------- |
| A domain term                | `CONTEXT.md`     |
| A decision and its reasoning | an ADR           |
| Behaviour                    | a test           |
| What a name should have said | the name         |

## What stays

- An invariant a reader cannot check from where they stand: the order of a tuple that some other file indexes into.
- A fact from outside the repo: Qt's `setColorScheme` ignores the system from then on.
- A choice nothing derives: Dark is mpvQC's historic default.
- A guard on an edit that looks safe and is not: this `__init__` stays empty or the imports cycle.
- Why an opaque shape was picked: `Signal(object)`, because Qt signals cannot carry type aliases.

Site it at the trap. The comment sits on the line someone is about to change, not in a header far from it.

## How a restatement reads

- It repeats the name or the signature. "Read a color scheme off a boundary" over `parse_color_scheme`.
- It narrates the branch the code right below it already takes.
- It copies a glossary entry or a sentence from an ADR.
- It says what a comment at the consumer already says. Two copies in two languages drift apart.
- It labels a section the file's own structure already marks: a `# region` or `// ---` banner.
- It is a docstring on a marker type whose name is the whole meaning.

A docstring that was the entire class body leaves `pass` behind. No pydocstyle rules run here, so that is fine.

## Verify the claim before keeping it

A comment that asserts something — "the only place X happens", "callers always Y" — is worth keeping only while it
is true. Grep it and confirm. A false comment is worse than no comment, because it is the one a reader believes.

## Done when

- Every comment still standing passed both halves of the test.
- The claims they make were checked against the code, not assumed.
- Whatever moved out landed in `CONTEXT.md`, an ADR, a test, or a better name.
