# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QUrl

from mpvqc.exporting.services import ExportService, ExportSettingsService
from mpvqc.exporting.viewmodels import MpvqcExportFileDialogViewModel
from mpvqc.player.services import PlayerService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, player_service, export_settings_service, manual_executor):
    exporter = ExportService(manual_executor)

    def bindings(binder: inject.Binder):
        binder.bind(ExportService, exporter)
        binder.bind(ExportSettingsService, export_settings_service)
        binder.bind(PlayerService, player_service)

    common_bindings_with(bindings)


@pytest.fixture
def view_model(tmp_path, player_handle, export_settings_service) -> MpvqcExportFileDialogViewModel:
    player_handle.load_video(str(tmp_path / "first.mkv"))
    export_settings_service.nickname = "alice"
    return MpvqcExportFileDialogViewModel()


def test_proposals_capture_state_before_first_read(tmp_path, player_handle, export_settings_service, view_model):
    player_handle.load_video(str(tmp_path / "second.mkv"))
    export_settings_service.nickname = "bob"

    assert view_model.filenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.json"))
    assert view_model.classicFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.txt"))
    assert view_model.customFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.txt"))


def test_proposals_stay_stable_after_first_read(tmp_path, player_handle, export_settings_service, view_model):
    original_json = QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.json"))
    original_txt = QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.txt"))
    assert view_model.filenameProposal == original_json
    assert view_model.classicFilenameProposal == original_txt
    assert view_model.customFilenameProposal == original_txt

    player_handle.load_video(str(tmp_path / "second.mkv"))
    export_settings_service.nickname = "bob"

    assert view_model.filenameProposal == original_json
    assert view_model.classicFilenameProposal == original_txt
    assert view_model.customFilenameProposal == original_txt


def test_new_instance_captures_current_state(tmp_path, player_handle, export_settings_service, view_model):
    assert view_model.filenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.json"))
    assert view_model.classicFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.txt"))
    assert view_model.customFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_first_alice.txt"))

    player_handle.load_video(str(tmp_path / "second.mkv"))
    export_settings_service.nickname = "bob"

    reopened = MpvqcExportFileDialogViewModel()
    assert reopened.filenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_second_bob.json"))
    assert reopened.classicFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_second_bob.txt"))
    assert reopened.customFilenameProposal == QUrl.fromLocalFile(str(tmp_path / "[QC]_second_bob.txt"))
