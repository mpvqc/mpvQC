// PROTOTYPE - Variant D "Sentence-first": the dialog is one sentence built from the plan plus
// sensible defaults, confirmable immediately. "Adjust import" expands the A-style cards for the
// uncommon case where the defaults are wrong.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root

    required property var plan

    property bool adjusting: false
    property bool replaceComments: false
    property int videoChoice: 0
    property var subtitleChoices: root.plan.subtitles.candidates.map(() => true)

    readonly property bool closeOnly: root.plan.commentCount === 0
        && root.plan.video.load === "" && root.plan.video.candidates.length === 0
        && root.plan.subtitles.load.length === 0 && root.plan.subtitles.candidates.length === 0

    readonly property string _chosenVideo: root.plan.video.resolved ? root.plan.video.load
        : root.videoChoice === -1 ? "" : root.plan.video.candidates[root.videoChoice]
    readonly property int _subtitleCount: root.plan.subtitles.resolved
        ? root.plan.subtitles.load.length
        : root.subtitleChoices.filter(c => c).length

    readonly property string sentence: {
        const parts = [];
        if (root.plan.commentCount > 0) {
            const suffix = root.plan.session.resolved ? "" : " into your current session";
            parts.push("<b>" + root.plan.commentCount + "</b> comments" + suffix);
        }
        if (root._chosenVideo !== "") {
            parts.push("the video <b>" + root._chosenVideo + "</b>");
        }
        if (root._subtitleCount > 0) {
            parts.push("<b>" + root._subtitleCount + "</b> subtitle files");
        }
        if (parts.length === 0) {
            return "";
        }
        const joined = parts.length === 1 ? parts[0] : parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1];
        return "Import " + joined + "?";
    }

    readonly property int _sectionSpacing: 12

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: root.adjusting ? MpvqcConstants.mediumDialogContentHeight : _collapsed.implicitHeight + 24

    contentItem: Item {

        ColumnLayout {
            id: _collapsed

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.topMargin: 12

            visible: !root.adjusting
            spacing: root._sectionSpacing

            Label {
                visible: root.sentence !== ""
                text: root.sentence
                textFormat: Text.StyledText
                wrapMode: Text.Wrap

                Layout.fillWidth: true
            }

            Label {
                visible: root.closeOnly
                text: "Nothing can be imported."
                color: MpvqcAppearance.palette.hint

                Layout.fillWidth: true
            }

            Repeater {
                model: root.plan.rejectedDocuments

                delegate: SummaryRow {
                    required property var modelData

                    icon: MpvqcIcons.error
                    iconColor: MpvqcAppearance.palette.error
                    text: modelData.filename
                    subText: modelData.reason
                    trailing: "skipped"

                    Layout.fillWidth: true
                }
            }

            Button {
                visible: !root.closeOnly
                flat: true
                text: "Adjust import"

                Layout.alignment: Qt.AlignLeft

                onClicked: root.adjusting = true
            }
        }

        ScrollView {
            id: _scroll

            anchors.fill: parent

            visible: root.adjusting
            contentWidth: availableWidth
            contentHeight: _sections.implicitHeight

            ColumnLayout {
                id: _sections

                width: _scroll.availableWidth
                spacing: root._sectionSpacing

                SectionCard {
                    title: "Comments"
                    visible: root.plan.commentCount > 0

                    Layout.fillWidth: true
                    Layout.topMargin: root._sectionSpacing

                    SummaryRow {
                        icon: MpvqcIcons.comment
                        text: root.plan.commentCount + " comments"

                        Layout.fillWidth: true
                    }

                    OptionRow {
                        visible: !root.plan.session.resolved
                        selected: !root.replaceComments
                        text: "Add to your current comments"

                        Layout.fillWidth: true

                        onClicked: root.replaceComments = false
                    }

                    OptionRow {
                        visible: !root.plan.session.resolved
                        selected: root.replaceComments
                        text: "Start fresh with the new comments"

                        Layout.fillWidth: true

                        onClicked: root.replaceComments = true
                    }
                }

                SectionCard {
                    title: "Video"
                    visible: !root.plan.video.resolved || root.plan.video.load !== ""

                    Layout.fillWidth: true

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

                            selected: root.videoChoice === index
                            text: modelData

                            Layout.fillWidth: true

                            onClicked: root.videoChoice = index
                        }
                    }

                    OptionRow {
                        visible: !root.plan.video.resolved
                        selected: root.videoChoice === -1
                        text: "Skip video"

                        Layout.fillWidth: true

                        onClicked: root.videoChoice = -1
                    }
                }

                SectionCard {
                    title: "Subtitles"
                    visible: !root.plan.subtitles.resolved || root.plan.subtitles.load.length > 0

                    Layout.fillWidth: true

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
                            subText: modelData.reason

                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }
    }

    footer: PrototypeFooter {
        primaryLabel: root.closeOnly ? "Close" : "Confirm import"
        showCancel: !root.closeOnly
    }

    Behavior on contentHeight {
        NumberAnimation {
            duration: 220
            easing.type: Easing.OutCubic
        }
    }
}
