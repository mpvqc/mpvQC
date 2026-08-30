# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import uuid
from pathlib import Path
from typing import NamedTuple, assert_never
from zipfile import ZipFile

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, QThreadPool, QUrl, Slot
from PySide6.QtQml import QmlElement, QQmlContext, QQmlEngine, QQmlExpression

from mpvqc.appearance.services import (
    AccentColor,
    AppearanceSettingsService,
    NoPreference,
    format_color_scheme_preference,
    parse_color_scheme,
)
from mpvqc.appearance.viewmodels import MpvqcPaletteViewModel
from mpvqc.comments.services import CommentsService, CommentsSettingsService
from mpvqc.comments.viewmodels import MpvqcCommentLabelWidthCalculatorViewModel, MpvqcCommentTableTimeFormatViewModel
from mpvqc.exporting.services import ExportService, ExportSettingsService
from mpvqc.importing.services import (
    FinishedPlan,
    ImportSettingsService,
    PendingImport,
    SessionReplace,
    SubtitlesLoad,
    VideoLoad,
)
from mpvqc.importing.viewmodels import MpvqcImportWizardViewModel
from mpvqc.services import (
    ApplicationPathsService,
    DesktopService,
    SettingsService,
    StateService,
)
from mpvqc.shared import Comment
from mpvqc.window.viewmodels import MpvqcPlatformViewModel, MpvqcWindowControlsViewModel
from testqml import import_wizard_fixtures
from testqml.injections import (
    FIXTURES_DIR,
    TEMP_ROOT,
    TEMP_SAVES_DIR,
    RecordedPlayer,
    configure_injections,
    current_platform,
    rebind_main_window,
)

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


class _SwappedViewModel(NamedTuple):
    module_uri: str
    singleton_name: str
    property_name: str
    view_model_class: type[QObject]


_PLATFORM_VIEW_MODEL = _SwappedViewModel(
    "io.github.mpvqc.mpvQC.Utility",
    "MpvqcPlatform",
    "_viewModel",
    MpvqcPlatformViewModel,
)

# Singleton-held view models subscribe to service signals or snapshot service
# state when constructed, so resetState() swaps in fresh instances wired to the
# freshly configured services.
_SWAPPED_VIEW_MODELS = (
    _PLATFORM_VIEW_MODEL,
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcWindowUtility",
        "_viewModel",
        MpvqcWindowControlsViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcAppearance",
        "_viewModel",
        MpvqcPaletteViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcLabelWidthCalculator",
        "viewModel",
        MpvqcCommentLabelWidthCalculatorViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Views.Table",
        "MpvqcTableUtility",
        "viewModel",
        MpvqcCommentTableTimeFormatViewModel,
    ),
)


