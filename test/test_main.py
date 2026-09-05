# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from main import print_version


def test_version_flag_prints_name_and_version_label(capsys, monkeypatch, make_build_info):
    info = make_build_info(version="1.0.0", is_release=True, origin="mpvqc-github")
    monkeypatch.setattr("mpvqc.build.get_build_info", lambda: info)

    print_version()

    assert capsys.readouterr().out == "mpvQC 1.0.0 (abc12345) mpvqc-github\n"
