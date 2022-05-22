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
    const builder = new DocumentBuilder()
    builder.addFileTag()
    if (settings.writeHeader) {
        if (settings.writeHeaderDate)
            builder.addDate(data.date)
        if (settings.writeHeaderGenerator)
            builder.addGenerator(data.generator)
        if (settings.writeHeaderNickname)
            builder.addNickname(data.nickname)
        if (settings.writeHeaderVideoPath)
            builder.addFilePath(data.videoPath)
    }
    return builder
        .addBlankLine()
        .addDataTag()
        .addComments(data.comments)
        .addCommentSummary()
        .addBlankLine()
        .build()
}
