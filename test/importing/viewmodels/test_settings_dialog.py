# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.importing.services import ImportSettingsService, LoadFoundVideo
from mpvqc.importing.viewmodels import MpvqcImportSettingsDialogViewModel


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, import_settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ImportSettingsService, import_settings_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcImportSettingsDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcImportSettingsDialogViewModel()


def test_options_offer_every_load_found_video_setting(view_model):
    assert [option["value"] for option in view_model.options] == [setting.value for setting in LoadFoundVideo]


def test_options_label_every_setting(view_model):
    assert [option["text"] for option in view_model.options] == ["Always", "Ask every time", "Never"]


def test_load_found_video_starts_at_the_stored_setting(import_settings_service):
    import_settings_service.import_found_video = LoadFoundVideo.NEVER

    # noinspection PyCallingNonCallable
    assert MpvqcImportSettingsDialogViewModel().loadFoundVideo == LoadFoundVideo.NEVER.value


def test_a_staged_change_leaves_the_service_untouched(view_model, import_settings_service):
    view_model.loadFoundVideo = LoadFoundVideo.NEVER.value

    assert view_model.loadFoundVideo == LoadFoundVideo.NEVER.value
    assert import_settings_service.import_found_video == LoadFoundVideo.ASK_EVERY_TIME


def test_accept_persists_the_staged_change(view_model, import_settings_service):
    view_model.loadFoundVideo = LoadFoundVideo.NEVER.value

    view_model.accept()

    assert import_settings_service.import_found_video == LoadFoundVideo.NEVER


def test_a_staged_change_notifies_once(view_model, make_spy):
    spy = make_spy(view_model.loadFoundVideoChanged)

    view_model.loadFoundVideo = LoadFoundVideo.NEVER.value

    assert spy.count() == 1
    assert spy.at(0, 0) == LoadFoundVideo.NEVER.value

    view_model.loadFoundVideo = LoadFoundVideo.NEVER.value
    assert spy.count() == 1


def test_an_unknown_setting_raises(view_model):
    with pytest.raises(ValueError, match="42"):
        view_model.loadFoundVideo = 42
