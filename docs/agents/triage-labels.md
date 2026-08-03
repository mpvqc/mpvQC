# Triage Labels

The skills speak in terms of canonical triage roles. This file maps those roles to the label strings that actually
exist, on each of the two trackers. When a skill mentions a role ("apply the AFK-ready triage label"), look the string
up here first — several of the roles have no label behind them.

## `mpvqc/mpvQC` (public tracker)

Triage happens here. Only two of the five canonical labels exist today:

| Canonical role    | On this tracker  | Meaning                                  |
| ----------------- | ---------------- | ---------------------------------------- |
| `needs-triage`    | `needs-triage`   | Maintainer needs to evaluate this issue  |
| `wontfix`         | `wontfix`        | Will not be actioned                     |
| `needs-info`      | does not exist   | Waiting on reporter for more information |
| `ready-for-agent` | does not exist   | Fully specified, ready for an AFK agent  |
| `ready-for-human` | does not exist   | Requires a human, not an agent           |

`gh issue edit --add-label` fails on a label that does not exist. When one of the last three is genuinely the right
outcome, create it first with `gh label create <name> --description "..."` and say that you did.

## `mpvqc/internal-tickets` (private tracker)

Three labels, and no others. The twelve inherited from the public repo were deleted on purpose: a label nobody filters
on is noise.

| Label             | Meaning                                                |
| ----------------- | ------------------------------------------------------ |
| `ready-for-agent` | Specified enough for an agent to take unattended       |
| `ready-for-human` | Requires a human, not an agent                         |
| `needs-grilling`  | Accepted finding, not yet broken down into tickets     |

`needs-grilling` is internal only — it describes work that has not been shaped yet, which is never a state a user
report is in.

Which of these a ticket gets, and when a ticket gets none, is the `filing-tickets` skill's call.

There are no area labels and no issue types on either tracker. Issue types are disabled org-wide and stay that way.
