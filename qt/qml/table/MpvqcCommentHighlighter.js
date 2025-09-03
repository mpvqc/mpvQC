/*
https://github.com/tc39/proposal-regex-escaping
 */

/**
 *
 * @param comment {string}
 * @param highlightedText {string}
 * @returns {string}
 */
function highlightComment(comment, highlightedText) {
	const re = new RegExp(RegExp.escape(highlightedText), "gi");
	return comment.replace(re, "<b><u>$&</u></b>");
}

// this is a direct translation to code of the spec
if (!RegExp.escape) {
	RegExp.escape = (S) => {
		// 1. let str be ToString(S).
		// 2. ReturnIfAbrupt(str).
		const str = String(S);
		// 3. Let cpList be a List containing in order the code
		// points as defined in 6.1.4 of str, starting at the first element of str.
		const cpList = Array.from(str[Symbol.iterator]());
		// 4. let cuList be a new List
		const cuList = [];
		// 5. For each code point c in cpList in List order, do:
		for (const c of cpList) {
			// i. If c is a SyntaxCharacter then do:
			if ("^$\\.*+?()[]{}|".indexOf(c) !== -1) {
				// a. Append "\" to cuList.
				cuList.push("\\");
			}
			// Append c to cpList.
			cuList.push(c);
		}
		// 7. Return a String whose elements are, in order, the elements of cuList.
		return cuList.join("");
	};
}
