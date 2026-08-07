# Import wizard redesign prototype (internal ticket #114)

Throwaway. The surviving direction for the import wizard redesign: resolved concerns ("what will
definitely be imported") shown alongside the questions, oriented on the appearance dialog's
section cards.

## Run

```
uv run .scratch/import-wizard-prototype/run.py
```

Needs `testqml/project.rcc` (`just prepare-tests` once). Uses the QML test harness injections, so
no mpv and no real settings.

## Controls

- `←` / `→` or the floating bar: cycle variants
- `S` or the scenario button: cycle data scenarios (every question open / one question left /
  many candidates / errors only)
- Dark/Light button: toggle the theme (drives the real appearance view model)

## The winner: C — Steps + summary

One open question per page. Fixed chrome on every page: a clickable Material pager (active dot
stretches to a pill, tooltips name the pages) with the page name beneath it, so all pages start
at the same coordinates. One persistent section card hosts the question pages: content swaps
atomically (no frame ever blends two pages) and the card animates its height - the moving
edge reveals or swallows content like a wipe (slide, fade-through, fade-over, sequential
fade, instant swap, and crossfade were all tried and rejected). Delegates share one fixed row
height and question headers a fixed two-line height across all three lists, so page heights
differ only by row count. The summary shares the same motion: the sweeping edge unveils its
four individual section cards. Overflowing pages show no scrollbar: gradient scrims at the top
and bottom edges let content dissolve into the background to signal more in that direction.
The final
summary lists the whole plan plainly: chosen answers, in-plan resolved imports, and skipped
files with their reasons - no actions, no trailing labels; the dots are the way back. Video
candidate rows show origin pills (from document / from subtitle) and full-path tooltips, the
tri-state "Select all" sits on the subtitles question line, questions render in foreground with
a fixed 32px question line, radios and checks are custom Material 3 Expressive indicators, and
long candidate lists scroll within the page with a reserved scrollbar lane and no overshoot.
The dialog size is static (640 content height): on Windows it is a native popup window that
cannot resize.

## Rejected

- Accordion checklist (sections expand/collapse as you answer, `VariantChecklist.qml`, out of
  rotation): too smartphone-like, desktop users don't want to click through.
- Dense desktop form (label column plus inline controls, `VariantForm.qml`, out of rotation):
  worst of the bunch by a big margin.
- Sentence-first confirm (`VariantSentence.qml`), side rail plan (`VariantSideRail.qml`), and
  editable facts (`VariantEditableFacts.qml`): explored, not liked, out of rotation.
- Overview, one page (`VariantOverview.qml`) and digest + questions (`VariantDigest.qml`):
  carried to the end, dropped in favor of C.
