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

The routing above the handlers went the same way. The filter used to copy all four fields of the message into a record
before anything looked at it, and most messages decide nothing: they belong to another window, or they are one of the
many the app does not answer. The same laziness holds one level up, with a struct field read in place of an OS call: the
probe is the Win32 message structure itself, the routing reads a field at a time, and a guard that returns early is a
field never read. Measured, reading and routing a message costs about a third less than it did, which is roughly 8% of
what answering a message costs end to end, and it halves the field reads per message. The eager version bought nothing
in exchange.

One probe per filter call, rebound to each message, is rejected. It looks like the obvious next step and it is not: it
recovers half of what making the probe be the message structure already recovers, for a mutable object and the
discipline to rebind it. It is also a trap. The filter is reentrant on Windows — setting a window style sends messages
back into it synchronously, and a handler blocked on a cross-process call has inbound sent messages dispatched to it —
so one shared probe is safe only while nothing reads it after a call that can pump. The routes that carry a message
parameter satisfy that today by where their reads land, not by construction, and a later change would reopen it with
nothing to catch it.

What the message path guarantees is narrower, and the narrow claim is the true one: nothing on it is written while a
message is being answered. The two window handles it reads are set when the window is wired up, the probe is fresh per
message, and the routes are frozen, so nested filter calls cannot alias one another. That is not the Windows backend
being reentrancy-safe. The fullscreen session handler keeps session state across calls that pump, and it already carries
its own answer: while a session is entering, the state read answers from the session's record and the abandonment check
holds off, so a half-entered window is not mistaken for one the OS took out of fullscreen.

The decisions live beside the platform-neutral window services rather than inside the Windows package, in a package of
their own. They import nothing platform-specific, so they load and are tested on any machine, and a fake probe that
records what it was asked turns the guard order itself into an assertion. Its name is a noun with a qualifier: the
decisions are what it holds, and Windows says only which decisions. A name whose noun is the platform would read as a
second Windows package, and merging two platform packages looks like tidying up rather than like the mistake below.

## Consequences

- The decisions move to a platform-neutral home and stay there. A future reader who files them back under the Windows
  package takes the tests down with them.
- A probe implementation is the only place a query can be reordered, hoisted, or cached, and doing any of that changes
  what the app asks the OS. The lazy contract is what the tests hold it to.
- Nothing on the message path is written while a message is being answered. Anything put there that outlives a single
  filter call has to answer for reentrancy before it goes in.
- The Win32 bindings keep the value types they construct. What crosses is the other way: the vocabulary the decisions
  own, taken by the bindings for typing only.
- The behaviour cannot be confirmed off Windows. The tests cover the arithmetic and the order of the questions; whether
  the frame still looks and resizes right is a run on a Windows machine.
