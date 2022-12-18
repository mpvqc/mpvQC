// noinspection JSUnusedGlobalSymbols

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


class ExportContentGenerator {

    /**
     * @param absPathGetterFunc {mpvqcAbsPathGetterFunc}
     * @param nicknameGetterFunc {mpvqcNicknameGetterFunc}
     * @param commentGetterFunc {mpvqcCommentGetterFunc}
     * @param settingsGetterFunc {mpvqcSettingsGetterFunc}
     * @param timeFormatFunc {mpvqcTimeFormatFunc}
     */
    constructor(
        absPathGetterFunc,
        nicknameGetterFunc,
        commentGetterFunc,
        settingsGetterFunc,
        timeFormatFunc,
    ) {
        this.dataGenerator = new DataGenerator(absPathGetterFunc, nicknameGetterFunc, commentGetterFunc)
        this.exportSettingsGenerator = new SettingsGenerator(settingsGetterFunc)
        this.documentCombiner = new DocumentFileCombiner(timeFormatFunc)
    }

    /**
     * @param video {QUrl}
     * @return string
     */
    createExportContent(video) {
        const data = this.dataGenerator.generateDataWith(video)
        const settings = this.exportSettingsGenerator.generateExportSettings()
        return this.documentCombiner.generateDocumentFrom(data, settings)
    }

    /**
     * @param video {QUrl}
     * @return string
     */
    createBackupContent(video) {
        const data = this.dataGenerator.generateDataWith(video)
        const settings = this.exportSettingsGenerator.generateBackupSettings()
        return this.documentCombiner.generateDocumentFrom(data, settings)
    }

}


class DataGenerator {

    /**
     * @param absPathGetterFunc {mpvqcAbsPathGetterFunc}
     * @param nicknameGetterFunc {mpvqcNicknameGetterFunc}
     * @param commentGetterFunc {mpvqcCommentGetterFunc}
     */
    constructor(absPathGetterFunc, nicknameGetterFunc, commentGetterFunc) {
        this.nicknameGetterFunc = nicknameGetterFunc
        this.absPathGetterFunc = absPathGetterFunc
        this.commentGetterFunc = commentGetterFunc
    }

    /**
     * @param video {QUrl}
     * @return MpvqcExportData
     */
    generateDataWith(video) {
        // noinspection JSUnresolvedVariable
        const date = new Date().toLocaleString(Qt.locale(Qt.uiLanguage))
        // noinspection JSUnresolvedVariable
        const generator = `${ Qt.application.name } ${ Qt.application.version }`
        const nickname = this.nicknameGetterFunc()
        // noinspection EqualityComparisonWithCoercionJS
        const videoPath = video != '' ? this.absPathGetterFunc(video) : ''
        const comments = this.commentGetterFunc()
        return { date, generator, nickname, videoPath, comments }
    }

}


class SettingsGenerator {

    /** @param settingsGetterFunc {mpvqcSettingsGetterFunc} */
    constructor(settingsGetterFunc) {
        this.settingsGetterFunc = settingsGetterFunc
    }

    /** @return {MpvqcExportSettings} */
    generateExportSettings() {
        const settings = this.settingsGetterFunc()
        const writeHeaderDate = settings.writeHeaderDate
        const writeHeaderGenerator = settings.writeHeaderGenerator
        const writeHeaderNickname = settings.writeHeaderNickname
        const writeHeaderVideoPath = settings.writeHeaderVideoPath
        return { writeHeaderDate, writeHeaderGenerator, writeHeaderNickname, writeHeaderVideoPath }
    }

    /** @return {MpvqcExportSettings} */
    generateBackupSettings() {
        const writeHeaderDate = true
        const writeHeaderGenerator = true
        const writeHeaderNickname = true
        const writeHeaderVideoPath = true
        return { writeHeaderDate, writeHeaderGenerator, writeHeaderNickname, writeHeaderVideoPath }
    }

}


class DocumentFileCombiner {

    /** @param timeFormatFunc {mpvqcTimeFormatFunc} */
    constructor(timeFormatFunc) {
        this.timeFormatFunc = timeFormatFunc
    }

    /**
     * @param exportData {MpvqcExportData}
     * @param exportSettings {MpvqcExportSettings}
     * @return {string}
     */
    generateDocumentFrom(exportData, exportSettings) {
        const builder = new DocumentBuilder(this.timeFormatFunc)
        builder.addFileTag()
        if (exportSettings.writeHeaderDate)
            builder.addDate(exportData.date)
        if (exportSettings.writeHeaderGenerator)
            builder.addGenerator(exportData.generator)
        if (exportSettings.writeHeaderNickname)
            builder.addNickname(exportData.nickname)
        if (exportSettings.writeHeaderVideoPath)
            builder.addFilePath(exportData.videoPath)
        builder.addBlankLine()
        builder.addDataTag()
        builder.addComments(exportData.comments)
        builder.addCommentSummary()
        builder.addBlankLine()
        return builder.build()
    }

}


class DocumentBuilder {

    /** @param timeFormatFunc {mpvqcTimeFormatFunc} */
    constructor(timeFormatFunc) {
        this.timeFormatFunc = timeFormatFunc
        this.lines = []
        this.comments = 0
    }

    addFileTag() {
        this.lines.push('[FILE]')
    }

    /** @param date {string} */
    addDate(date) {
        this.lines.push(`date      : ${ date }`)
    }

    /** @param generator {string} */
    addGenerator(generator) {
        this.lines.push(`generator : ${ generator }`)
    }

    /** @param nickname {string} */
    addNickname(nickname) {
        this.lines.push(`nick      : ${ nickname }`)
    }

    /** @param filePath {string} */
    addFilePath(filePath) {
        this.lines.push(`path      : ${ filePath }`)
    }

    addBlankLine() {
        this.lines.push('')
    }

    addDataTag() {
        this.lines.push('[DATA]')
    }

    /** @param comments {Array<MpvqcComment>} */
    addComments(comments) {
        this.comments += comments.length
        for (const comment of comments) {
            const time = this.timeFormatFunc(comment.time)
            const commentType = qsTranslate("CommentTypes", comment.commentType)
            this.lines.push(`[${ time }] [${ commentType }] ${ comment.comment }`)
        }
    }

    addCommentSummary() {
        this.lines.push(`# total lines: ${ this.comments }`)
    }

    build() {
        return this.lines.join('\n')
    }

}
