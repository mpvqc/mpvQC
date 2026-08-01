---
name: writing-glossary
description: Glossary entries in CONTEXT.md. Use when adding, changing, or reviewing a domain term in this repo.
---

# Writing glossary entries

An entry answers one question: what is this thing? A reader who has never opened the code comes away able to
recognise the term in the wild, and to tell it from its neighbours.

## The concept, nothing else

A term outlives the implementation it was coined for, and the entry has to survive it too. So write what the term
means and stop.

The test: would this sentence change if the code changed while the concept stayed the same? Then it is
implementation, and it belongs in the code and its tests, where it can be checked. Counts of what ships today,
tie-breaks, defaults, what an entity carries, file formats, lookup keys — implementation, all of it.

## Define positively

Say what the term is, in one or two sentences, in plain words.

- **Straw terms**: "Family, not set" argues with a name the reader never had. Contrast only if absolutely necessary
  with another entry in the file, where a reader can genuinely mix the two up: "A request, not a result."
- **Circles**: "the color choice that selects the colored variant of what it colors" restates the term. Reach instead
  for what the thing is made of, or what it decides.
- **Wit**: "A key, not a promise" reads well and defines nothing.

## Borrow only defined words

Every noun in an entry is plain English or another term in the file. A compound invented while writing the entry —
"accent palette", "one design" — is a new term you now owe a definition; use an existing one instead.

Where a word has stages, name the stage: "one effective color scheme", never a bare "color scheme".

## Done when

- A reader who does not know this codebase can say what the term means and when it applies.
- Every word in the entry is plain English or another entry in the file.
- Nothing in the entry would change if the implementation changed and the concept did not.
