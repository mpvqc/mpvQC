// PROTOTYPE - three variants of the import wizard redesign (internal ticket #114), switchable
// via the floating bar at the bottom. Left/Right arrows cycle variants, S cycles the data
// scenario. Delete this directory once a direction is picked.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ApplicationWindow {
    id: root

    readonly property MpvqcAppearanceDialogViewModel appearanceViewModel: MpvqcAppearanceDialogViewModel {}

    // Stub data only - shapes mirror the importing domain's concerns. resolved: true means the
    // plan already knows the answer; the wizard's job is to show it, not ask.
    readonly property var scenarios: [
        {
            name: "Every question open",
            commentCount: 42,
            acceptedDocuments: ["episode-03.qc", "old-notes.txt"],
            rejectedDocuments: [
                {
                    filename: "broken.qc",
                    reason: "Not a QC document"
                }
            ],
            session: {
                resolved: false
            },
            video: {
                resolved: false,
                load: "",
                candidates: [
                    {
                        name: "episode-03.mkv",
                        fromDocument: true,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.v2.mkv",
                        fromDocument: false,
                        fromSubtitle: true
                    }
                ]
            },
            subtitles: {
                resolved: false,
                load: [],
                candidates: ["episode-03.de.srt", "episode-03.en.srt", "episode-03.fr.srt", "episode-03.es.srt", "episode-03.it.srt", "episode-03.ja.srt"]
            }
        },
        {
            name: "One question left",
            commentCount: 42,
            acceptedDocuments: ["episode-03.qc"],
            rejectedDocuments: [],
            session: {
                resolved: true
            },
            video: {
                resolved: true,
                load: "[QC-Crew] Beyond the Long Night - 03 (1080p HEVC 10bit AAC) [B47A1FC2].mkv",
                candidates: []
            },
            subtitles: {
                resolved: false,
                load: [],
                candidates: ["episode-03.de.srt", "episode-03.en.srt"]
            }
        },
        {
            name: "Many candidates",
            commentCount: 42,
            acceptedDocuments: ["episode-03.qc"],
            rejectedDocuments: [],
            session: {
                resolved: true
            },
            video: {
                resolved: false,
                load: "",
                candidates: [
                    {
                        name: "episode-03.mkv",
                        fromDocument: true,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.v2.mkv",
                        fromDocument: false,
                        fromSubtitle: true
                    },
                    {
                        name: "[QC-Crew] Beyond the Long Night - 03 - Director's Cut (2160p HDR HEVC 10bit TrueHD Atmos) [F91D22A7].mkv",
                        fromDocument: true,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.1080p.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.720p.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.hdr.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.web.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.bluray.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.remux.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    },
                    {
                        name: "episode-03.final.mkv",
                        fromDocument: false,
                        fromSubtitle: false
                    }
                ]
            },
            subtitles: {
                resolved: false,
                load: [],
                candidates: ["episode-03.de.srt", "episode-03.en.srt", "[QC-Crew] Beyond the Long Night - 03 - full dialogue, signs and songs.en-US.forced.srt", "episode-03.es.srt", "episode-03.it.srt", "episode-03.ja.srt", "episode-03.ar.srt", "episode-03.pl.srt", "episode-03.pt.srt", "episode-03.ru.srt"]
            }
        },
        {
            name: "Document + error",
            commentCount: 1,
            acceptedDocuments: ["episode-03.qc"],
            rejectedDocuments: [
                {
                    filename: "broken.qc",
                    reason: "Not a QC document"
                }
            ],
            session: {
                resolved: true
            },
            video: {
                resolved: true,
                load: "",
                candidates: []
            },
            subtitles: {
                resolved: true,
                load: [],
                candidates: []
            }
        },
        {
            name: "Errors only",
            commentCount: 0,
            acceptedDocuments: [],
            rejectedDocuments: [
                {
                    filename: "broken.qc",
                    reason: "Not a QC document"
                },
                {
                    filename: "future.json",
                    reason: "Unsupported version"
                }
            ],
            session: {
                resolved: true
            },
            video: {
                resolved: true,
                load: "",
                candidates: []
            },
            subtitles: {
                resolved: true,
                load: [],
                candidates: []
            }
        }
    ]

    readonly property var variants: [
        {
            key: "C",
            name: "Steps + summary",
            component: _steps
        }
    ]

    property int scenarioIndex: 0
    property int variantIndex: 0
    property bool rtl: false

    readonly property var plan: root.scenarios[root.scenarioIndex]

    function cycleVariant(offset: int): void {
        root.variantIndex = (root.variantIndex + offset + root.variants.length) % root.variants.length;
        root.reloadVariant();
    }

    function cycleScenario(): void {
        root.scenarioIndex = (root.scenarioIndex + 1) % root.scenarios.length;
        root.reloadVariant();
    }

    function reloadVariant(): void {
        _variantLoader.active = false;
        _variantLoader.active = true;
    }

    function themeDark(): void {
        root.appearanceViewModel.setColorSchemePreference("dark");
    }

    function themeLight(): void {
        root.appearanceViewModel.setColorSchemePreference("light");
    }

    width: 960
    height: 860
    visible: true
    font: MpvqcFonts.applicationFont
    color: MpvqcAppearance.palette.background

    M.Material.theme: MpvqcAppearance.isDark ? M.Material.Dark : M.Material.Light
    M.Material.accent: MpvqcAppearance.palette.accent
    M.Material.background: MpvqcAppearance.palette.background
    M.Material.foreground: MpvqcAppearance.palette.foreground
    title: "Import wizard prototype"

    Loader {
        id: _variantLoader

        anchors.fill: parent
        sourceComponent: root.variants[root.variantIndex].component
    }

    Component {
        id: _steps

        VariantSteps {
            plan: root.plan
            rtlPreview: root.rtl
        }
    }


    Popup {
        id: _switcher

        parent: Overlay.overlay
        x: (parent.width - width) / 2
        y: parent.height - height - 16
        z: 100
        visible: true
        modal: false
        closePolicy: Popup.NoAutoClose
        padding: 4

        contentItem: RowLayout {
            spacing: 4

            ToolButton {
                text: "‹"

                onClicked: root.cycleVariant(-1)
            }

            Label {
                text: root.variants[root.variantIndex].key + " — " + root.variants[root.variantIndex].name
                horizontalAlignment: Text.AlignHCenter

                Layout.preferredWidth: 220
            }

            ToolButton {
                text: "›"

                onClicked: root.cycleVariant(1)
            }

            ToolSeparator {}

            ToolButton {
                text: "Scenario: " + root.plan.name

                onClicked: root.cycleScenario()
            }

            ToolSeparator {}

            ToolButton {
                text: MpvqcAppearance.isDark ? "Light" : "Dark"

                onClicked: root.appearanceViewModel.setColorSchemePreference(MpvqcAppearance.isDark ? "light" : "dark")
            }

            ToolSeparator {}

            ToolButton {
                text: root.rtl ? "LTR" : "RTL"

                onClicked: {
                    root.rtl = !root.rtl;
                    root.reloadVariant();
                }
            }
        }
    }

    Shortcut {
        sequences: ["Left"]
        context: Qt.ApplicationShortcut

        onActivated: root.cycleVariant(-1)
    }

    Shortcut {
        sequences: ["Right"]
        context: Qt.ApplicationShortcut

        onActivated: root.cycleVariant(1)
    }

    Shortcut {
        sequences: ["S"]
        context: Qt.ApplicationShortcut

        onActivated: root.cycleScenario()
    }
}
