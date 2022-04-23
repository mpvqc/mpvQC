/*
 * Copyright (C) 2013 Nikita Krupenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
 * associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute,
 * sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
 * NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


/**
 * https://github.com/krnekit/qml-utils/blob/master/qml/Log.js
 * @returns {string}
 */
function serialize(object, maxDepth) {
    function _processObject(object, maxDepth, level) {
        const output = Array();
        const pad = "  ";
        if (maxDepth === undefined) {
            maxDepth = -1
        }
        if (level === undefined) {
            level = 0
        }
        const padding = Array(level + 1).join(pad);

        output.push((Array.isArray(object) ? "[" : "{"))
        const fields = Array();
        for (let key in object) {
            const keyText = Array.isArray(object) ? "" : (`"${key}": `);
            if (typeof (object[key]) == "object" && key !== "parent" && maxDepth !== 0) {
                const res = _processObject(object[key], maxDepth > 0 ? maxDepth - 1 : -1, level + 1);
                fields.push(padding + pad + keyText + res)
            } else {
                fields.push(`${padding + pad + keyText}"${object[key]}"`)
            }
        }
        output.push(fields.join(",\n"))
        output.push(padding + (Array.isArray(object) ? "]" : "}"))

        return output.join("\n")
    }

    return _processObject(object, maxDepth)
}
