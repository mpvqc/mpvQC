// PROTOTYPE - Variant C "Steps + summary": one open question per page. Fixed chrome on every
// page: a clickable Material pager (active dot stretches to a pill, tooltips name the pages)
// plus the page name beneath it. A clipped page area hosts every page: on navigation the
// content swaps atomically (no frame ever blends two pages) and the area's edge sweeps to the
// new height, revealing or swallowing content - between questions that morphs the single card,
// and into the summary it unveils the four section cards listing the whole plan: chosen
// answers, in-plan resolved imports, and skipped files with their reasons; the dots are the
// way back. With nothing to ask, the summary is the only page.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root

    required property var plan

    property bool rtlPreview: false

    property bool replaceComments: false
    property int videoChoice: 0
    property var subtitleChoices: root.plan.subtitles.candidates.map(() => true)

    property int pageIndex: 0
    property string _shownPage: root.pages[0]
    property string _questionPage: root.pages[0] === "review" ? "" : root.pages[0]

    readonly property var pages: {
        const result = [];
        if (!root.plan.session.resolved) {
            result.push("session");
        }
        if (!root.plan.video.resolved) {
            result.push("video");
        }
        if (!root.plan.subtitles.resolved) {
            result.push("subtitles");
        }
        result.push("review");
        return result;
    }

    readonly property string currentPage: root.pages[root.pageIndex] ?? "review"
    readonly property bool onReview: root.currentPage === "review"

    readonly property bool closeOnly: root.plan.commentCount === 0
        && root.plan.video.load === "" && root.plan.video.candidates.length === 0
        && root.plan.subtitles.load.length === 0 && root.plan.subtitles.candidates.length === 0

    readonly property var selectedSubtitles: root.plan.subtitles.resolved
        ? root.plan.subtitles.load
        : root.plan.subtitles.candidates.filter((_, index) => root.subtitleChoices[index])

    readonly property int _sectionSpacing: 12

    function pageTitle(page: string): string {
        switch (page) {
        case "session":
            return root.plan.commentCount === 1 ? "Comment" : "Comments";
        case "video":
            return "Video";
        case "subtitles":
            return root.plan.subtitles.candidates.length === 1 ? "Subtitle" : "Subtitles";
        }
        return "Summary";
    }

    function _componentFor(page: string): Component {
        switch (page) {
        case "session":
            return _sessionContent;
        case "video":
            return _videoContent;
        case "subtitles":
            return _subtitlesContent;
        }
        return _reviewContent;
    }

    function goTo(index: int): void {
        if (index < 0 || index >= root.pages.length || index === root.pageIndex) {
            return;
        }
        root.pageIndex = index;
        root._shownPage = root.currentPage;
        if (root.currentPage !== "review") {
            root._questionPage = root.currentPage;
        }
        _pageScroll.scrollToTop();
    }

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    function toggleAllSubtitles(): void {
        const all = root.selectedSubtitles.length === root.plan.subtitles.candidates.length;
        root.subtitleChoices = root.plan.subtitles.candidates.map(() => !all);
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth

    // Static: on Windows the dialog is a native popup window that cannot resize. Sized so a
    // typical summary (all decisions plus three subtitles and a skipped file) fits unscrolled.
    contentHeight: 640

    contentItem: ColumnLayout {
        spacing: 20

        ColumnLayout {
            id: _chrome

            spacing: 20
            visible: root.pages.length > 1

            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 24

            Row {
                spacing: 0

                Layout.alignment: Qt.AlignHCenter

                Repeater {
                    model: root.pages.length

                    delegate: AbstractButton {
                        id: _dot

                        required property int index

                        readonly property bool isCurrent: _dot.index === root.pageIndex
                        readonly property bool isDone: _dot.index < root.pageIndex

                        width: 32
                        height: 28
                        hoverEnabled: true

                        ToolTip.text: root.pageTitle(root.pages[_dot.index])
                        ToolTip.visible: _dot.hovered
                        ToolTip.delay: MpvqcConstants.tooltipDelay

                        onClicked: root.goTo(_dot.index)

                        HoverHandler {
                            cursorShape: _dot.isCurrent ? Qt.ArrowCursor : Qt.PointingHandCursor
                        }

                        Rectangle {
                            id: _indicator

                            anchors.centerIn: parent

                            width: _dot.isCurrent ? 24 : 10
                            height: 10
                            radius: 5
                            color: _dot.isCurrent ? MpvqcAppearance.palette.accent
                                : _dot.isDone ? Qt.alpha(MpvqcAppearance.palette.foreground, _dot.hovered ? 0.65 : 0.45)
                                : Qt.alpha(MpvqcAppearance.palette.foreground, _dot.hovered ? 0.35 : 0.2)

                            Behavior on width {
                                NumberAnimation {
                                    duration: 220
                                    easing.type: Easing.OutCubic
                                }
                            }

                            Behavior on color {
                                ColorAnimation {
                                    duration: 150
                                }
                            }
                        }
                    }
                }
            }

            Label {
                text: root.pageTitle(root.currentPage)
                font.weight: Font.DemiBold

                Layout.alignment: Qt.AlignHCenter
            }
        }

        SectionScroll {
            id: _pageScroll

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: root.pages.length > 1 ? 0 : 24

            Item {
                id: _pageClip

                property bool _ready: false

                // Every boundary swaps content atomically at the click (no stale text, no
                // frame ever blends two pages), then one edge sweeps to the new height. On a
                // question page the card background rides that edge - appearing stretched
                // when arriving from a taller page and shrinking to fit; the summary is
                // unveiled or swallowed by the same edge.
                property real sweepHeight: root._shownPage === "review"
                    ? (_summaryLoader.item ? _summaryLoader.item.implicitHeight : 0)
                    : _questionCard.implicitHeight

                clip: true
                implicitHeight: _pageClip.sweepHeight

                Layout.fillWidth: true
                Layout.bottomMargin: root._sectionSpacing

                Component.onCompleted: _pageClip._ready = true

                Behavior on sweepHeight {
                    enabled: _pageClip._ready

                    NumberAnimation {
                        duration: 220
                        easing.type: Easing.OutCubic
                    }
                }

                SectionCard {
                    id: _questionCard

                    width: _pageClip.width
                    height: _pageClip.height
                    clip: true
                    visible: root._shownPage !== "review"

                    Loader {
                        active: root._questionPage !== ""
                        sourceComponent: root._componentFor(root._questionPage)

                        Layout.fillWidth: true
                    }
                }

                Loader {
                    id: _summaryLoader

                    width: _pageClip.width
                    active: root._shownPage === "review"
                    visible: active
                    sourceComponent: _reviewContent
                }
            }
        }
    }

    footer: PrototypeFooter {
        primaryLabel: !root.onReview ? "Next" : root.closeOnly ? "Close" : "Confirm import"
        showBack: root.pageIndex > 0
        showCancel: !root.closeOnly

        onBackClicked: root.goTo(root.pageIndex - 1)
        onPrimaryClicked: {
            if (!root.onReview) {
                root.goTo(root.pageIndex + 1);
            }
        }
    }

    Binding {
        when: root.rtlPreview && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.enabled"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.rtlPreview && root.contentItem
        target: root.contentItem
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.rtlPreview && root.footer
        target: root.footer
        property: "LayoutMirroring.enabled"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.rtlPreview && root.footer
        target: root.footer
        property: "LayoutMirroring.childrenInherit"
        value: true
        restoreMode: Binding.RestoreNone
    }

    Component {
        id: _sessionContent

        ColumnLayout {
            spacing: 8

            Label {
                text: "You're about to import <b>" + root.plan.commentCount + "</b> " + (root.plan.commentCount === 1 ? "comment" : "comments") + " into your current session. What do you want to do?"
                textFormat: Text.StyledText
                horizontalAlignment: Text.AlignLeft
                wrapMode: Text.Wrap
                verticalAlignment: Text.AlignVCenter

                Layout.fillWidth: true
                Layout.minimumHeight: 44
                Layout.bottomMargin: 6
            }

            OptionRow {
                selected: !root.replaceComments
                text: "Add to your current comments"

                Layout.fillWidth: true

                onClicked: root.replaceComments = false
            }

            OptionRow {
                selected: root.replaceComments
                text: "Start fresh with the new comments"

                Layout.fillWidth: true

                onClicked: root.replaceComments = true
            }
        }
    }

    Component {
        id: _videoContent

        ColumnLayout {
            spacing: 8

            Label {
                text: "Which video should be loaded?"
                horizontalAlignment: Text.AlignLeft
                wrapMode: Text.Wrap
                verticalAlignment: Text.AlignVCenter

                Layout.fillWidth: true
                Layout.minimumHeight: 44
                Layout.bottomMargin: 6
            }

            Repeater {
                model: root.plan.video.candidates

                delegate: OptionRow {
                    required property int index
                    required property var modelData

                    selected: root.videoChoice === index
                    text: modelData.name
                    fullPath: "/mnt/media/QC/Episode 03/" + modelData.name
                    fromDocument: modelData.fromDocument
                    fromSubtitle: modelData.fromSubtitle

                    Layout.fillWidth: true

                    onClicked: root.videoChoice = index
                }
            }

            OptionRow {
                selected: root.videoChoice === -1
                text: "Skip video"

                Layout.fillWidth: true

                onClicked: root.videoChoice = -1
            }
        }
    }

    Component {
        id: _subtitlesContent

        ColumnLayout {
            spacing: 8

            RowLayout {
                spacing: 8

                Layout.fillWidth: true
                Layout.minimumHeight: 44
                Layout.bottomMargin: 6

                Label {
                    text: root.plan.subtitles.candidates.length === 1
                        ? "Which subtitle should be loaded?"
                        : "Which subtitles should be loaded?"
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Text.Wrap

                    Layout.fillWidth: true
                }

                SelectAllCheckBox {
                    visible: root.plan.subtitles.candidates.length > 1
                    checkedCount: root.selectedSubtitles.length
                    totalCount: root.plan.subtitles.candidates.length

                    onToggleAllRequested: root.toggleAllSubtitles()
                }
            }

            Repeater {
                model: root.plan.subtitles.candidates

                delegate: CheckRow {
                    required property int index
                    required property string modelData

                    isChecked: root.subtitleChoices[index] === true
                    text: modelData
                    fullPath: "/mnt/media/QC/Episode 03/" + modelData

                    Layout.fillWidth: true

                    onToggleRequested: root.toggleSubtitle(index)
                }
            }
        }
    }

    Component {
        id: _reviewContent

        ColumnLayout {
            spacing: root._sectionSpacing

            SectionCard {
                title: root.plan.commentCount === 1 ? "Comment" : "Comments"
                visible: root.plan.commentCount > 0

                Layout.fillWidth: true

                SummaryRow {
                    icon: MpvqcIcons.comment
                    text: root.plan.commentCount + (root.plan.commentCount === 1 ? " comment" : " comments")
                    subText: root.plan.session.resolved ? ""
                        : root.replaceComments ? "replacing your current comments"
                        : "added to your current comments"

                    Layout.fillWidth: true
                }
            }

            SectionCard {
                title: "Video"
                visible: root.plan.video.load !== "" || root.plan.video.candidates.length > 0

                Layout.fillWidth: true

                SummaryRow {
                    readonly property string chosen: root.plan.video.resolved ? root.plan.video.load
                        : root.videoChoice === -1 ? "" : root.plan.video.candidates[root.videoChoice].name

                    icon: MpvqcIcons.movie
                    iconColor: chosen === "" ? MpvqcAppearance.palette.hint : MpvqcAppearance.palette.foreground
                    text: chosen === "" ? "No video will be loaded" : chosen
                    fullPath: chosen === "" ? "" : "/mnt/media/QC/Episode 03/" + chosen

                    Layout.fillWidth: true
                }
            }

            SectionCard {
                title: root.selectedSubtitles.length === 1 ? "Subtitle" : "Subtitles"
                visible: !root.plan.subtitles.resolved || root.plan.subtitles.load.length > 0

                Layout.fillWidth: true

                Label {
                    visible: root.selectedSubtitles.length === 0
                    text: "No subtitles will be loaded"
                    color: MpvqcAppearance.palette.hint

                    Layout.fillWidth: true
                }

                Repeater {
                    model: root.selectedSubtitles

                    delegate: SummaryRow {
                        required property string modelData

                        icon: MpvqcIcons.subtitles
                        text: modelData
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData

                        Layout.fillWidth: true
                    }
                }
            }

            SectionCard {
                title: "Not imported"
                visible: root.plan.rejectedDocuments.length > 0

                Layout.fillWidth: true
                Layout.bottomMargin: root._sectionSpacing

                Repeater {
                    model: root.plan.rejectedDocuments

                    delegate: SummaryRow {
                        required property var modelData

                        icon: MpvqcIcons.error
                        iconColor: MpvqcAppearance.palette.error
                        text: modelData.filename
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData.filename
                        subText: modelData.reason

                        Layout.fillWidth: true
                    }
                }
            }

            Label {
                visible: root.closeOnly
                text: "Nothing can be imported."
                color: MpvqcAppearance.palette.hint

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 12
            }
        }
    }
}
