# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import uuid
from pathlib import Path
from zipfile import ZipFile

import inject
from PySide6.QtCore import Property, QObject, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.dialogs.import_wizard import MpvqcImportWizardViewModel
from mpvqc.services import (
    ApplicationPathsService,
    DesktopService,
    DocumentBackupService,
    PlayerService,
    SettingsService,
    StateService,
)
from testqml import import_wizard_fixtures
from testqml.injections import FIXTURES_DIR, TEMP_ROOT, TEMP_SAVES_DIR, configure_injections, rebind_main_window

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

_DELAY_MS = int(os.environ.get("MPVQC_TEST_DELAY_MS", "100"))


def _create_complex_qc_document() -> Path:
    base = TEMP_ROOT / f"complex-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video = base / "video.mp4"
    sub1 = base / "track1.ass"
    sub2 = base / "track2.ass"
    for f in (video, sub1, sub2):
        f.touch()
    doc = base / "qc-complex.txt"
    doc.write_text(
        "[FILE]\n"
        f"path     : {video}\n"
        f"subtitle : {sub1}\n"
        f"subtitle : {sub2}\n"
        "\n"
        "[DATA]\n"
        "[00:00:10] [Translation] line1\n"
        "[00:01:20] [Spelling] line2\n",
        encoding="utf-8",
    )
    return doc


def _create_video_only_qc_document() -> Path:
    base = TEMP_ROOT / f"video-only-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video = base / "video_only.mp4"
    video.touch()
    doc = base / "qc-video-only.txt"
    doc.write_text(
        f"[FILE]\npath     : {video}\n\n[DATA]\n[00:00:10] [Translation] line1\n",
        encoding="utf-8",
    )
    return doc


def _create_multi_video_qc_documents() -> tuple[Path, Path]:
    base = TEMP_ROOT / f"multi-video-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video_a = base / "alpha.mp4"
    video_b = base / "beta.mp4"
    for f in (video_a, video_b):
        f.touch()
    doc_a = base / "qc-alpha.txt"
    doc_a.write_text(
        f"[FILE]\npath     : {video_a}\n\n[DATA]\n[00:00:10] [Translation] line1\n",
        encoding="utf-8",
    )
    doc_b = base / "qc-beta.txt"
    doc_b.write_text(
        f"[FILE]\npath     : {video_b}\n\n[DATA]\n[00:00:20] [Spelling] line2\n",
        encoding="utf-8",
    )
    return doc_a, doc_b


