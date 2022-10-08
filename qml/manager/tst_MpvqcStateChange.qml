/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick 2.0
import QtTest
import "MpvqcStateChanges.js" as TestObject

Item {

    property string defaultDocument: 'defaultDocument'
    property string defaultVideo: 'some-path'

    property bool saved: true
    property bool unsaved: false

    property var noDocuments: []
    property var oneDocument: [defaultDocument]
    property var twoDocuments: [defaultDocument, defaultDocument]
    property string videoPresent: defaultVideo
    property string noVideoPresent: ''

    TestCase {
        name: 'MpvqcStateChanges::ImportChanges'

        function test_isOnlyVideoImported() {
            const changes1 = new TestObject.ImportChanges(noDocuments, videoPresent)
            verify(changes1.isOnlyVideoImported)
            const changes2 = new TestObject.ImportChanges(oneDocument, videoPresent)
            verify(!changes2.isOnlyVideoImported)
            const changes3 = new TestObject.ImportChanges(oneDocument, noVideoPresent)
            verify(!changes3.isOnlyVideoImported)
            const changes4 = new TestObject.ImportChanges(noDocuments, noVideoPresent)
            verify(!changes4.isOnlyVideoImported)
        }

        function test_isExactlyOneDocumentImported() {
            const changes1 = new TestObject.ImportChanges(noDocuments, videoPresent)
            verify(!changes1.isExactlyOneDocumentImported)
            const changes2 = new TestObject.ImportChanges(['one'], videoPresent)
            verify(changes2.isExactlyOneDocumentImported)
            const changes3 = new TestObject.ImportChanges(['one', 'two'], videoPresent)
            verify(!changes3.isExactlyOneDocumentImported)
        }

        function test_thatImportedDocument() {
            const changes1 = new TestObject.ImportChanges(noDocuments, videoPresent)
            compare(changes1.thatImportedDocument, undefined)
            const changes2 = new TestObject.ImportChanges(['one'], videoPresent)
            compare(changes2.thatImportedDocument, 'one')
            const changes3 = new TestObject.ImportChanges(['one', 'two'], videoPresent)
            compare(changes3.thatImportedDocument, 'one')
        }
    }

    TestCase {
        name: 'MpvqcStateChanges::ApplicationState'

        function test_findVideo() {
            const unavailable = ''
            const standalone = 'standalone-video'
            const present = 'present-video'

            const state = new TestObject.InitialState(present)
            let change = new TestObject.ImportChanges(noDocuments, standalone)
            let video = state.findVideo(change)
            compare(video, standalone)

            change = new TestObject.ImportChanges(noDocuments, unavailable)
            video = state.findVideo(change)
            compare(video, present)
        }

        function test_handleSave() {
            let video = ''
            let document = ''
            let state = new TestObject.OtherState(video, document, unsaved)
            state = state.handleSave('other-document')
            compare(state.video, video)
            compare(state.document, 'other-document')
            verify(state.saved)

            video = 'video'
            document = 'document'
            state = new TestObject.OtherState(video, document, unsaved)
            state = state.handleSave('other-document')
            compare(state.video, video)
            compare(state.document, 'other-document')
            verify(state.saved)
        }

        function test_handleChange() {
            let video = ''
            let document = ''
            let state = new TestObject.OtherState(video, document, saved)
            state = state.handleChange()
            compare(state.video, video)
            compare(state.document, document)
            verify(!state.saved)

            video = 'video'
            document = 'document'
            state = new TestObject.OtherState(video, document, saved)
            state = state.handleChange()
            compare(state.video, video)
            compare(state.document, document)
            verify(!state.saved)
        }

        function test_handleReset() {
            let video = ''
            let document = ''
            let state = new TestObject.OtherState(video, document, saved)
            state = state.handleReset()
            compare(state.video, video)
            verify(!state.document)
            verify(state.saved)
            verify(state.constructor.toString().includes('InitialState'))

            video = 'video'
            document = 'document'
            state = new TestObject.OtherState(video, document, saved)

            state = state.handleReset()
            compare(state.video, video)
            verify(!state.document)
            verify(state.saved)
            verify(state.constructor.toString().includes('InitialState'))
        }

    }

    TestCase {
        name: 'MpvqcStateChanges::InitialState'

        function verifyInitialState(state) {
            verify(state.constructor.toString().includes('InitialState'))
        }

        function verifyOtherState(state) {
            verify(state.constructor.toString().includes('OtherState'))
        }

        function test_handleImport_video1x() {
            const video1 = 'video-1'
            const importSummary = new TestObject.ImportChanges(noDocuments, video1)
            let state = new TestObject.InitialState('')
            state = state.handleImport(importSummary)
            verifyInitialState(state)
            compare(state.video, video1)
        }

        function test_handleImport_video2x() {
            const video1 = 'video-1'
            const video2 = 'video-2'
            const import1Summary = new TestObject.ImportChanges(noDocuments, video1)
            const import2Summary = new TestObject.ImportChanges(noDocuments, video2)
            let state = new TestObject.InitialState('')
            state = state.handleImport(import1Summary).handleImport(import2Summary)
            verifyInitialState(state)
            compare(state.video, video2)
        }

        function test_handleImport_documents1x() {
            const video = 'video'
            const importSummary = new TestObject.ImportChanges(oneDocument, video)
            let state = new TestObject.InitialState('video-initial')
            state = state.handleImport(importSummary)
            verifyOtherState(state)
            compare(state.video, 'video')
            compare(state.document, defaultDocument)
            verify(state.saved)
        }

        function test_handleImport_documents2x() {
            const video = 'video'
            const importSummary = new TestObject.ImportChanges(twoDocuments, video)
            let state = new TestObject.InitialState('video-initial')
            state = state.handleImport(importSummary)
            verifyOtherState(state)
            compare(state.video, 'video')
            compare(state.document, '')
            verify(!state.saved)
        }

    }

    TestCase {
        name: 'MpvqcStateChanges::OtherState'

        function verifyOtherState(state) {
            verify(state.constructor.toString().includes('OtherState'))
        }

        function test_handleImport_videoIsSame() {
            const video = 'video'
            const document = 'document'
            const importSummary = new TestObject.ImportChanges(noDocuments, video)
            let state = new TestObject.OtherState(video, document, saved)
            state = state.handleImport(importSummary)
            verifyOtherState(state)
            compare(state.video, video)
            compare(state.document, document)
            verify(state.saved)
        }

        function test_handleImport_videoIsDifferent() {
            const video = 'video'
            const document = 'document'
            const importSummary = new TestObject.ImportChanges(noDocuments, 'video-different')
            let state = new TestObject.OtherState(video, document, saved)
            state = state.handleImport(importSummary)
            verifyOtherState(state)
            compare(state.video, 'video-different')
            verify(!state.document)
            verify(!state.saved)
        }

        function test_handleImport_document() {
            const video = 'video'
            const document = 'document'
            const importSummary = new TestObject.ImportChanges(oneDocument, video)
            let state = new TestObject.OtherState(video, document, saved)
            state = state.handleImport(importSummary)
            verifyOtherState(state)
            compare(state.video, video)
            verify(!state.document)
            verify(!state.saved)
        }

    }

}
