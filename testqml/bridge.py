# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from pathlib import Path
from typing import assert_never

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement, QQmlEngine

from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.appearance.services import (
    AccentColor,
    AppearanceSettingsService,
    NoPreference,
    format_color_scheme_preference,
    parse_color_scheme,
)
from mpvqc.comments.services import CommentsService, CommentsSettingsService
from mpvqc.exporting.services import ExportService, ExportSettingsService
from mpvqc.i18n.services import I18nSettingsService
from mpvqc.importing.services import (
    FinishedPlan,
    ImportSettingsService,
    PendingImport,
    SessionReplace,
    SubtitlesLoad,
    VideoLoad,
)
from mpvqc.importing.viewmodels import MpvqcImportWizardViewModel
from mpvqc.session import SessionService
from mpvqc.shared import Comment
from mpvqc.shell.services import DesktopService, ShellSettingsService
from testqml import artifacts, import_wizard_fixtures, runtime
from testqml.injections import DesktopServiceOverride, RecordedPlayer

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

_DELAY_MS = int(os.environ.get("MPVQC_TEST_DELAY_MS", "100"))


@QmlElement
class MpvqcTestBridge(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._wizard_outcome: dict = {"outcome": "none"}

    @Slot()
    def resetState(self) -> None:
        self._wizard_outcome = {"outcome": "none"}
        # Keep the context wrapper alive through the call; inlining the lookup invalidates the engine.
        context = QQmlEngine.contextForObject(self)
        runtime.reset_state(context.engine())

    @Slot(str)
    def switchPlatform(self, name: str) -> None:
        context = QQmlEngine.contextForObject(self)
        runtime.switch_platform(context.engine(), name)

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
        return inject.instance(SessionService).saved

    @Slot(str, result=QUrl)
    def importArtifact(self, name: str) -> QUrl:
        return QUrl.fromLocalFile(str(artifacts.FIXTURES_DIR / name))

    @Slot(result=QUrl)
    def tempSavePath(self) -> QUrl:
        return QUrl.fromLocalFile(str(artifacts.temp_save_path()))

    @Slot(QUrl, str, result=bool)
    def fileContains(self, url: QUrl, text: str) -> bool:
        return artifacts.file_contains(Path(url.toLocalFile()), text)

    @Slot()
    def waitForBackgroundJobs(self) -> None:
        runtime.wait_for_background_jobs()

    @Slot(result=QUrl)
    def importComplexDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(artifacts.create_complex_qc_document()))

    @Slot(result=QUrl)
    def importVideoOnlyDocument(self) -> QUrl:
        return QUrl.fromLocalFile(str(artifacts.create_video_only_qc_document()))

    @Slot(result=list)
    def importMultiVideoDocuments(self) -> list[QUrl]:
        return [QUrl.fromLocalFile(str(p)) for p in artifacts.create_multi_video_qc_documents()]

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
        desktop = inject.instance(DesktopService)
        if not isinstance(desktop, DesktopServiceOverride):
            msg = "Desktop URL recording requires DesktopServiceOverride"
            raise TypeError(msg)
        return [url.toString() for url in desktop.opened_urls]

    @Slot(result=QUrl)
    def appDataFolderUrl(self) -> QUrl:
        return QUrl.fromLocalFile(str(inject.instance(ApplicationPathsService).dir_config))

    @Slot(result=QUrl)
    def backupFolderUrl(self) -> QUrl:
        return QUrl.fromLocalFile(str(inject.instance(ApplicationPathsService).dir_backup))

    @Slot(result=int)
    def backupWriteCount(self) -> int:
        return getattr(inject.instance(ExportService), "write_count", 0)

    @Slot(str, result=bool)
    def backupArchiveAnyEntryContains(self, text: str) -> bool:
        backup_dir = inject.instance(ApplicationPathsService).dir_backup
        return artifacts.backup_archive_any_entry_contains(backup_dir, text)

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
        return inject.instance(ShellSettingsService).window_title_format.value

    @Slot(result=int)
    def layoutOrientation(self) -> int:
        return inject.instance(ShellSettingsService).layout_orientation

    @Slot(result=str)
    def language(self) -> str:
        return inject.instance(I18nSettingsService).language
