// PROTOTYPE - Variant B "Checklist": a vertical accordion of section cards. The sections ARE the
// step indicator: each header carries a status glyph and a live summary, the open question is
// expanded, answering collapses it and expands the next. Resolved concerns sit as collapsed,
// expandable facts.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root

    required property var plan

    property bool replaceComments: false
    property int videoChoice: 0
    property var subtitleChoices: root.plan.subtitles.candidates.map(() => true)

    property bool sessionAnswered: root.plan.session.resolved
    property bool videoAnswered: root.plan.video.resolved
    property bool subtitlesAnswered: root.plan.subtitles.resolved
    property string expandedKey: root.firstOpenKey()

    readonly property bool allAnswered: root.sessionAnswered && root.videoAnswered && root.subtitlesAnswered
    readonly property bool closeOnly: root.plan.commentCount === 0
        && root.plan.video.load === "" && root.plan.video.candidates.length === 0
        && root.plan.subtitles.load.length === 0 && root.plan.subtitles.candidates.length === 0

    readonly property int selectedSubtitleCount: root.subtitleChoices.filter(c => c).length
    readonly property int _sectionSpacing: 12

    function firstOpenKey(): string {
        if (!root.sessionAnswered) {
            return "comments";
        }
        if (!root.videoAnswered) {
            return "video";
        }
        if (!root.subtitlesAnswered) {
            return "subtitles";
        }
        return "";
    }

    function toggleExpanded(key: string): void {
        root.expandedKey = root.expandedKey === key ? "" : key;
    }

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    component AccordionSection: Item {
        id: _section

        property string title
        property string summary
        property url statusIcon
        property color statusColor: MpvqcAppearance.palette.foreground
        property bool expanded: false
        default property alias body: _body.data

        signal headerClicked()

        readonly property int _padding: 16

        property bool _ready: false

        implicitHeight: _header.implicitHeight + (_section.expanded ? _body.implicitHeight + _section._padding : 0)
        clip: true

        Component.onCompleted: _section._ready = true

        Rectangle {
            anchors.fill: parent
            radius: 20
            color: MpvqcAppearance.palette.sectionCard
        }

        ItemDelegate {
            id: _header

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            verticalPadding: 14
            horizontalPadding: _section._padding

            contentItem: RowLayout {
                spacing: 12

                MpvqcIconLabel {
                    iconColor: _section.statusColor
                    icon.source: _section.statusIcon
                    icon.width: 20
                    icon.height: 20

                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20
                }

                Label {
                    text: _section.title
                    font.weight: Font.DemiBold
                    horizontalAlignment: Text.AlignLeft

                    Layout.fillWidth: false
                }

                Label {
                    text: _section.summary
                    color: MpvqcAppearance.palette.hint
                    horizontalAlignment: Text.AlignRight
                    elide: Text.ElideMiddle

                    Layout.fillWidth: true
                }

                MpvqcIconLabel {
                    iconColor: MpvqcAppearance.palette.hint
                    icon.source: MpvqcIcons.keyboardArrowDown
                    icon.width: 20
                    icon.height: 20
                    rotation: _section.expanded ? 180 : 0

                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20

                    Behavior on rotation {
                        NumberAnimation {
                            duration: 220
                            easing.type: Easing.OutCubic
                        }
                    }
                }
            }

            onClicked: _section.headerClicked()
        }

        ColumnLayout {
            id: _body

            anchors.top: _header.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: _section._padding
            anchors.rightMargin: _section._padding
        }

        Behavior on implicitHeight {
            enabled: _section._ready

            NumberAnimation {
                duration: 220
                easing.type: Easing.OutCubic
            }
        }
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: MpvqcConstants.mediumDialogContentHeight

    contentItem: ScrollView {
        id: _scroll

        contentWidth: availableWidth
        contentHeight: _sections.implicitHeight

        ColumnLayout {
            id: _sections

            width: _scroll.availableWidth
            spacing: root._sectionSpacing

            AccordionSection {
                title: "Comments"
                visible: root.plan.commentCount > 0
                expanded: root.expandedKey === "comments"
                summary: !root.sessionAnswered ? ""
                    : root.plan.session.resolved ? root.plan.commentCount + " comments"
                    : root.replaceComments ? root.plan.commentCount + " comments · replacing"
                    : root.plan.commentCount + " comments · adding"
                statusIcon: root.sessionAnswered ? MpvqcIcons.check
                    : root.expandedKey === "comments" ? MpvqcIcons.circleFilled : MpvqcIcons.circle

                Layout.fillWidth: true
                Layout.topMargin: root._sectionSpacing

                onHeaderClicked: root.toggleExpanded("comments")

                SummaryRow {
                    icon: MpvqcIcons.description
                    text: "from " + root.plan.acceptedDocuments.join(", ")

                    Layout.fillWidth: true
                }

                OptionRow {
                    visible: !root.plan.session.resolved
                    selected: root.sessionAnswered && !root.replaceComments
                    text: "Add to your current comments"

                    Layout.fillWidth: true

                    onClicked: {
                        root.replaceComments = false;
                        root.sessionAnswered = true;
                        root.expandedKey = root.firstOpenKey();
                    }
                }

                OptionRow {
                    visible: !root.plan.session.resolved
                    selected: root.sessionAnswered && root.replaceComments
                    text: "Start fresh with the new comments"

                    Layout.fillWidth: true

                    onClicked: {
                        root.replaceComments = true;
                        root.sessionAnswered = true;
                        root.expandedKey = root.firstOpenKey();
                    }
                }
            }

            AccordionSection {
                title: "Video"
                visible: !root.plan.video.resolved || root.plan.video.load !== ""
                expanded: root.expandedKey === "video"
                summary: root.plan.video.resolved ? root.plan.video.load
                    : !root.videoAnswered ? ""
                    : root.videoChoice === -1 ? "no video"
                    : root.plan.video.candidates[root.videoChoice]
                statusIcon: root.videoAnswered ? MpvqcIcons.check
                    : root.expandedKey === "video" ? MpvqcIcons.circleFilled : MpvqcIcons.circle

                Layout.fillWidth: true

                onHeaderClicked: root.toggleExpanded("video")

                SummaryRow {
                    visible: root.plan.video.resolved
                    icon: MpvqcIcons.movie
                    text: root.plan.video.load
                    trailing: "will be loaded"

                    Layout.fillWidth: true
                }

                Repeater {
                    model: root.plan.video.candidates

                    delegate: OptionRow {
                        required property int index
                        required property string modelData

                        selected: root.videoAnswered && root.videoChoice === index
                        text: modelData

                        Layout.fillWidth: true

                        onClicked: {
                            root.videoChoice = index;
                            root.videoAnswered = true;
                            root.expandedKey = root.firstOpenKey();
                        }
                    }
                }

                OptionRow {
                    visible: !root.plan.video.resolved
                    selected: root.videoAnswered && root.videoChoice === -1
                    text: "Skip video"

                    Layout.fillWidth: true

                    onClicked: {
                        root.videoChoice = -1;
                        root.videoAnswered = true;
                        root.expandedKey = root.firstOpenKey();
                    }
                }
            }

            AccordionSection {
                title: "Subtitles"
                visible: !root.plan.subtitles.resolved || root.plan.subtitles.load.length > 0
                expanded: root.expandedKey === "subtitles"
                summary: root.plan.subtitles.resolved ? root.plan.subtitles.load.length + " files"
                    : !root.subtitlesAnswered ? ""
                    : root.selectedSubtitleCount + " of " + root.plan.subtitles.candidates.length + " selected"
                statusIcon: root.subtitlesAnswered ? MpvqcIcons.check
                    : root.expandedKey === "subtitles" ? MpvqcIcons.circleFilled : MpvqcIcons.circle

                Layout.fillWidth: true

                onHeaderClicked: root.toggleExpanded("subtitles")

                Repeater {
                    model: root.plan.subtitles.load

                    delegate: SummaryRow {
                        required property string modelData

                        icon: MpvqcIcons.subtitles
                        text: modelData
                        trailing: "will be loaded"

                        Layout.fillWidth: true
                    }
                }

                Repeater {
                    model: root.plan.subtitles.candidates

                    delegate: CheckRow {
                        required property int index
                        required property string modelData

                        isChecked: root.subtitleChoices[index] === true
                        text: modelData

                        Layout.fillWidth: true

                        onToggleRequested: root.toggleSubtitle(index)
                    }
                }

                Button {
                    visible: !root.plan.subtitles.resolved && !root.subtitlesAnswered
                    flat: true
                    text: "Continue"

                    Layout.alignment: Qt.AlignRight

                    onClicked: {
                        root.subtitlesAnswered = true;
                        root.expandedKey = root.firstOpenKey();
                    }
                }
            }

            AccordionSection {
                title: "Not imported"
                visible: root.plan.rejectedDocuments.length > 0
                expanded: root.expandedKey === "errors"
                summary: root.plan.rejectedDocuments.length === 1 ? "1 file skipped"
                    : root.plan.rejectedDocuments.length + " files skipped"
                statusIcon: MpvqcIcons.error
                statusColor: MpvqcAppearance.palette.error

                Layout.fillWidth: true
                Layout.bottomMargin: root._sectionSpacing

                onHeaderClicked: root.toggleExpanded("errors")

                Repeater {
                    model: root.plan.rejectedDocuments

                    delegate: SummaryRow {
                        required property var modelData

                        icon: MpvqcIcons.error
                        iconColor: MpvqcAppearance.palette.error
                        text: modelData.filename
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

    footer: PrototypeFooter {
        primaryLabel: root.closeOnly ? "Close" : "Confirm import"
        primaryEnabled: root.closeOnly || root.allAnswered
        showCancel: !root.closeOnly
    }
}
