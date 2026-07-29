# Track modal overlay state centrally

Qt blocks the presses beneath a modal popup but keeps delivering hover events there. Everything below one keeps its
hover-driven feedback alive: cursor shapes, hover highlights, drag affordances, all promising input that the modal
popup will swallow. Anything that wants to be honest under a modal has to stand down by hand.

The search box solved this locally first. The comment list's popups reported their modality through a chain of
properties threaded across the view, and the search box read the far end of it. The chain could not see the
application's own dialogs and message boxes, so under those the search box kept offering its cursors and hover
highlights while clicks went nowhere. Every future modal source would have had to join the chain by hand, through
every layer in between.

Now one singleton counts open modal overlays and exposes a single flag: any modal overlay open. Each kind of modal
overlay reports in through a small declarative tracker object placed once in its base component, so dialogs, message
boxes and menus participate by inheritance, and the two one-offs, the time editor popup and the native file dialog
loader, carry their own. The tracker binds to open-and-modal, so non-modal menus and the inline comment editor stay
out. Whatever must stand down reads the flag; nothing is plumbed.

## Consequences

- A new dialog, message box or menu participates automatically. Nothing registers, nothing joins a chain.
- The count self-balances. A tracker releases when its overlay closes and when it is destroyed, so a loader tearing
  down an open overlay cannot leak the state. Tests that open overlays need no reset for the same reason.
- The flag only says when to stand down; standing down stays per consumer, because Qt delivers the hover regardless.
  The search box drops its cursor claims, hover feedback and drag while the flag is up.
- Message boxes now declare themselves modal explicitly. The Material style already defaults dialogs to modal, but the
  input blocking the app relies on must not hang on a style default.