@QmlElement
class MpvqcTestBridge(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._wizard_outcome: dict = {"outcome": "none"}

    @Slot()
    def resetState(self) -> None:
        self._wizard_outcome = {"outcome": "none"}
        configure_injections()
        rebind_main_window()
        self._recreate_and_replace_singleton_view_models(_SWAPPED_VIEW_MODELS)

    @Slot(str)
    def switchPlatform(self, name: str) -> None:
        current_platform.switch(name)
        self._recreate_and_replace_singleton_view_models((_PLATFORM_VIEW_MODEL,))

    def _recreate_and_replace_singleton_view_models(self, entries: tuple[_SwappedViewModel, ...]) -> None:
        context = QQmlEngine.contextForObject(self)
        engine = context.engine()
        for entry in entries:
            singleton = engine.singletonInstance(entry.module_uri, entry.singleton_name)
            if not isinstance(singleton, QObject):
                msg = f"Cannot resolve singleton {entry.singleton_name}"
                raise TypeError(msg)
            previous = [child for child in singleton.children() if isinstance(child, entry.view_model_class)]
            view_model = entry.view_model_class()
            view_model.setParent(singleton)
            # Assign through a JS expression, not QQmlProperty.write: only a JS
            # assignment removes the property's declarative initializer. Left in
            # place, it re-fires when the previous view model is destroyed and
            # stomps the fresh one with null.
            swap_context = QQmlContext(engine.rootContext())
            swap_context.setContextProperty("__freshViewModel", view_model)
            expression = QQmlExpression(swap_context, singleton, f"{entry.property_name} = __freshViewModel")
            expression.evaluate()
            if expression.hasError():
                msg = f"Cannot swap {entry.property_name} on {entry.singleton_name}: {expression.error()}"
                raise RuntimeError(msg)
            for old in previous:
                old.deleteLater()

    @Slot()
    def resetComments(self) -> None:
        inject.instance(CommentsService).reset()

    @Slot(result=list)
    def comments(self) -> list:
        return [
            {"time": c.time, "commentType": c.comment_type, "comment": c.comment}
            for c in inject.instance(CommentsService).comments()
        ]

    @Slot(int, result=dict)
    def comment(self, index: int) -> dict:
        c = inject.instance(CommentsService).comment_at(index)
        return {"time": c.time, "commentType": c.comment_type, "comment": c.comment}

    @Slot(list)
    def importComments(self, comments: list) -> None:
        inject.instance(CommentsService).import_comments(
            [Comment(time=c["time"], comment_type=c["commentType"], comment=c["comment"]) for c in comments]
        )

    @Property(int, constant=True)
    def delayMs(self) -> int:
        return _DELAY_MS

    @Property(bool)
    def saved(self) -> bool:
        return inject.instance(StateService).saved

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
        # a job's result hops back to the GUI thread as one queued event, so one pass delivers it
        QCoreApplication.processEvents()

    @Slot(result=QUrl)
    def importComplexDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(_create_complex_qc_document()))

    @Slot(result=QUrl)
    def importVideoOnlyDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(_create_video_only_qc_document()))

    @Slot(result=list)
    def importMultiVideoDocuments(self) -> list[QUrl]:
        return [QUrl.fromLocalFile(str(p)) for p in _create_multi_video_qc_documents()]

    @Slot(dict)
    def loadVideo(self, values: dict) -> None:
        handle = inject.instance(RecordedPlayer).handle
        handle.load_video(values.get("path", "/videos/movie.mkv"))
        handle.update(
            duration=float(values.get("duration", 0.0)),
            time_pos=float(values.get("timePos", 0.0)),
            time_remaining=float(values.get("timeRemaining", 0.0)),
            percent_pos=float(values.get("percentPos", 0.0)),
        )

    @Slot(result=str)
    def openedVideoName(self) -> str:
        loaded = inject.instance(RecordedPlayer).handle.commands_named("loadfile")
        return Path(str(loaded[-1][1])).name if loaded else ""

    @Slot(result=int)
    def openedSubtitleCount(self) -> int:
        return len(self.openedSubtitleNames())

    @Slot(result=list)
    def openedSubtitleNames(self) -> list[str]:
        added = inject.instance(RecordedPlayer).handle.commands_named("sub-add")
        return [Path(str(command[1])).name for command in added]

    @Slot(result=list)
    def openedDesktopUrls(self) -> list[str]:
        urls = getattr(inject.instance(DesktopService), "opened_urls", ())
        return [url.toString() for url in urls]

    @Slot(result=int)
    def backupWriteCount(self) -> int:
        return getattr(inject.instance(ExportService), "write_count", 0)

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
        self._wizard_outcome = {"outcome": "none"}

        def on_finished(finished: FinishedPlan) -> None:
            self._wizard_outcome = {
                "outcome": "finished",
                "video": finished.video.path.name if isinstance(finished.video, VideoLoad) else "",
                "subtitles": [path.name for path in finished.subtitles.paths]
                if isinstance(finished.subtitles, SubtitlesLoad)
                else [],
                "replace": isinstance(finished.session, SessionReplace),
            }

        def on_dismissed() -> None:
            self._wizard_outcome = {"outcome": "dismissed"}

        pending = PendingImport(plan, on_finished=on_finished, on_dismissed=on_dismissed)
        return MpvqcImportWizardViewModel(self, pending)

    @Slot(result=dict)
    def wizardOutcome(self) -> dict:
        return self._wizard_outcome


@QmlElement
class MpvqcTestSettings(QObject):
    @Slot(result=bool)
    def backupEnabled(self) -> bool:
        return inject.instance(ExportSettingsService).backup_enabled

    @Slot(result=int)
    def backupInterval(self) -> int:
        return inject.instance(ExportSettingsService).backup_interval

    @Slot(result=str)
    def colorSchemePreference(self) -> str:
        return format_color_scheme_preference(inject.instance(AppearanceSettingsService).color_scheme_preference)

    @Slot(str, result=str)
    def accentColor(self, color_scheme: str) -> str:
        settings = inject.instance(AppearanceSettingsService)
        preference = settings.appearance_preference.accent_color_preference_for(parse_color_scheme(color_scheme))
        match preference:
            case NoPreference():
                return ""
            case AccentColor():
                return preference.identifier
            case _:
                assert_never(preference)

    @Slot(result=list)
    def commentTypes(self) -> list[str]:
        return list(inject.instance(CommentsSettingsService).comment_types)

    @Slot(result=int)
    def loadFoundVideo(self) -> int:
        return inject.instance(ImportSettingsService).import_found_video.value

    @Slot(result=str)
    def nickname(self) -> str:
        return inject.instance(ExportSettingsService).nickname

    @Slot(result=bool)
    def writeHeaderDate(self) -> bool:
        return inject.instance(ExportSettingsService).write_header_date

    @Slot(result=bool)
    def writeHeaderGenerator(self) -> bool:
        return inject.instance(ExportSettingsService).write_header_generator

    @Slot(result=bool)
    def writeHeaderNickname(self) -> bool:
        return inject.instance(ExportSettingsService).write_header_nickname

    @Slot(result=bool)
    def writeHeaderVideoPath(self) -> bool:
        return inject.instance(ExportSettingsService).write_header_video_path

    @Slot(result=bool)
    def writeHeaderSubtitles(self) -> bool:
        return inject.instance(ExportSettingsService).write_header_subtitles

    @Slot(result=int)
    def windowTitleFormat(self) -> int:
        return inject.instance(SettingsService).window_title_format

    @Slot(result=int)
    def layoutOrientation(self) -> int:
        return inject.instance(SettingsService).layout_orientation

    @Slot(result=str)
    def language(self) -> str:
        return inject.instance(SettingsService).language
