# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.importing.domain import StepKind
from mpvqc.importing.enums import MpvqcImportWizardStepKind


def test_step_kind_covers_the_domain_enum() -> None:
    assert [(member.name, member.value) for member in MpvqcImportWizardStepKind.StepKind] == [
        (member.name, member.value) for member in StepKind
    ]
