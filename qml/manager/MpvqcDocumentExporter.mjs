/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import { DocumentBuilder } from "./MpvqcDocumentBuilder.mjs";

/**
 * @param settings {MpvqcExportSettings}
 * @param data {MpvqcExportData}
 * @return {string}
 */
export function generateDocumentFrom(data, settings) {
    const documentBuilder = new DocumentBuilder()
    documentBuilder.withFileTag()
    if (settings.writeHeader) {
        if (settings.writeHeaderDate)
            documentBuilder.withDate(data.date)
        if (settings.writeHeaderGenerator)
            documentBuilder.withGenerator(data.generator)
        if (settings.writeHeaderNickname)
            documentBuilder.withNickname(data.nickname)
        if (settings.writeHeaderVideoPath)
            documentBuilder.withFilePath(data.videoPath)
    }
    return documentBuilder
        .withBlankLine()
        .withDataTag()
        .withComments(data.comments)
        .withCommentSummary()
        .withBlankLine()
        .build()
}
