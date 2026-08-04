# Triage Labels

The skills speak in terms of triage roles. This file maps them to the label strings on each of the two trackers.
Neither tracker uses area labels or issue types.

## `mpvqc/mpvQC` (public tracker)

Triage happens here. `gh label list --repo mpvqc/mpvQC` shows which of these exist today.

| Role              | Meaning                                  |
| ----------------- | ---------------------------------------- |
| `needs-triage`    | Maintainer needs to evaluate this issue  |
| `wontfix`         | Will not be actioned                     |
| `needs-info`      | Waiting on reporter for more information |
| `ready-for-agent` | An agent can take it unattended          |
| `ready-for-human` | Requires a human, not an agent           |

`gh issue edit --add-label` fails on a label that does not exist. When `needs-info`, `ready-for-agent`, or
`ready-for-human` is genuinely the right outcome, create it first with
`gh label create <name> --repo mpvqc/mpvQC --description "..."` and tell the user.

## `mpvqc/internal-tickets` (private tracker)

`gh label list --repo mpvqc/internal-tickets` shows which of these exist today, and every other `gh` call against this
tracker needs the same `--repo`. Which label a ticket gets is the `filing-tickets` skill's call.

| Label             | Meaning                                                                              |
| ----------------- | ------------------------------------------------------------------------------------ |
| `ready-for-agent` | An agent can take it unattended                                                      |
| `ready-for-human` | Requires a human, not an agent                                                       |
| `needs-grilling`  | Qualifier alongside a readiness label: accepted finding, not yet broken down          |
