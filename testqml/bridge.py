# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import uuid
from pathlib import Path

import inject
from PySide6.QtCore import Property, QObject, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import DesktopService, PlayerService, StateService
from testqml.injections import FIXTURES_DIR, TEMP_ROOT, TEMP_SAVES_DIR, configure_injections

QML_IMPORT_NAME = "pyobjects"
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


@QmlElement
class MpvqcTestBridge(QObject):
    @Slot()
    def resetState(self) -> None:
        configure_injections()

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

    @Slot(result=str)
    def openedVideoName(self) -> str:
        opened = getattr(inject.instance(PlayerService), "opened_video", None)
        return opened.name if opened else ""

    @Slot(result=int)
    def openedSubtitleCount(self) -> int:
        return len(getattr(inject.instance(PlayerService), "opened_subtitles", ()))

    @Slot(result=list)
    def openedDesktopUrls(self) -> list[str]:
        urls = getattr(inject.instance(DesktopService), "opened_urls", ())
        return [url.toString() for url in urls]
