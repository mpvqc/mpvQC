# Drive the Windows frame decisions through read-only probes

The native event filter of ADR 0004 answers two messages, and both answers are arithmetic: which part of the frame the
cursor is over, and how large the client area should be. Neither needs Windows to compute. Both used to need Windows to
run, because they reached the OS through an import that fails outside it, so none of them had a test on any platform.

Fetching every fact before the arithmetic starts does not fix that. The taskbar queries are cross-process, and gathering
them up front would put them on the ordinary windowed resize, a path that makes none today. The two handlers cannot
share one bundle of facts either: their message parameter means different things, a packed cursor point for one and a
pointer to a size structure for the other, and they resolve their monitor from different rectangles, since a window
crossing monitors gets a proposed rectangle on the new monitor while its current rectangle still reports the old one.

So each handler takes a probe instead: a small read-only port holding exactly the queries that handler makes, in the
order it makes them. A probe answers when it is asked and not before, so every guard and every early return the handler
already had is an OS call that never happens, and the Win32 call sequence stays what it was by construction rather than
by discipline. The handlers also stop writing. Each returns what it decided, and the event filter performs the one write
the frame needs, which is what keeps both ports read-only.

The decisions live beside the platform-neutral window services rather than inside the Windows package. They import
nothing platform-specific, so they load and are tested on any machine, and a fake probe that records what it was asked
turns the guard order itself into an assertion.

## Consequences

- The decisions move to a platform-neutral home and stay there. A future reader who files them back under the Windows
  package takes the tests down with them.
- A probe implementation is the only place a query can be reordered, hoisted, or cached, and doing any of that changes
  what the app asks the OS. The lazy contract is what the tests hold it to.
- The Win32 bindings keep the value types they construct. What crosses is the other way: the vocabulary the decisions
  own, taken by the bindings for typing only.
- The behaviour cannot be confirmed off Windows. The tests cover the arithmetic and the order of the questions; whether
  the frame still looks and resizes right is a run on a Windows machine.
