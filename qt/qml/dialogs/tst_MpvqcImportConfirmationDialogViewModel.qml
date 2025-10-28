// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcImportConfirmationDialogViewModel"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcImportConfirmationDialogViewModel {}
    }

    function makeControl(videosJson: string, subtitlesJson: string): var {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            videosJson: videosJson,
            subtitlesJson: subtitlesJson
        });
        verify(control);
        return control;
    }

    function test_videosWithSkipOption() {
        const videosJson = JSON.stringify([
            {
                path: "/video1.mp4",
                filename: "video1.mp4",
                fromDocument: true,
                fromSubtitle: false
            },
            {
                path: "/video2.mp4",
                filename: "video2.mp4",
                fromDocument: false,
                fromSubtitle: true
            }
        ]);
        const control = makeControl(videosJson, "[]");

        compare(control.videosWithSkipOption.length, 3);

        const skipOption = control.videosWithSkipOption[control.videosWithSkipOption.length - 1];
        compare(skipOption.path, "");
        compare(skipOption.filename, "");
        compare(skipOption.fromDocument, false);
        compare(skipOption.fromSubtitle, false);
        verify(skipOption.isNoVideo);
    }

    function test_selectVideo_data() {
        return [
            {
                tag: "first_video",
                videoIndex: 0,
                expectedIndex: 0
            },
            {
                tag: "skip_option",
                videoIndex: 2,
                expectedIndex: 2
            },
            {
                tag: "middle_video",
                videoIndex: 1,
                expectedIndex: 1
            },
        ];
    }

    function test_selectVideo(data) {
        const videosJson = JSON.stringify([
            {
                path: "/v1.mp4",
                filename: "v1.mp4",
                fromDocument: true,
                fromSubtitle: false
            },
            {
                path: "/v2.mp4",
                filename: "v2.mp4",
                fromDocument: false,
                fromSubtitle: true
            }
        ]);
        const control = makeControl(videosJson, "[]");

        control.selectVideo(data.videoIndex);

        compare(control.selectedVideoIndex, data.expectedIndex);
    }

    function test_toggleSubtitle_data() {
        return [
            {
                tag: "toggle_checked",
                subtitleIndex: 0,
                timesToToggle: 1,
                expectedFinalState: false
            },
            {
                tag: "toggle_twice",
                subtitleIndex: 1,
                timesToToggle: 2,
                expectedFinalState: true
            },
        ];
    }

    function test_toggleSubtitle(data) {
        const subtitlesJson = JSON.stringify([
            {
                path: "/s1.srt",
                filename: "s1.srt",
                checked: true
            },
            {
                path: "/s2.srt",
                filename: "s2.srt",
                checked: true
            }
        ]);
        const control = makeControl("[]", subtitlesJson);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "modelChanged"
        });
        verify(spy);

        compare(control.subtitles[data.subtitleIndex].checked, true);

        for (let i = 0; i < data.timesToToggle; i++) {
            control.toggleSubtitle(data.subtitleIndex);
        }

        compare(control.subtitles[data.subtitleIndex].checked, data.expectedFinalState);
        compare(spy.count, data.timesToToggle);
    }

    function test_bulk_subtitle_selection_data() {
        return [
            {
                tag: "select_all_from_mixed",
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    },
                    {
                        path: "/s2.srt",
                        filename: "s2.srt",
                        checked: true
                    },
                    {
                        path: "/s3.srt",
                        filename: "s3.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [1, 2],
                operation: "selectAll",
                expectedAllChecked: true
            },
            {
                tag: "deselect_all_from_all",
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    },
                    {
                        path: "/s2.srt",
                        filename: "s2.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [],
                operation: "deselectAll",
                expectedAllChecked: false
            },
            {
                tag: "deselect_all_from_mixed",
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    },
                    {
                        path: "/s2.srt",
                        filename: "s2.srt",
                        checked: true
                    },
                    {
                        path: "/s3.srt",
                        filename: "s3.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [1],
                operation: "deselectAll",
                expectedAllChecked: false
            },
        ];
    }

    function test_bulk_subtitle_selection(data) {
        const control = makeControl("[]", data.subtitlesJson);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "modelChanged"
        });
        verify(spy);

        for (const index of data.indicesToToggle) {
            control.toggleSubtitle(index);
        }
        spy.clear();

        if (data.operation === "selectAll") {
            control.selectAllSubtitles();
        } else {
            control.deselectAllSubtitles();
        }

        for (let i = 0; i < control.subtitles.length; i++) {
            compare(control.subtitles[i].checked, data.expectedAllChecked);
        }

        compare(spy.count, 1);
    }

    function test_getSelectedItems_data() {
        return [
            {
                tag: "video_with_all_subs",
                selectedVideoIndex: 0,
                videosJson: JSON.stringify([
                    {
                        path: "/v1.mp4",
                        filename: "v1.mp4",
                        fromDocument: true,
                        fromSubtitle: false
                    }
                ]),
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    },
                    {
                        path: "/s2.srt",
                        filename: "s2.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [],
                expectedVideoPath: "/v1.mp4",
                expectedSubtitlePaths: ["/s1.srt", "/s2.srt"]
            },
            {
                tag: "skip_video_with_subs",
                selectedVideoIndex: 1,
                videosJson: JSON.stringify([
                    {
                        path: "/v1.mp4",
                        filename: "v1.mp4",
                        fromDocument: true,
                        fromSubtitle: false
                    }
                ]),
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [],
                expectedVideoPath: "",
                expectedSubtitlePaths: ["/s1.srt"]
            },
            {
                tag: "video_with_no_subs",
                selectedVideoIndex: 0,
                videosJson: JSON.stringify([
                    {
                        path: "/v1.mp4",
                        filename: "v1.mp4",
                        fromDocument: true,
                        fromSubtitle: false
                    }
                ]),
                subtitlesJson: JSON.stringify([]),
                indicesToToggle: [],
                expectedVideoPath: "/v1.mp4",
                expectedSubtitlePaths: []
            },
            {
                tag: "video_with_mixed_subs",
                selectedVideoIndex: 1,
                videosJson: JSON.stringify([
                    {
                        path: "/v1.mp4",
                        filename: "v1.mp4",
                        fromDocument: true,
                        fromSubtitle: false
                    },
                    {
                        path: "/v2.mp4",
                        filename: "v2.mp4",
                        fromDocument: false,
                        fromSubtitle: true
                    }
                ]),
                subtitlesJson: JSON.stringify([
                    {
                        path: "/s1.srt",
                        filename: "s1.srt",
                        checked: true
                    },
                    {
                        path: "/s2.srt",
                        filename: "s2.srt",
                        checked: true
                    },
                    {
                        path: "/s3.srt",
                        filename: "s3.srt",
                        checked: true
                    }
                ]),
                indicesToToggle: [1],
                expectedVideoPath: "/v2.mp4",
                expectedSubtitlePaths: ["/s1.srt", "/s3.srt"]
            },
        ];
    }

    function test_getSelectedItems(data) {
        const control = makeControl(data.videosJson, data.subtitlesJson);

        control.selectVideo(data.selectedVideoIndex);

        for (const index of data.indicesToToggle) {
            control.toggleSubtitle(index);
        }

        const result = control.getSelectedItems();

        compare(result.video, data.expectedVideoPath);
        compare(result.subtitles.length, data.expectedSubtitlePaths.length);

        for (let i = 0; i < data.expectedSubtitlePaths.length; i++) {
            compare(result.subtitles[i], data.expectedSubtitlePaths[i]);
        }
    }
}