@QmlElement
class MpvqcTestBridge(QObject):
    @Slot()
    def resetState(self) -> None:
        configure_injections()
        rebind_main_window()

    @Property(int, constant=True)
    def delayMs(self) -> int:
        return _DELAY_MS

    @Property(bool)
    def saved(self) -> bool:
        return bool(inject.instance(StateService).saved)

    @Slot(str, result=QUrl)
    def importArtifact(self, name: str) -> QUrl:
        return QUrl.fromLocalFile(str(FIXTURES_DIR / name))

    @Slot(result=QUrl)
    def tempSavePath(self) -> QUrl:
        name = f"qc_document_{uuid.uuid4().hex[:8]}.txt"
        return QUrl.fromLocalFile(str(TEMP_SAVES_DIR / name))

    @Slot(QUrl, str, result=bool)
    def fileContains(self, url: QUrl, text: str) -> bool:
        path = Path(url.toLocalFile())
        return path.is_file() and text in path.read_text(encoding="utf-8")

    @Slot()
    def waitForBackgroundJobs(self) -> None:
        QThreadPool.globalInstance().waitForDone()

    @Slot(result=QUrl)
    def importComplexDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(_create_complex_qc_document()))

    @Slot(result=QUrl)
    def importVideoOnlyDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(_create_video_only_qc_document()))

    @Slot(result=list)
    def importMultiVideoDocuments(self) -> list[QUrl]:
        return [QUrl.fromLocalFile(str(p)) for p in _create_multi_video_qc_documents()]

    @Slot(result=str)
    def openedVideoName(self) -> str:
        opened = getattr(inject.instance(PlayerService), "opened_video", None)
        return opened.name if opened else ""

    @Slot(result=int)
    def openedSubtitleCount(self) -> int:
        return len(getattr(inject.instance(PlayerService), "opened_subtitles", ()))

    @Slot(result=list)
    def openedSubtitleNames(self) -> list[str]:
        subtitles = getattr(inject.instance(PlayerService), "opened_subtitles", ())
        return [s.name for s in subtitles]

    @Slot(result=list)
    def openedDesktopUrls(self) -> list[str]:
        urls = getattr(inject.instance(DesktopService), "opened_urls", ())
        return [url.toString() for url in urls]

    @Slot(result=int)
    def backupWriteCount(self) -> int:
        return getattr(inject.instance(DocumentBackupService), "write_count", 0)

    @Slot(str, result=bool)
    def backupArchiveAnyEntryContains(self, text: str) -> bool:
        backup_dir = inject.instance(ApplicationPathsService).dir_backup
        if not backup_dir.is_dir():
            return False
        for archive in backup_dir.glob("*.zip"):
            with ZipFile(archive) as zf:
                for name in zf.namelist():
                    if text in zf.read(name).decode("utf-8", errors="replace"):
                        return True
        return False

    @Slot(result=QUrl)
    def mpvConfPath(self) -> QUrl:
        return QUrl.fromLocalFile(str(inject.instance(ApplicationPathsService).file_mpv_conf))

    @Slot(result=QUrl)
    def inputConfPath(self) -> QUrl:
        return QUrl.fromLocalFile(str(inject.instance(ApplicationPathsService).file_input_conf))

    @Slot(str, result=MpvqcImportWizardViewModel)
    def buildWizardViewModel(self, scenario: str) -> MpvqcImportWizardViewModel:
        plan = import_wizard_fixtures.build(scenario)
        return MpvqcImportWizardViewModel(self, plan)


@QmlElement
class MpvqcTestSettings(QObject):
    @Slot(result=bool)
    def backupEnabled(self) -> bool:
        return inject.instance(SettingsService).backup_enabled

    @Slot(result=int)
    def backupInterval(self) -> int:
        return inject.instance(SettingsService).backup_interval

    @Slot(result=str)
    def themeIdentifier(self) -> str:
        return inject.instance(SettingsService).theme_identifier

    @Slot(result=str)
    def primaryColor(self) -> str:
        return inject.instance(SettingsService).primary_color

    @Slot(result=list)
    def commentTypes(self) -> list[str]:
        return list(inject.instance(SettingsService).comment_types)

    @Slot(result=int)
    def importFoundVideo(self) -> int:
        return inject.instance(SettingsService).import_found_video

    @Slot(result=str)
    def nickname(self) -> str:
        return inject.instance(SettingsService).nickname

    @Slot(result=bool)
    def writeHeaderDate(self) -> bool:
        return inject.instance(SettingsService).write_header_date

    @Slot(result=bool)
    def writeHeaderGenerator(self) -> bool:
        return inject.instance(SettingsService).write_header_generator

    @Slot(result=bool)
    def writeHeaderNickname(self) -> bool:
        return inject.instance(SettingsService).write_header_nickname

    @Slot(result=bool)
    def writeHeaderVideoPath(self) -> bool:
        return inject.instance(SettingsService).write_header_video_path

    @Slot(result=bool)
    def writeHeaderSubtitles(self) -> bool:
        return inject.instance(SettingsService).write_header_subtitles

    @Slot(result=int)
    def windowTitleFormat(self) -> int:
        return inject.instance(SettingsService).window_title_format

    @Slot(result=int)
    def layoutOrientation(self) -> int:
        return inject.instance(SettingsService).layout_orientation

    @Slot(result=str)
    def language(self) -> str:
        return inject.instance(SettingsService).language
